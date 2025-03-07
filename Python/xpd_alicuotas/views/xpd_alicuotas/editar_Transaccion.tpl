% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Transaccion", usuario = usuario, estilo = "")
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
    <label class="col form-label" for="concepto">
    concepto*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="concepto" value="{{objeto['concepto']}}" maxlength="256">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto">
    monto*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto" value="{{objeto['monto']}}" maxlength="7">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="saldo_antes">
    saldo_antes*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="saldo_antes" value="{{objeto['saldo_antes']}}" maxlength="6">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="saldo_despues">
    saldo_despues*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="saldo_despues" value="{{objeto['saldo_despues']}}" maxlength="6">
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

<div class="row">
    <label class="col form-label" for="id_abono">
    id_abono:
    </label>

<span class="col">
        <input class="form-control" type="number" name="id_abono" value="{{objeto['id_abono']}}" maxlength="0">
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
