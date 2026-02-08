% include('xpd_alicuotas/encabezado.tpl', titulo="Generar Alicuota Masiva", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label">
    Condominio :
    </label>

    <span class="col">
        {{objeto['nombre']}}        
    </span>

</div>

<div class="row">
    <label class="col form-label" for="anio_alicuota">
    A&nacute;o *:
    </label>

    <span class="col">
        <input class="form-control" type="number" name="anio_alicuota" value="{{objeto['anio_alicuota']}}" maxlength="4">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="mes_alicuota">
    Mes *:
    </label>

<span class="col">
        <input class="form-control" type="number" name="mes_alicuota" value="{{objeto['mes_alicuota']}}" maxlength="2">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto_alicuota">
    Monto *:
    </label>

<span class="col">
        <input class="form-control" type="number" step="0.01" name="monto_alicuota" value="{{objeto['monto_alicuota']}}" maxlength="5">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="observaciones_alicuota">
    observaciones*:
    </label>

    <span class="col">
        <input class="form-control" type="text" name="observaciones_alicuota" value="{{objeto['observaciones_alicuota']}}" maxlength="256">
    </span>

</div>

<div class="row">
    <label class="col" for="observaciones_alicuota">
    Aplicar a los siguientes departamentos:
    </label>
</div>

% for departamento in departamentos:
<div class="row">
    <span class="col-1 form-check">
        <input class="form-check-input" type="checkbox" name="ids_departamento" value="{{departamento['id']}}"
% if departamento['seleccionado'] == True:
            checked
% end
        >
    </span>
    <span class="col-11 form-check-label">
        Dep {{departamento['numero_dep']}} - {{departamento['propietario']}}
    </span>
</div>
% end

    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
