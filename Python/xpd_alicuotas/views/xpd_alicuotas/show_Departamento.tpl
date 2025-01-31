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
            <a class="nav-link active" data-bs-toggle="tab" href="#divAlicuotas">Alicuotas</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divEventoLimpiezas">EventoLimpiezas</a>
        </li>

    </ul>
    <div class="tab-content">    

        <div class="tab-pane container active" id="divAlicuotas">
            <table class="mt-2 table table-striped">
                <thead>
                    <tr>

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
                            Pagado
                        </th>

                        <th>
                            Observaciones
                        </th>

                        <th>
                            <a class="btn btn-primary" href="/xpd_alicuotas/departamentos/{{objeto['id']}}/nuevoalicuota">Crear Nuevo</a>
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
                    <tr>
                        <td>{{alicuota['id']}}</td>
                        <td>{{alicuota['anio']}}</td>
                        <td>{{alicuota['mes']}}</td>
                        <td>{{alicuota['monto']}}</td>
                        <td>{{alicuota['monto_pendiente']}}</td>
                        <td>{{alicuota['pagado']}}</td>
                        <td>{{alicuota['observaciones']}}</td>
                        <td>
                            <a class="btn btn-primary" href = "/xpd_alicuotas/alicuotas/{{alicuota['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divEventoLimpiezas">
            <table class="mt-2 table table-striped">
                <thead>
                    <tr>

                        <th>
                            Id
                        </th>

                        <th>
                            Fecha
                        </th>

                        <th>
                            Fecha_validacion
                        </th>

                        <th>
                            Observacion
                        </th>

                        <th>
                            <a class="btn btn-primary" href="/xpd_alicuotas/departamentos/{{objeto['id']}}/nuevoeventolimpieza">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(eventolimpiezas) == 0:
                    <tr>
                        <td colspan="4">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for eventolimpieza in eventolimpiezas:
                    <tr>
                        <td>{{eventolimpieza['id']}}</td>
                        <td>{{eventolimpieza['fecha']}}</td>
                        <td>{{eventolimpieza['fecha_validacion']}}</td>
                        <td>{{eventolimpieza['observacion']}}</td>
                        <td>
                            <a class="btn btn-primary" href = "/xpd_alicuotas/eventolimpiezas/{{eventolimpieza['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>    

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
