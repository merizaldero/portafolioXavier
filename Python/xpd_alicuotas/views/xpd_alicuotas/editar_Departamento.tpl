% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Departamento", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="numero_dep">
    numero_dep*:
    </label>

<span class="col">
        <input class="form-control" type="number" name="numero_dep" value="{{objeto['numero_dep']}}" maxlength="0">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="propietario">
    propietario*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="propietario" value="{{objeto['propietario']}}" maxlength="64">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="arrendatario">
    arrendatario:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="arrendatario" value="{{objeto['arrendatario']}}" maxlength="64">
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
