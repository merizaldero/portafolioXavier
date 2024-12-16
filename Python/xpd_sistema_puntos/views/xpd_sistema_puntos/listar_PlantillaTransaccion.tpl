% include('xpd_sistema_puntos/encabezado.tpl', titulo="PlantillaTransaccions", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Descripcion</th>
        <th>Puntos</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/plantillatransaccions/nuevo">Crear Nuevo</a>
        </th>
    </tr>
    </thead>
    <tbody>
% if len(lista) == 0:
    <tr>
    <td colspan = "3">No se ha encontrado registros</td>
    </tr>
% end
% for objeto in lista:
    <tr>
        <td>
            {{objeto['id']}}
        </td>
        <td>
            {{objeto['descripcion']}}
        </td>
        <td>
            {{objeto['puntos']}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/plantillatransaccions/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
