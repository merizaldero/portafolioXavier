% include('xpd_alicuotas/encabezado.tpl', titulo="Departamento", usuario = usuario, estilo = "")

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
        numero_dep:
    </span>
    <span class="col">
        {{objeto['numero_dep']}}
    </span>
</div>

<div class="row">
    <span class="col">
        propietario:
    </span>
    <span class="col">
        {{objeto['propietario']}}
    </span>
</div>

<div class="row">
    <span class="col">
        arrendatario:
    </span>
    <span class="col">
        {{objeto['arrendatario']}}
    </span>
</div>

<div class="row">
    <span class="col">
        saldo:
    </span>
    <span class="col">
        {{objeto['saldo']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/condominios/{{objeto['id_condominio']}}">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_alicuotas/departamentos/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/departamentos/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

    <ul class="mt-3 nav nav-tabs nav-justified">

        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#divAlicuotas">Alicuotas ({{len(alicuotas)}})</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divAbonos">Abonos ({{len(abonos)}})</a>
        </li>

    </ul>
    <div class="tab-content">    

        <div class="tab-pane container active" id="divAlicuotas">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Anio
                        </th>

                        <th>
                            Mes
                        </th>

                        <th>
                            Monto
                        </th>

                        <th>
                            Monto_pendiente
                        </th>

                        <th>
                            Observaciones
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_alicuotas/departamentos/{{objeto['id']}}/nuevoalicuota">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(alicuotas) == 0:
                    <tr>
                        <td colspan="7">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for alicuota in alicuotas:
                    <tr class="small">
                        <td>{{alicuota['id']}}</td>
                        <td>{{alicuota['anio']}}</td>
                        <td>{{alicuota['mes']}}</td>
                        <td>{{alicuota['monto']}}</td>
%if alicuota['pagado'] == '0':
                        <td class="text-bg-danger">{{alicuota['monto_pendiente']}}</td>
% else:
                        <td class="text-bg-info">{{alicuota['monto_pendiente']}}</td>
% end
                        <td>{{alicuota['observaciones']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_alicuotas/alicuotas/{{alicuota['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divAbonos">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Fecha
                        </th>

                        <th>
                            Monto
                        </th>

                        <th>
                            Monto_aprobado
                        </th>

                        <th>
                            Monto_por_aplicar
                        </th>

                        <th>
                            Observacion
                        </th>

                        <th>
                            Genera_egreso
                        </th>

                        <th>
                            Aplicado
                        </th>

                        <th>
                            Id_egreso
                        </th>

                        <th>
                            Aplicado_saldo
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_alicuotas/departamentos/{{objeto['id']}}/nuevoabono">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(abonos) == 0:
                    <tr>
                        <td colspan="10">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for abono in abonos:
                    <tr class="small">
                        <td>{{abono['id']}}</td>
                        <td>{{abono['fecha']}}</td>
                        <td>{{abono['monto']}}</td>
                        <td>{{abono['monto_aprobado']}}</td>
                        <td>{{abono['monto_por_aplicar']}}</td>
                        <td>{{abono['observacion']}}</td>
                        <td>{{abono['genera_egreso']}}</td>
% if abono['aplicado'] == "1":
                        <td class="text-bg-success">APROBADO</td>
% else:
                        <td class="text-bg-warning">Pendiente Rev</td>
% end
                        <td>{{abono['id_egreso']}}</td>
                        <td>{{abono['aplicado_saldo']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_alicuotas/abonos/{{abono['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>    

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
