from contextlib import closing
import sqlite3
import datetime

DATABASE = './data/crrnc.db'

CAMPOS_TIPO_TRANSACCION = ['id','descripcion','trx_bal','fecha_creacion']
CAMPOS_CUENTA = ['id','avatar_uuid','saldo','fecha_creacion','fecha_actualizacion']
CAMPOS_TRANSACCION = ['id','tipo_id','ip_origen','fecha_contable','marca_tiempo','monto','descripcion']
CAMPOS_MOVIMIENTO = ['id', 'transaccion_id','avatar_uuid', 'fecha_contable', 'marca_tiempo', 'monto', 'saldo', 'descripcion']

MINTER = 'ad285f64-d318-44da-8943-c2d180cb2412'

COSTO_ESTIMADO = 0

def get_minteador():
    return '' + MINTER

def get_costo_estimado( monto = 0.0 ):
    return COSTO_ESTIMADO * monto

def __connect_db( database ):
    """Returns a new connection to the database."""
    return sqlite3.connect(database)

def init_db( database = DATABASE ):
    """Creates the database tables."""
    with closing( __connect_db( database = database ) ) as db:
        with open('esquema.sql','r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def __serializar_fila(fila,arreglo_campos):
    return { arreglo_campos[i] : fila[i] for i in range( len(arreglo_campos) )  }

def listar_cuentas( page_size = 10, page = 1, database = DATABASE ):
    entries = []
    with closing( __connect_db( database = database ) ) as db:
        cur = db.execute('select ' + ','.join(CAMPOS_CUENTA) + ' from cuenta order by id desc limit {0} offset {1} '.format(page_size, (page - 1) * page_size ) )
        entries = [ __serializar_fila(row, CAMPOS_CUENTA) for row in cur.fetchall()]
    return entries

def obtener_cuenta( avatar_uuid, database = DATABASE ):
    cuenta = None
    with closing(__connect_db( database = database )) as db:
        cur = db.execute('select ' + ','.join(CAMPOS_CUENTA) + ' from cuenta where avatar_uuid = ? ', [avatar_uuid,] )
        lista = [ __serializar_fila(row, CAMPOS_CUENTA) for row in cur.fetchall()]
    if len(lista) == 1:
        cuenta = lista[0]
    return cuenta

def listar_transacciones_por_fecha( fecha, page_size = 10, page = 1 , database = DATABASE ):
    entries = []
    with closing(__connect_db( database = database )) as db:
        cur = db.execute('select ' + ','.join(CAMPOS_TRANSACCION) + ' from transaccion where fecha_contable = ? order by id limit {0} offset {1} '.format( page_size, (page - 1) * page_size ), [fecha,] )
        entries = [ __serializar_fila(row, CAMPOS_TRANSACCION) for row in cur.fetchall()]
    return entries

def listar_movimientos_cuenta( avatar_uuid, page_size = 10, page = 1 , database = DATABASE ):
    entries = []
    with closing(__connect_db( database = database )) as db:
        cur = db.execute('select ' + ','.join(CAMPOS_MOVIMIENTO) + ' from movimiento  where avatar_uuid = ? order by id desc limit {0} offset {1} '.format(page_size, (page - 1) * page_size ), [avatar_uuid,] )
        entries = [ __serializar_fila(row, CAMPOS_MOVIMIENTO) for row in cur.fetchall()]
    return entries

def listar_movimientos_transaccion( transaccion_id , page_size = 10, page = 1 , database = DATABASE ):
    entries = []
    with closing(__connect_db( database = database )) as db:
        cur = db.execute('select ' + ','.join(CAMPOS_MOVIMIENTO) + ' from movimiento  where transaccion_id = ? order by id limit {0} offset {1} '.format(page_size, (page - 1) * page_size ), [transaccion_id ,] )
        entries = [ __serializar_fila(row, CAMPOS_MOVIMIENTO) for row in cur.fetchall()]
    return entries

def crear_cuenta( avatar_uuid , database = DATABASE ):
    last_id = -1
    fecha = str(datetime.datetime.now())
    with closing(__connect_db( database = database )) as db:
        cur = db.execute('insert into cuenta (' + ','.join(CAMPOS_CUENTA[1:]) + ') values ( ' + ','.join([ '?' for x in CAMPOS_CUENTA[1:] ]) + ' )',
            [avatar_uuid, 0.0, fecha , fecha] )
        db.commit()
    return obtener_cuenta(avatar_uuid , database = database )

def crear_cuenta_si_no_existe( avatar_uuid, database = DATABASE ):
    minter = obtener_cuenta( avatar_uuid , database = database )
    if minter is None:
        minter = crear_cuenta( avatar_uuid , database = database )
    return minter

def nueva_transaccion(tipo, ip_origen, movimientos, database ):
    resultado = None
    cuentas = [ m['avatar_uuid'] for m in movimientos ]
    if len([x for x in movimientos if x['monto'] == 0.0 ]) > 0:
        raise Exception("Monto por cuenta no puede ser cero")
    with closing(__connect_db( database = database )) as db:
        # valida Tipo transaccion
        cur = db.execute('select ' + ','.join(CAMPOS_TIPO_TRANSACCION) + ' from tipo_transaccion where descripcion = ? ', [tipo, ] )
        tipo_transaccion = [ __serializar_fila(row, CAMPOS_TIPO_TRANSACCION) for row in cur.fetchall() ]
        if len(tipo_transaccion) == 0:
            raise Exception("Transaccion no válida")
        tipo_transaccion = tipo_transaccion[0]
        # consulta cuentas
        cur = db.execute('select ' + ','.join(CAMPOS_CUENTA) + ' from cuenta where avatar_uuid in ( ' + ','.join(['?' for x in cuentas]) + ' ) ', cuentas)
        lista_cuentas = [ __serializar_fila(row, CAMPOS_CUENTA) for row in cur.fetchall() ]
        if len(cuentas) != len(lista_cuentas):
            raise Exception("Inconsistencia de Cuentas")
        saldos = [ ( a['avatar_uuid'], a['saldo'] + m['monto'] ) for a in lista_cuentas for m in movimientos if m['avatar_uuid'] == a['avatar_uuid'] ]
        if len( [ s for s in saldos if s[1] < 0.0 ] ) > 0:
            raise Exception('Saldo insuficiente')
        monto_transaccion = sum( [ m['monto'] for m in movimientos if m['monto'] > 0.0 ] )
        if tipo_transaccion['trx_bal'] == 1 and sum( [ m['monto'] for m in movimientos ] ) != 0.0 :
            raise Exception("Transaccion inconsistente")
        # arranca secuencia
        fecha = str(datetime.date.today())
        fechahora = str(datetime.datetime.now())
        cur = db.execute('insert into transaccion ( ' + ','.join(CAMPOS_TRANSACCION[1:]) + ' ) values ( ' + ','.join([ '?' for x in CAMPOS_TRANSACCION[1:] ]) + ' ) ',
            [ tipo_transaccion['id'], ip_origen, fecha, fechahora, monto_transaccion, tipo_transaccion['descripcion'] ] )
        transaccion_id = cur.lastrowid
        for m in movimientos:
            a = [ c for c in lista_cuentas if c['avatar_uuid'] == m['avatar_uuid'] ] [0]
            saldo = [ s[1] for s in saldos if s[0] == m['avatar_uuid'] ] [0]
            cur = db.execute('insert into movimiento ( ' + ','.join(CAMPOS_MOVIMIENTO[1:]) + ' ) values ( ' + ','.join([ '?' for x in CAMPOS_MOVIMIENTO[1:] ]) + ' ) ',
                [ transaccion_id, m['avatar_uuid'], fecha, fechahora, m['monto'], saldo, tipo_transaccion['descripcion'] ] )
            cur = db.execute('update cuenta set saldo = ?, fecha_actualizacion = ? where avatar_uuid = ? ',
                [ saldo, fechahora, m['avatar_uuid'] ] )
        cur = db.execute('select ' + ','.join(CAMPOS_TRANSACCION) + ' from transaccion where id = ? ', [transaccion_id ,] )
        resultado = __serializar_fila( cur.fetchall()[0] , CAMPOS_TRANSACCION)
        cur = db.execute('select ' + ','.join(CAMPOS_MOVIMIENTO) + ' from movimiento where transaccion_id = ? ', [transaccion_id ,] )
        resultado['movimientos'] = [ __serializar_fila(row, CAMPOS_MOVIMIENTO) for row in cur.fetchall()]
        db.commit()
    return resultado

def mintear( monto, database = DATABASE):
    minter = crear_cuenta_si_no_existe(MINTER, database = database)
    return nueva_transaccion( 'MINT' , 'localhost', [ {'avatar_uuid':MINTER, 'monto': monto } ] , database = database )

def comprar( comprador_uuid, monto, ip_origen, database = DATABASE):
    comprador = crear_cuenta_si_no_existe( comprador_uuid , database = database)
    minter = obtener_cuenta( MINTER , database = database )
    if minter is None:
        raise Exception("Debe existir un Minter en el sistema")
    return nueva_transaccion( 'COMPRA DIVISA' , ip_origen, [ {'avatar_uuid':MINTER, 'monto': - monto }, {'avatar_uuid':comprador_uuid, 'monto': monto } ] , database = database )

def transferir( debito_uuid, credito_uuid, monto, ip_origen, database = DATABASE):
    creditado = crear_cuenta_si_no_existe( credito_uuid , database = database)
    debitado = obtener_cuenta( debito_uuid , database = database )
    if debitado is None:
        raise Exception("Cuenta no existe")
    return nueva_transaccion( 'TRANSFERENCIA' , ip_origen, [ {'avatar_uuid':debito_uuid, 'monto': - monto }, {'avatar_uuid':credito_uuid, 'monto': monto } ] , database = database )

def obtener_stats( database = DATABASE):
    minter = crear_cuenta_si_no_existe(MINTER, database = database)
    stats = { 'saldo_minter' : minter['saldo'] }
    entries = []
    with closing(__connect_db( database = database )) as db:
        cur = db.execute('select sum(saldo) saldo_total_sistema, sum(case when saldo > 0.0 then 1 else 0 end) cuentas_activas from cuenta ' )
        entries = cur.fetchall()
    if len(stats) == 1:
        stats['saldo_sistema'] = entries[0][0]
        stats['cuentas_activas'] = entries[0][1]
    return stats
