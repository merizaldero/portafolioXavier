% include('xpd_health/encabezado.tpl', titulo="Sujetos", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Nombre</th>
        <th>Umbral_maximo</th>
        <th>Umbral_minimo</th>
        <th>Fecha_update</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_health/sujetos/nuevo">Crear Nuevo</a>
        </th>
    </tr>
    </thead>
    <tbody>
% if len(lista) == 0:
    <tr>
    <td colspan = "5">No se ha encontrado registros</td>
    </tr>
% end
% for objeto in lista:
    <tr>
        <td>
            {{objeto['id']}}
        </td>
        <td>
            {{objeto['nombre']}}
        </td>
        <td>
            {{objeto['umbral_maximo']}}
        </td>
        <td>
            {{objeto['umbral_minimo']}}
        </td>
        <td>
            {{objeto['fecha_update']}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_health/sujetos/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_health/pie.tpl', usuario = usuario)
