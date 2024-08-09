% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Configuracion", usuario = usuario, estilo =".card-header{font-weight:bold;color:#ffffff;background-color:#880088;} .card-footer{background-color:#ff00ff;}")
<div class="w-100 d-flex flex-row justify-content-end">
    <a class="btn btn-secondary btn-sm" href="/xpdcobros/usuarios/organizacion/{{organizacion['id']}}">Regresar a {{organizacion['nombre']}}</a>
</div>
<div class="card">
    <div class="card-header">
        Cliente
    </div>
    <div class="card-body">
        <div class="d-flex flex-row justify-content-between">

            <div class="container">
                <div class="row">
                    <div class="col strong">Nombre:</div>
                    <div class="col">{{ cliente['nombre'] }}</div>
                </div>
                <div class="row">
                    <div class="col strong">E-mail :</div>
                    <div class="col">{{ cliente['email'] }}</div>
                </div>
    % if cliente['saldo'] > 0.0 :
                <div class="row">
                    <div class="col strong">Saldo a Favor :</div>
                    <div class="col">{{ cliente['saldo'] }}</div>
                </div>
    % else:
                <div class="row">
                    <div class="col strong">Pendiente Pagar :</div>
                    <div class="col">{{ - cliente['saldo'] }}</div>
                </div>
    % end
                <div class="row">
                    <div class="col strong">Actualizado :</div>
                    <div class="col">{{cliente['fecha_saldo'][:10]}}</div>
                </div>
            </div>

            <div class="d-flex flex-column">
                <form method="POST">
                <input type="hidden" name="accion" value="editar">
                <input type="submit" class="btn btn-primary btn-sm" value="Editar">
                </form>                
            </div>

        </div>
        
    </div>
</div>

<div class="card mt-3">
    <div class="card-header">
        Abonos
    </div>
    <div id="div_abonos" class="card-body">
        <div class="w-100 d-flex flex-row border-bottom">
            <a href="#div_abonos_registrados" class="border border-bottom-0 rounded-top p-2" data-bs-toggle="collapse">Requieren Aprobaci&oacute;n</a>
            <a href="#div_abonos_aprobados" class="border border-bottom-0 rounded-top p-2" data-bs-toggle="collapse">Aprobados</a>
            <a href="#div_abonos_rechazados" class="border border-bottom-0 rounded-top p-2" data-bs-toggle="collapse">Rechazados</a>
        </div>

        <div id="div_abonos_registrados" class="collapse show list-group" data-bs-parent="#div_abonos">
% if len(abonos_registrados) == 0 :
            <span class="list-group-item">No se registra Abonos para revisi&oacute;n</span>
% end           
        </div>

        <div id="div_abonos_aprobados" class="collapse list-group" data-bs-parent="#div_abonos">
% if len(abonos_aprobados) == 0 :
            <span class="list-group-item">No se registra Abonos Aprobados</span>
% end           
        </div>

        <div id="div_abonos_rechazados" class="collapse list-group" data-bs-parent="#div_abonos">
% if len(abonos_rechazados) == 0 :
            <span class="list-group-item">No se registra Abonos Rechazados</span>
% end
        </div>

    </div>
</div>

<div class="card mt-3">
    <div class="card-header">
        Ordenes de Pago
    </div>
    <div class="card-body">
% if len(ordenes_pago) == 0 :
    <div>Al momento no se registran &oacute;rdenes de pago.</div>
% else :
    <table class="table table-striped">
        <tbody>
    % for orden_pago in ordenes_pago :
            <tr>
                <td class="w-75">
                    Orden #{{orden_pago['id']}}<br>
                    {{orden_pago['descripcion']}}<br>
                    {{orden_pago['fecha_emision'][:10]}}<br>                            
                    Pendiente {{"{0:.2f}".format(orden_pago['monto'])}} de <b>{{"{0:.2f}".format(orden_pago['monto_pendiente'])}}</b>                            
                </td>
                <td class="w-25">
                    <a class="btn btn-success btn-sm" href="/xpdcobros/usuarios/organizacion/{{organizacion['id']}}/ordenes_pago/{{orden_pago['id']}}">
                    ...
                    </a>
                </td>
            </tr>
    % end
        </tbody>
    </table>
% end

    </div>
</div>

% include('xpdcobros/pie.tpl', usuario = usuario)