% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Alicuota", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="anio">
    anio*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="anio" value="{{objeto['anio']}}" maxlength="4">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="mes">
    mes*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="mes" value="{{objeto['mes']}}" maxlength="2">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto">
    monto*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto" value="{{objeto['monto']}}" maxlength="5">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto_pendiente">
    monto_pendiente*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto_pendiente" value="{{objeto['monto_pendiente']}}" maxlength="5">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="pagado">
    pagado*:
    </label>

    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="pagado" value="1">
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

    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
