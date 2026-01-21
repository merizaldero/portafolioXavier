% include('xpd_health/encabezado.tpl', titulo="Datos de LecturaGlucosa", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="fecha_hora">
    fecha_hora*:
    </label>

    <span class="col">
        <input class="form-control" type="datetime-local" name="fecha_hora" value="{{fecha_iso_to_js(objeto['fecha_hora'])}}" >
    </span>

</div>

<div class="row">
    <label class="col form-label" for="valor">
    valor*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="valor" value="{{objeto['valor']}}" maxlength="6">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="observacion">
    observacion:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="observacion" value="{{des_convertir_acentos(objeto['observacion'])}}" maxlength="256">
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
