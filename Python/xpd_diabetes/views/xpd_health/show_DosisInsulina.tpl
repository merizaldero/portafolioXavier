% include('xpd_health/encabezado.tpl', titulo="DosisInsulina", usuario = usuario, estilo = "")

<div class="row">
    <span class="col">
        id:
    </span>
    <span class="col">
        {{objeto['id']}}
    </span>
</div>

<div class="row">
    <span class="col">
        fecha_hora:
    </span>
    <span class="col">
        {{objeto['fecha_hora']}}
    </span>
</div>

<div class="row">
    <span class="col">
        unidades_aplicadas:
    </span>
    <span class="col">
        {{objeto['unidades_aplicadas']}}
    </span>
</div>

<div class="row">
    <span class="col">
        observacion:
    </span>
    <span class="col">
        {{objeto['observacion']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_health/sujetos/{{objeto['id_sujeto']}}">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_health/dosisinsulinas/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_health/dosisinsulinas/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

% include('xpd_health/pie.tpl', usuario = usuario)
