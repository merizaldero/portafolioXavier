% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Configuracion", usuario = usuario, estilo =".card-header{font-weight:bold;color:#ffffff;background-color:#880088;} .card-footer{background-color:#ff00ff;}")

<div class="mt-3 row">
    <div class="col-6">
    <div class="card">
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
    <div class="card">
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

<div class="card mt-3">
    <div class="card-header">
        Ordenes de Pago
    </div>
    <div class="card-body">
% if len(ordenes_pago) == 0 :
    <div>Al momento no se registran &oacute;rdenes de pago.</div>
% else :
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Orden #</th>
                <th>Descripcion</th>
                <th>Emitido</th>
                <th>Vence</th>
                <th>Monto</th>
                <th>Pendiente</th>
            </tr>
        </thead>
        <tbody>
    % for orden_pago in ordenes_pago :
            <tr>
                <td>{{orden_pago['id']}}</td>
                <td>{{orden_pago['descripcion']}}</td>
                <td>{{orden_pago['fecha_emision'][:10]}}</td>
                <td>{{orden_pago['fecha_vencimiento'][:10]}}</td>
                <td class="text-end">{{"{0:.2f}".format(orden_pago['monto'])}}</td>
                <td class="text-end"><b>{{"{0:.2f}".format(orden_pago['monto_pendiente'])}}</b></td>
                <td>
                    <a class="btn btn-success btn-sm" href="/xpdcobros/ordenes_pago/{{orden_pago['id']}}">
                    Pagar
                    </a>
                </td>
            </tr>
    % end
        </tbody>
    </table>
% end

    </div>
</div>

