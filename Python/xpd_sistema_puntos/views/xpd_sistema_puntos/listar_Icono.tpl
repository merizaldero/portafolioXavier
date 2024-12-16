% include('xpd_sistema_puntos/encabezado.tpl', titulo="Iconos", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Icono</th>
        <th>Orden</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/iconos/nuevo">Crear Nuevo</a>
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
            {{objeto['icono']}}
        </td>
        <td>
            {{objeto['orden']}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/iconos/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
