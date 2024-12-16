% include('xpd_sistema_puntos/encabezado.tpl', titulo="Evaluado", usuario = usuario, estilo = "")

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
        nombre:
    </span>
    <span class="col">
        {{objeto['nombre']}}
    </span>
</div>

<div class="row">
    <span class="col">
        id_icono:
    </span>
    <span class="col">
        {{objeto['id_icono']}}
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

<div class="row">
    <span class="col">
        orden:
    </span>
    <span class="col">
        {{objeto['orden']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_sistema_puntos/evaluados">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_sistema_puntos/evaluados/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_sistema_puntos/evaluados/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

    <ul class="mt-3 nav nav-tabs nav-justified">

        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#divTransaccions">Transaccions</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divMetas">Metas</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divLogros">Logros</a>
        </li>

    </ul>
    <div class="tab-content">    

        <div class="tab-pane container active" id="divTransaccions">
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
                            Id_icono
                        </th>

                        <th>
                            Descripcion
                        </th>

                        <th>
                            Monto
                        </th>

                        <th>
                            Saldo
                        </th>

                        <th>
                            <a class="btn btn-primary" href="/xpd_sistema_puntos/evaluados/{{objeto['id']}}/nuevotransaccion">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(transaccions) == 0:
                    <tr>
                        <td colspan="6">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for transaccion in transaccions:
                    <tr>
                        <td>{{transaccion['id']}}</td>
                        <td>{{transaccion['fecha']}}</td>
                        <td>{{transaccion['id_icono']}}</td>
                        <td>{{transaccion['descripcion']}}</td>
                        <td>{{transaccion['monto']}}</td>
                        <td>{{transaccion['saldo']}}</td>
                        <td>
                            <a class="btn btn_primary" href = "/xpd_sistema_puntos/transaccions/{{transaccion['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divMetas">
            <table class="mt-2 table table-striped">
                <thead>
                    <tr>

                        <th>
                            Id
                        </th>

                        <th>
                            Descripcion
                        </th>

                        <th>
                            Id_icono
                        </th>

                        <th>
                            Puntos_requeridos
                        </th>

                        <th>
                            Puntos_logro
                        </th>

                        <th>
                            Fecha_creacion
                        </th>

                        <th>
                            Fecha_vencimiento
                        </th>

                        <th>
                            <a class="btn btn-primary" href="/xpd_sistema_puntos/evaluados/{{objeto['id']}}/nuevometa">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(metas) == 0:
                    <tr>
                        <td colspan="7">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for meta in metas:
                    <tr>
                        <td>{{meta['id']}}</td>
                        <td>{{meta['descripcion']}}</td>
                        <td>{{meta['id_icono']}}</td>
                        <td>{{meta['puntos_requeridos']}}</td>
                        <td>{{meta['puntos_logro']}}</td>
                        <td>{{meta['fecha_creacion']}}</td>
                        <td>{{meta['fecha_vencimiento']}}</td>
                        <td>
                            <a class="btn btn_primary" href = "/xpd_sistema_puntos/metas/{{meta['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divLogros">
            <table class="mt-2 table table-striped">
                <thead>
                    <tr>

                        <th>
                            Id
                        </th>

                        <th>
                            Id_icono
                        </th>

                        <th>
                            Descripcion
                        </th>

                        <th>
                            Fecha
                        </th>

                        <th>
                            Puntos_requeridos
                        </th>

                        <th>
                            Puntos_logro
                        </th>

                        <th>
                            <a class="btn btn-primary" href="/xpd_sistema_puntos/evaluados/{{objeto['id']}}/nuevologro">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(logros) == 0:
                    <tr>
                        <td colspan="6">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for logro in logros:
                    <tr>
                        <td>{{logro['id']}}</td>
                        <td>{{logro['id_icono']}}</td>
                        <td>{{logro['descripcion']}}</td>
                        <td>{{logro['fecha']}}</td>
                        <td>{{logro['puntos_requeridos']}}</td>
                        <td>{{logro['puntos_logro']}}</td>
                        <td>
                            <a class="btn btn_primary" href = "/xpd_sistema_puntos/logros/{{logro['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>    

% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
