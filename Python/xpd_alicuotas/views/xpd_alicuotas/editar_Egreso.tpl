% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Egreso", usuario = usuario, estilo = "")
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
    <label class="col form-label" for="destino">
    destino*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="destino" value="{{objeto['destino']}}" maxlength="128">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto">
    monto*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto" value="{{objeto['monto']}}" maxlength="6">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="observaciones">
    observaciones*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="observaciones" value="{{objeto['observaciones']}}" maxlength="256">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="anulado">
    anulado*:
    </label>

    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="anulado" value="1">
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
