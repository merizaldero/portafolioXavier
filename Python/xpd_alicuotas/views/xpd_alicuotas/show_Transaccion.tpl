% include('xpd_alicuotas/encabezado.tpl', titulo="Transaccion", usuario = usuario, estilo = "")

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
        fecha:
    </span>
    <span class="col">
        {{objeto['fecha']}}
    </span>
</div>

<div class="row">
    <span class="col">
        concepto:
    </span>
    <span class="col">
        {{objeto['concepto']}}
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
        saldo_antes:
    </span>
    <span class="col">
        {{objeto['saldo_antes']}}
    </span>
</div>

<div class="row">
    <span class="col">
        saldo_despues:
    </span>
    <span class="col">
        {{objeto['saldo_despues']}}
    </span>
</div>

<div class="row">
    <span class="col">
        anulado:
    </span>
    <span class="col">
        {{objeto['anulado']}}
    </span>
</div>

<div class="row">
    <span class="col">
        id_abono:
    </span>
    <span class="col">
        {{objeto['id_abono']}}
    </span>
</div>

<div class="row">
    <span class="col">
        id_egreso:
    </span>
    <span class="col">
        {{objeto['id_egreso']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/condominios/{{objeto['id_condominio']}}">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_alicuotas/transaccions/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/transaccions/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
