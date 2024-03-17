from bottle import run, debug, route, error, static_file, template, request, redirect, TEMPLATE_PATH
from bottle import Bottle

import xpd_usr
import pymvu
from uuid import uuid4

from bottle.ext.websocket import websocket

import json

RUTA_BASE = ''

USUARIOS = []

SALA = {}

def servir_websocket(ws):
    usuario = xpd_usr.getCurrentUser(request)
    if usuario is None:
        print('No se pudo identificar usuario para websocket')
        return
    
    if usuario['id'] in USUARIOS:
        print('Usuario ya tiene abierto websocket')
        return
    
    USUARIOS.append( usuario['id'] )
    
    id_sala = None

    while True:
        msg = ws.receive()
        if msg is None:
            break
        print('procesando ' + msg)
        try:
            comando = json.loads(msg)
            if comando['accion'] == 'solicitar_sala':
                if id_sala is not None:
                    break                    
                id_sala = comando['id_sala']
                if id_sala not in SALA.keys():
                    SALA[id_sala] = { 'usuarios':[], 'avatares':[]}
                asientos = comando['asientos']
                if usuario['id'] in [ x['id'] for x in SALA[id_sala]['usuarios'] ]:
                    print('Usuario {0} ya se encuentra en la sala {1}'.format(usuario['username'], id_sala))
                    break
                asientos_disponibles = [x for x in asientos if x not in [ y['asiento'] for y in SALA[id_sala]['avatares'] ] ]
                if len(asientos_disponibles) == 0:
                    print('Usuario {0} ya se encuentra en la sala {1}'.format(usuario['username'], id_sala))
                    break
                apariencias = pymvu.consultar(pymvu.Apariencias, 'findByUsuario', {'id_usuario':usuario['id'] , 'activo' : 1})
                apariencias = [x for x in apariencias if x['es_default'] == 1]
                if len(apariencias) == 0 :
                    print('No se ha encontrado apariencia default para {0}'.format(usuario['username']))
                prendas_apariencia = pymvu.get_prendas_apariencia(apariencias[0]['id'])
                prendas_apariencia = [x for x in prendas_apariencia if x['id_modelo'] is not None]
                usuario_info = {'id':usuario['id'], 'username':usuario['username'], 'ws': ws }
                avatar_info = { 'id': str(uuid4()), 'nombre': usuario['username'] , 'id_usuario':usuario['id'] ,'id_apariencia': apariencias[0]['id'], 'modelos':prendas_apariencia, 'asiento':asientos_disponibles[0] }
                SALA[id_sala]['usuarios'].append( usuario_info )
                SALA[id_sala]['avatares'].append( avatar_info )
                for usuario_info in SALA[id_sala]['usuarios']:
                    if usuario_info['id'] == usuario['id'] :
                        # al avatar que inicia sesion se le envia agregar a todos los avatares
                        ws.send( json.dumps({'accion':'agregar_avatar', 'avatares':SALA[id_sala]['avatares'] }) )
                    else:
                        usuario_info['ws'].send( json.dumps({'accion':'agregar_avatar', 'avatares':[avatar_info,] }) )
            elif comando['accion'] == 'solicitar_asiento':
                if id_sala is None:
                    break
                id_avatar = comando['id_avatar']
                avatares = [ y for y in SALA[id_sala]['avatares'] if y['id'] == id_avatar ]
                if len(avatares) == 0 or avatares[0]['id_usuario'] != usuario['id'] :
                    print('Avatar {0} no existe o no pertenece al usuario {1}'.format(id_avatar, usuario['username']))
                    continue
                asiento = comando['asiento']
                if asiento in [ y['asiento'] for y in SALA[id_sala]['avatares'] ] :
                    print('El asiento {0} ya esta ocupado'.format(asiento))
                    continue
                avatares[0]['asiento'] = asiento
                for usuario_info in SALA[id_sala]['usuarios']:
                    usuario_info['ws'].send( json.dumps({'accion':'asiento_avatar', 'id_avatar':id_avatar, 'asiento' : asiento }) )
            elif comando['accion'] == 'cambiar_apariencia':
                pass
            elif comando['accion'] == 'solicitar_npc':
                pass
            elif comando['accion'] == 'apagar_npc':
                pass
        except Exception as ex:
            print(repr (ex))
            
        finally:
            pass

    # remueve al usuario de todas las salas
    for id_sala1 in SALA.keys():
        usuarios_quitar = [x for x in SALA[id_sala1]['usuarios'] if x['id'] == usuario['id']]
        for usuario_quitar in usuarios_quitar:
            SALA[id_sala1]['usuarios'].remove(usuario_quitar)
        avatares_quitar = [x for x in SALA[id_sala1]['avatares'] if x['id_usuario'] == usuario['id']]
        for avatar_quitar in avatares_quitar:
            for usuario_not in SALA[id_sala1]['usuarios']:
                usuario_not['ws'].send( json.dumps({'accion':'eliminar_avatar', 'avatar_id':avatar_quitar['id'] }) )
            SALA[id_sala1]['avatares'].remove(avatar_quitar)
        
    USUARIOS.remove( usuario['id'] )
    print('Usuario {0} ha salido de sala {1}'.format(usuario['username'], id_sala))

def rutearModulo( app : Bottle, ruta_base : str ):
    # encapsula Session Middleware
    RUTA_BASE = ruta_base

    app.route( ruta_base + '/socket' , method = ['GET'], apply = [websocket])(servir_websocket)
