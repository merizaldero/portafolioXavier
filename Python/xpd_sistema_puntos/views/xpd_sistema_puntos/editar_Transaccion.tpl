% include('xpd_sistema_puntos/encabezado.tpl', titulo="Datos de Transaccion", usuario = usuario, estilo = "")
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
        <input class="form-control" type="datetime-local" name="fecha" value="{{fecha_iso_to_js(objeto['fecha'])}}" >
    </span>

</div>

<div class="row">
    <label class="col form-label" for="id_icono">
    id_icono:
    </label>

<span class="col">
        <input class="form-control" type="number" name="id_icono" value="{{objeto['id_icono']}}" maxlength="0">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="descripcion">
    descripcion*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="descripcion" value="{{objeto['descripcion']}}" maxlength="128">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto">
    monto*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="monto" value="{{objeto['monto']}}" maxlength="0">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="saldo">
    saldo*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="saldo" value="{{objeto['saldo']}}" maxlength="0">
    </span>

</div>

    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
