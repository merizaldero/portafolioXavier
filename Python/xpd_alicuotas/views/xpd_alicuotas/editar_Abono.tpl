% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Abono", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">

<div class="row">
    <label class="col form-label" for="fecha">
    Fecha *:
    </label>

    <span class="col">
% if 'id' in objeto and objeto['id'] is not None:
        {{fecha_iso_to_js(objeto['fecha'])}}
% else:
        <input class="form-control" type="date" name="fecha" value="{{fecha_iso_to_js(objeto['fecha'])}}" >
% end
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto">
    Monto *:
    </label>

<span class="col">
% if 'id' in objeto and objeto['id'] is not None:
        {{objeto['monto']}}
% else:
        <input class="form-control" type="number" step="0.01" name="monto" value="{{objeto['monto']}}" maxlength="5">
% end
    </span>

</div>

<div class="row">
    <label class="col form-label" for="monto_aprobado">
    Monto Aprobado *:
    </label>

<span class="col">
        <input class="form-control" type="number" step="0.01" name="monto_aprobado" value="{{objeto['monto_aprobado']}}" maxlength="5">
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
    Genera Egreso*:
    </label>

    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="genera_egreso" value="1"
% if objeto['genera_egreso'] in ['1', True]:
        checked
% end
        >
    </span>

</div>

<div class="row">
    <label class="col form-label" for="aplicado">
    Aplicado *:
    </label>

    <span class="col">
        <input class="form-check form-switch" type="checkbox" name="aplicado" value="1"
% if objeto['aplicado'] in ['1', True]:
        checked
% end        
        >
    </span>

</div>


    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
% if objeto['id'] is None or objeto['aplicado'] == '0':
        <input type="submit" value="Guardar" class="btn btn-primary">
% end
    </div>
</form>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
