% include('xpd_sistema_puntos/encabezado.tpl', titulo="PlantillaTransaccion", usuario = usuario, estilo = "")

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
        descripcion:
    </span>
    <span class="col">
        {{objeto['descripcion']}}
    </span>
</div>

<div class="row">
    <span class="col">
        puntos:
    </span>
    <span class="col">
        {{objeto['puntos']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_sistema_puntos/plantillatransaccions">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_sistema_puntos/plantillatransaccions/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_sistema_puntos/plantillatransaccions/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

% include('xpd_sistema_puntos/pie.tpl', usuario = usuario)