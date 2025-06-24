% include('xpd_alicuotas/encabezado.tpl', titulo="Condominios", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Nombre</th>
        <th>Saldo</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_alicuotas/condominios/nuevo">Crear Nuevo</a>
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
            {{objeto['nombre']}}
        </td>
        <td>
            {{"{0:0.2f}".format(objeto['saldo'])}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_alicuotas/condominios/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
