% include('xpd_sistema_puntos/encabezado.tpl', titulo="Premios", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Id_icono</th>
        <th>Descripcion</th>
        <th>Puntos_requeridos</th>
        <th>Puntos_logro</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/premios/nuevo">Crear Nuevo</a>
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
            {{objeto['id_icono']}}
        </td>
        <td>
            {{objeto['descripcion']}}
        </td>
        <td>
            {{objeto['puntos_requeridos']}}
        </td>
        <td>
            {{objeto['puntos_logro']}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_sistema_puntos/premios/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
