% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de EventoLimpezaAlicuota", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="id_alicuota">
    id_alicuota*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="id_alicuota" value="{{objeto['id_alicuota']}}" maxlength="0">
    </span>

</div>

    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
