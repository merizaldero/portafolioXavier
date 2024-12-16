% include('xpd_sistema_puntos/encabezado.tpl', titulo="Evaluados", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Nombre</th>
        <th>Id_icono</th>
        <th>Saldo</th>
        <th>Orden</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/evaluados/nuevo">Crear Nuevo</a>
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
            {{objeto['id_icono']}}
        </td>
        <td>
            {{objeto['saldo']}}
        </td>
        <td>
            {{objeto['orden']}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/evaluados/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
