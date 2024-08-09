% include('xpdcobros/encabezado.tpl', titulo="XPD Cobros - Configuracion", usuario = usuario, estilo ="")
<div class="container">
    <h1>Configuraciones</h1>
    <div id="div_mensaje" class="collapse alert"></div>
    <table class="table table-striped">
% for item in configs:
        <tr>
            <td>{{item['descripcion']}}</td>
            <td>
                <input class="form-control config-input" type="text" data-id_config="{{item['id']}}" value="{{item['valor']}}">
            </td>
        </tr>
% end
    </table>
</div>
<script src="/static/js/config.js"></script>
% include('xpdcobros/pie.tpl', usuario = usuario)