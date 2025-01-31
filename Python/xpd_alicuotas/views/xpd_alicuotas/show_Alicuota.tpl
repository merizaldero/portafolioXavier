% include('xpd_alicuotas/encabezado.tpl', titulo="Alicuota", usuario = usuario, estilo = "")

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
        anio:
    </span>
    <span class="col">
        {{objeto['anio']}}
    </span>
</div>

<div class="row">
    <span class="col">
        mes:
    </span>
    <span class="col">
        {{objeto['mes']}}
    </span>
</div>

<div class="row">
    <span class="col">
        monto:
    </span>
    <span class="col">
        {{objeto['monto']}}
    </span>
</div>

<div class="row">
    <span class="col">
        monto_pendiente:
    </span>
    <span class="col">
        {{objeto['monto_pendiente']}}
    </span>
</div>

<div class="row">
    <span class="col">
        pagado:
    </span>
    <span class="col">
        {{objeto['pagado']}}
    </span>
</div>

<div class="row">
    <span class="col">
        observaciones:
    </span>
    <span class="col">
        {{objeto['observaciones']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/departamentos/{{objeto['id_departamento']}}">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_alicuotas/alicuotas/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/alicuotas/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
