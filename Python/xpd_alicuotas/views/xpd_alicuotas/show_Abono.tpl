% include('xpd_alicuotas/encabezado.tpl', titulo="Abono", usuario = usuario, estilo = "")

<div class="row">
    <span class="col">
        id:
    </span>
    <span class="col">
        {{objeto['id']}}
    </span>
</div>

<div class="row">
    <span class="col">
        fecha:
    </span>
    <span class="col">
        {{objeto['fecha']}}
    </span>
</div>

<div class="row">
    <span class="col">
        monto:
    </span>
    <span class="col">
        {{objeto['monto']}}
    </span>
</div>

<div class="row">
    <span class="col">
        monto_aprobado:
    </span>
    <span class="col">
        {{objeto['monto_aprobado']}}
    </span>
</div>

<div class="row">
    <span class="col">
        monto_por_aplicar:
    </span>
    <span class="col">
        {{objeto['monto_por_aplicar']}}
    </span>
</div>

<div class="row">
    <span class="col">
        observacion:
    </span>
    <span class="col">
        {{objeto['observacion']}}
    </span>
</div>

<div class="row">
    <span class="col">
        genera_egreso:
    </span>
    <span class="col">
        {{objeto['genera_egreso']}}
    </span>
</div>

<div class="row">
    <span class="col">
        aplicado:
    </span>
    <span class="col">
        {{objeto['aplicado']}}
    </span>
</div>

<div class="row">
    <span class="col">
        aplicado_saldo:
    </span>
    <span class="col">
        {{objeto['aplicado_saldo']}}
    </span>
</div>

<div class="row">
    <span class="col">
        Egreso Generado:
    </span>
    <span class="col">
% if objeto['id_egreso'] is not None:
        <a href="/xpd_alicuotas/egresos/{{objeto['id_egreso']}}">Mostrar</a>
% else:
        No Generado
% end
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/departamentos/{{objeto['id_departamento']}}">
            Volver
        </a>
% if objeto['aplicado'] == '0':
        <a class="btn btn-primary" href="/xpd_alicuotas/abonos/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/abonos/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
% end
    </div>

    <ul class="mt-3 nav nav-tabs nav-justified">

        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#divEventoLimpezaAlicuotas">Abonos Aplicados ({{len(eventolimpezaalicuotas)}})</a>
        </li>

    </ul>
    <div class="tab-content">    

        <div class="tab-pane container active" id="divEventoLimpezaAlicuotas">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Id_alicuota
                        </th>

                        <th>
                            Monto
                        </th>

                    </tr>
                </thead>
                <tbody>
% if len(eventolimpezaalicuotas) == 0:
                    <tr>
                        <td colspan="3">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for eventolimpezaalicuota in eventolimpezaalicuotas:
                    <tr class="small">
                        <td>{{eventolimpezaalicuota['id']}}</td>
                        <td>{{eventolimpezaalicuota['id_alicuota']}}</td>
                        <td>{{eventolimpezaalicuota['monto']}}</td>

                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>    

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
