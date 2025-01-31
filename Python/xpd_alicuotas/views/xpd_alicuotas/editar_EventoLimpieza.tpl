% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de EventoLimpieza", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="fecha">
    fecha*:
    </label>

    <span class="col">
        <input class="form-control" type="date" name="fecha" value="{{fecha_iso_to_js(objeto['fecha'])}}" >
    </span>

</div>

<div class="row">
    <label class="col form-label" for="fecha_validacion">
    fecha_validacion:
    </label>

    <span class="col">
        <input class="form-control" type="date" name="fecha_validacion" value="{{fecha_iso_to_js(objeto['fecha_validacion'])}}" >
    </span>

</div>

<div class="row">
    <label class="col form-label" for="observacion">
    observacion:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="observacion" value="{{objeto['observacion']}}" maxlength="256">
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
