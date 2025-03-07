% include('xpd_alicuotas/encabezado.tpl', titulo="EventoLimpezaAlicuota", usuario = usuario, estilo = "")

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
        id_alicuota:
    </span>
    <span class="col">
        {{objeto['id_alicuota']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/abonos/{{objeto['id_abono']}}">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_alicuotas/eventolimpezaalicuotas/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/eventolimpezaalicuotas/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
