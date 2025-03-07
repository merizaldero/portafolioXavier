% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Abono", usuario = usuario, estilo = "")
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
    <label class="col form-label" for="monto">
    monto*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto" value="{{objeto['monto']}}" maxlength="5">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto_aprobado">
    monto_aprobado*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto_aprobado" value="{{objeto['monto_aprobado']}}" maxlength="5">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto_por_aplicar">
    monto_por_aplicar*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto_por_aplicar" value="{{objeto['monto_por_aplicar']}}" maxlength="5">
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

<div class="row">
    <label class="col form-label" for="genera_egreso">
    genera_egreso*:
    </label>

    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="genera_egreso" value="1">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="aplicado">
    aplicado*:
    </label>

    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="aplicado" value="1">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="id_egreso">
    id_egreso:
    </label>

<span class="col">
        <input class="form-control" type="number" name="id_egreso" value="{{objeto['id_egreso']}}" maxlength="0">
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
