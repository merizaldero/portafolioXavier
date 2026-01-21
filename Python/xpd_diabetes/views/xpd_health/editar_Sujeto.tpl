% include('xpd_health/encabezado.tpl', titulo="Datos de Sujeto", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="nombre">
    nombre*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="nombre" value="{{des_convertir_acentos(objeto['nombre'])}}" maxlength="128">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="umbral_maximo">
    umbral_maximo*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="umbral_maximo" value="{{objeto['umbral_maximo']}}" maxlength="6">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="umbral_minimo">
    umbral_minimo*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="umbral_minimo" value="{{objeto['umbral_minimo']}}" maxlength="6">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="fecha_update">
    fecha_update*:
    </label>

    <span class="col">
        <input class="form-control" type="datetime-local" name="fecha_update" value="{{fecha_iso_to_js(objeto['fecha_update'])}}" >
    </span>

</div>

    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('xpd_health/pie.tpl', usuario = usuario)
