% include('xpd_health/encabezado.tpl', titulo="Sujetos", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>
        <th>Nombre</th>
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
            {{objeto['nombre']}}
        </td>
        <td>
            <a class="btn btn-primary" href="/xpd_health/sujetos/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_health/pie.tpl', usuario = usuario)
