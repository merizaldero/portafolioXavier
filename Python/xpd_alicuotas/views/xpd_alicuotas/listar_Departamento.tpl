% include('xpd_alicuotas/encabezado.tpl', titulo="Departamentos", usuario = usuario, estilo = "")
<table class="table table-striped">
    <thead>
    <tr>        <th>Id</th>
        <th>Numero_dep</th>
        <th>Propietario</th>
        <th>Arrendatario</th>

        <th>Mover</th>
        <th>
            <a class="btn btn-primary" href="/xpd_alicuotas/departamentos/nuevo">Crear Nuevo</a>
        </th>
    </tr>
    </thead>
    <tbody>
% if len(lista) == 0:
    <tr>
    <td colspan = "4">No se ha encontrado registros</td>
    </tr>
% end
% for objeto in lista:
    <tr>
        <td>
            {{objeto['id']}}
        </td>
        <td>
            {{objeto['numero_dep']}}
        </td>
        <td>
            {{objeto['propietario']}}
        </td>
        <td>
            {{objeto['arrendatario']}}
        </td>
        <td></td>
        <td>
            <a class="btn btn-primary" href="/xpd_alicuotas/departamentos/{{objeto['id']}}">Mostrar</a>
        </td>
    </tr>
% end
    </tbody>
</table>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
