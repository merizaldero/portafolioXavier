% include('xpd_sistema_puntos/encabezado.tpl', titulo="Logro", usuario = usuario, estilo = "")

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
        id_icono:
    </span>
    <span class="col">
        {{objeto['id_icono']}}
    </span>
</div>

<div class="row">
    <span class="col">
        descripcion:
    </span>
    <span class="col">
        {{objeto['descripcion']}}
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
        puntos_requeridos:
    </span>
    <span class="col">
        {{objeto['puntos_requeridos']}}
    </span>
</div>

<div class="row">
    <span class="col">
        puntos_logro:
    </span>
    <span class="col">
        {{objeto['puntos_logro']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_sistema_puntos/evaluados/{{objeto['id_evaluado']}}">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_sistema_puntos/logros/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_sistema_puntos/logros/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)
