% include('xpd_alicuotas/encabezado.tpl', titulo="Condominio", usuario = usuario, estilo = "")

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

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/condominios">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_alicuotas/condominios/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/condominios/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

    <ul class="mt-3 nav nav-tabs nav-justified">

        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#divDepartamentos">Departamentos</a>
        </li>

    </ul>
    <div class="tab-content">    

        <div class="tab-pane container active" id="divDepartamentos">
            <table class="mt-2 table table-striped">
                <thead>
                    <tr>

                        <th>
                            Id
                        </th>

                        <th>
                            Numero_dep
                        </th>

                        <th>
                            Propietario
                        </th>

                        <th>
                            Arrendatario
                        </th>

                        <th>
                            <a class="btn btn-primary" href="/xpd_alicuotas/condominios/{{objeto['id']}}/nuevodepartamento">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(departamentos) == 0:
                    <tr>
                        <td colspan="4">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for departamento in departamentos:
                    <tr>
                        <td>{{departamento['id']}}</td>
                        <td>{{departamento['numero_dep']}}</td>
                        <td>{{departamento['propietario']}}</td>
                        <td>{{departamento['arrendatario']}}</td>
                        <td>
                            <a class="btn btn-primary" href = "/xpd_alicuotas/departamentos/{{departamento['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>    

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
