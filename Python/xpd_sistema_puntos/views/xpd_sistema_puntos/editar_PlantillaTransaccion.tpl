% include('xpd_sistema_puntos/encabezado.tpl', titulo="Datos de PlantillaTransaccion", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="descripcion">
    descripcion*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="descripcion" value="{{objeto['descripcion']}}" maxlength="256">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="puntos">
    puntos*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="puntos" value="{{objeto['puntos']}}" maxlength="0">
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
