% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de Condominio", usuario = usuario, estilo = "")
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
        <input class="form-control" type="text" name="nombre" value="{{objeto['nombre']}}" maxlength="64">
    </span>

</div>

<div class="row">
    <label class="col form-label" for="saldo">
    saldo*:
    </label>

<span class="col">
% if 'id' in objeto and objeto['id'] is not None:
        {{"{0:.2f}".format(objeto['saldo'])}}
% else:
        <input class="form-control" type="number" name="saldo" value="{{objeto['saldo']}}" maxlength="9">
% end
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
