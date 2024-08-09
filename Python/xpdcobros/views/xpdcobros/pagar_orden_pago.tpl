% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Orden de Pago", usuario = usuario, estilo =".navbar{background-color:#aaaa00;} .card-header{font-weight:bold;color:#ffffff;background-color:#880088;} .card-footer{background-color:#ff00ff;}")
<div class="mt-3 row">
    <div class="col-6">
    <div class="card small">
        <div class="card-header">Organizaci&oacute;n</div>
        <div class="card-body">
            <div class="container">
                <div class="row">
                    <div class="col strong">Empresa / Servicio :</div>
                    <div class="col">{{ cobrador['nombre'] }}</div>
                </div>
                <div class="row">
                    <div class="col strong">E-mail :</div>
                    <div class="col">{{ cobrador['email'] }}</div>
                </div>
            </div>
        </div>
    </div>
    </div>
    <div class="col-6">
    <div class="card small">
        <div class="card-header">
            Cliente
        </div>
        <div class="card-body">
            <div class="container">
    % if pagador['nombre'] != pagador['email']: 
                <div class="row">
                    <div class="col strong">Nombre:</div>
                    <div class="col">{{ pagador['nombre'] }}</div>
                </div>
    % end            
                <div class="row">
                    <div class="col strong">E-mail :</div>
                    <div class="col">{{ pagador['email'] }}</div>
                </div>
    % if pagador['saldo'] > 0.0 :
                <div class="row">
                    <div class="col strong">Saldo a Favor :</div>
                    <div class="col">{{ pagador['saldo'] }}</div>
                </div>
    % else:
                <div class="row">
                    <div class="col strong">Pendiente Pagar :</div>
                    <div class="col">{{ - pagador['saldo'] }}</div>
                </div>
    % end
                <div class="row">
                    <div class="col strong">Actualizado :</div>
                    <div class="col">{{pagador['fecha_saldo'][:10]}}</div>
                </div>
            </div>
        </div>
    </div>
    </div>
</div>
<div class="card mt-3 small">
    <div class="card-header">
        Orden de Pago
    </div>
    <div class="card-body">
        <div class="container">
            <div class="row">
                <div class="col-2 strong"><b>Orden #:</b></div>
                <div class="col-10">{{orden_pago['id']}}</div>
            </div>
            <div class="row">
                <div class="col-2 strong"><b>Descripci&oacute;n:</b></div>
                <div class="col-10">{{orden_pago['descripcion']}}</div>
            </div>
            <div class="row">
                <div class="col-2 strong"><b>Fecha Emisi&oacute;n:</b></div>
                <div class="col-4">{{orden_pago['fecha_emision'][:10]}}</div>
                <div class="col-2 strong"><b>Valor:</b></div>
                <div class="col-4">{{"{0:.2f}".format(orden_pago['monto'])}}</div>                
            </div>
            <div class="row">
                <div class="col-2 strong"><b>Fecha Vencimiento:</b></div>
                <div class="col-4">{{orden_pago['fecha_vencimiento'][:10]}}</div>
                <div class="col-2 strong"><b>Valor Pendiente:</b></div>
                <div class="col-4"><b>{{"{0:.2f}".format(orden_pago['monto_pendiente'])}}</b></div>
            </div>
        </div>
    </div>
</div>

% if len(abonos) > 0:
<div class="card mt-3 small">
    <div class="card-header">
        Abonos
    </div>
    <div class="card-body">
        <table class="table table-striped">
            <thead>
            <tr>
                <th>Fecha</th>
                <th>Cuenta</th>
                <th>Monto</th>
                <th>Estado</th>
                <th>Fecha Est.</th>
                <th>Monto Aprobado</th>
                <th>Observaciones</th>
            </tr>
            </thead>
            <tbody>
% for abn in abonos:
            <tr>
                <td>{{abn['fecha_transaccion'][:10]}}</td>
                <td>{{abn['nombre_banco']}} {{abn['tipo_cuenta']}} {{abn['numero_cuenta'][:10]}}</td>
                <td>{{"{0:.2f}".format(abn['monto_registrado'])}}</td>
                <td>
% if abn['estado'] == 'R':
                    REGISTRADO
% elif abn['estado'] == 'A':
                    APROBADO
% elif abn['estado'] == 'X':
                    RECHAZADO
% end                
                </td>
                <td>{{abn['fecha_transaccion'][:10] if abn['fecha_transaccion'] else '-'}}</td>
                <td>{{"{0:.2f}".format(abn['monto_registrado']) if abn['monto_registrado'] else '-'}}</td>
                <td>{{abn['observaciones'] if abn['observaciones'] else '-'}}</d>
            </tr>
% end
            </tbody>
        </table>
    </div>
</div>
% end

% if mensaje != "":
<div class="mt-3 alert alert-{{lvl}}">
    {{mensaje}}
% if 'id' in abono:
    <a class="btn btn-primary" href = "/xpdcobros/ordenes_pago/{{orden_pago['id']}}">Registrar Nuevo Abono</a>        
% end
</div>
% end

% if orden_pago['pagado'] == 1:
<div class="mt-3 alert alert-success">
Esta Orden de Pago se encuentra pagada. No requiere registrar m&aacute;s abonos.
</div>
% else:

<form method="post" enctype="multipart/form-data">
<input id="hid_id_imagen" type="hidden" name="id_imagen" value="{{abono['id_imagen']}}">            
<div class="mt-3 row">
    <div class="col-6">
    <div class="card small">
        <div class="card-header">
            <span>Captura de Transferencia</span>
% if 'id' not in abono:            
            <span class="input-group input-group-sm">
            <input class="form-control" type="file" name="file_imagen" placeholder="Seleccione Archivo y presione en Cargar Imagen">
            <input class="btn btn-primary" type="submit" name="accion" value="Cambiar Imagen">
            </span>
% end
        </div>
        <div class="card-body d-flex flex-row justify-content-center">
            <iframe class="m-5 border" style="width:500px;height:500px" src="/xpdcobros/imagenes/{{abono['id_imagen']}}">
            </iframe>
        </div>
    </div>
    </div>
    <div class="col-6">
    <div class="card small">
        <div class="card-header">
            Detalle de Transferencia
        </div>
        <div class="card-body">
            <div>
                <label class="form-label">Cuenta que recibe Transferencia:</label>
% for cuenta in cuentas:
                <div class="form-check">
                    <input onclick="validar_formulario()" type="radio" class="form-check-input" id="id_cta_bco_{{cuenta['id']}}" name="id_cta_bco" value="{{cuenta['id']}}"
% if cuenta['id'] == id_cta_bco:
                    checked
% end
                    >
                    <label for="id_cta_bco_{{cuenta['id']}}" class="form-check-label">{{cuenta['nombre_banco']}} / {{cuenta['tipo_cuenta']}} / {{cuenta['numero_cuenta']}}</label>
                </div>
% end                
                <label for="numero_transaccion" class="form-label">Transacci&oacute;n #:</label>
                <input onchange="validar_formulario()" id="txt_numero_transaccion" class="form-control" name="numero_transaccion" placeholder="00000000000" value="{{abono['numero_transaccion']}}" required>
                <label for="fecha_transaccion" class="form-label">Fecha de Transacci&oacute;n:</label>
                <input onchange="validar_formulario()" id="txt_fecha_transaccion" class="form-control" name="fecha_transaccion" placeholder="AAAA-MM-DD" value="{{abono['fecha_transaccion']}}" required>
                <label for="monto_registrado" class="form-label">Monto:</label>
                <input onchange="validar_formulario()" id="txt_monto_registrado" class="form-control" name="monto_registrado" placeholder="0000.00" value="{{abono['monto_registrado']}}" required>
            </div>
        </div>        
        <div class="card-body">
            <div id="div_alerta_validacion" class="alert alert-warning">
            </div>
        </div>
% if 'id' not in abono:        
        <div class="card-footer d-flex flex-row justify-content-end">
            <input id="btn_registrar_abono" class="btn btn-success" type="submit" name="accion" value="Registrar Abono &gt;&gt;">
        </div>
% end
    </div>
    </div>
</div>
</form>

<script language="javascript">

function validar_formulario(){

    const div_alerta_validacion = document.getElementById("div_alerta_validacion");

% if 'id' not in abono:    
    const hid_id_imagen = document.getElementById("hid_id_imagen");
    const txt_numero_transaccion = document.getElementById("txt_numero_transaccion");
    const txt_fecha_transaccion = document.getElementById("txt_fecha_transaccion");
    const txt_monto_registrado = document.getElementById("txt_monto_registrado");
    const btn_registrar_abono = document.getElementById("btn_registrar_abono");
    const observaciones = [];
    if(hid_id_imagen.value == "-1"){
        observaciones.push("Debe cargar una imagen con el comprobante de su transferencia. La información ingrasada debe corresponder con la imagen.");
    }
    let elegido_banco = false;
% for cuenta in cuentas:
    if( !elegido_banco && document.getElementById('id_cta_bco_{{cuenta['id']}}').checked ){
        elegido_banco = true;
    }
% end
    if( !elegido_banco ){
        observaciones.push("La transferencia debe ser realizada a uno de las cuentas bancarias de la lista. Seleccione la Cuenta Destino utilizada.");
    }
    if(txt_numero_transaccion.value == ""){
        observaciones.push("Debe ingresar el número de Transacción.");
    }
    if(txt_fecha_transaccion.value.length != 10){
        observaciones.push(`Debe ingresar la fecha de transacción en formato AAAA-MM-DD. ${txt_fecha_transaccion.value.length}`);
    }

    if(txt_monto_registrado.value.length == 0){
        observaciones.push("Debe ingresar Monto de la Transferencia.");
    }else if( isNaN(txt_monto_registrado.value) ){
        observaciones.push("El Monto de la Transferencia ingresado debe ser una cantidad válida.");
    }else if( parseFloat(txt_monto_registrado.value) > {{"{0:.2f}".format(orden_pago['monto_pendiente'])}} ){
        observaciones.push("El Monto de la Transferencia ingresado sobrepasa el Monto pendiente de pago.");
    }

    div_alerta_validacion.innerHTML = "";

    if(observaciones.length == 0){
        btn_registrar_abono.disabled = false;
        div_alerta_validacion.classList.add("alert-success");
        div_alerta_validacion.classList.remove("alert-warning");
        div_alerta_validacion.innerHTML = "La información de la Transferencia está completa y se puede Registrar";
    }else{
        btn_registrar_abono.disabled = true;
        div_alerta_validacion.classList.add("alert-warning");
        div_alerta_validacion.classList.remove("alert-success");
        const ulObservaciones = document.createElement("ul");
        observaciones.forEach(observacion=>{
            const liObservacion = document.createElement("li");
            liObservacion.innerText = observacion;
            ulObservaciones.appendChild(liObservacion);
        });
        div_alerta_validacion.appendChild(ulObservaciones);
    }
% else:
    div_alerta_validacion.classList.add("collapse");
% end
}

validar_formulario();

</script>
% end


% include('xpdcobros/pie.tpl', usuario = usuario)