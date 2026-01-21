% include('xpd_health/encabezado.tpl', titulo="Sujeto", usuario = usuario, estilo = "")

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
        nombre:
    </span>
    <span class="col">
        {{objeto['nombre']}}
    </span>
</div>

<div class="row">
    <span class="col">
        umbral_maximo:
    </span>
    <span class="col">
        {{objeto['umbral_maximo']}}
    </span>
</div>

<div class="row">
    <span class="col">
        umbral_minimo:
    </span>
    <span class="col">
        {{objeto['umbral_minimo']}}
    </span>
</div>

<div class="row">
    <span class="col">
        fecha_update:
    </span>
    <span class="col">
        {{objeto['fecha_update']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary btn-sm" href="/xpd_health/sujetos">
            Volver
        </a>
        <a class="btn btn-primary btn-sm" href="/xpd_health/sujetos/{{objeto['id']}}/editar">
            Editar
        </a>
    </div>

    <ul class="mt-3 nav nav-tabs nav-justified">

        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#divGrafica">Resumen</a>
        </li>

        <li class="nav-item">
            <a class="nav-link" data-bs-toggle="tab" href="#divLecturaGlucosas">Lecturas Glucosa ({{len(lecturaglucosas)}})</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divDosisInsulinas">Dosis Insulina ({{len(dosisinsulinas)}})</a>
        </li>

    </ul>

    <div class="tab-content">    

        <div class="tab-pane container active" id="divGrafica">
            <img id="img_resumen" src="/static/img/cargando.png" class="img-fluid">
            
            <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
                <a class="btn btn-primary btn-sm" href="/xpd_health/sujetos/{{objeto['id']}}/nuevolecturaglucosa">Registrar Glucosa</a>
                <a class="btn btn-primary btn-sm" href="/xpd_health/sujetos/{{objeto['id']}}/nuevodosisinsulina">Registrar Insulina</a>
            </div>

        </div>

        <div class="tab-pane container" id="divLecturaGlucosas">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Fecha_hora
                        </th>

                        <th>
                            Valor
                        </th>

                        <th>
                            Observacion
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_health/sujetos/{{objeto['id']}}/nuevolecturaglucosa">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(lecturaglucosas) == 0:
                    <tr>
                        <td colspan="4">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for lecturaglucosa in lecturaglucosas:
                    <tr class="small">
                        <td>{{lecturaglucosa['id']}}</td>
                        <td>{{lecturaglucosa['fecha_hora']}}</td>
                        <td>{{lecturaglucosa['valor']}}</td>
                        <td>{{lecturaglucosa['observacion']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_health/lecturaglucosas/{{lecturaglucosa['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divDosisInsulinas">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Fecha_hora
                        </th>

                        <th>
                            Unidades_aplicadas
                        </th>

                        <th>
                            Observacion
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_health/sujetos/{{objeto['id']}}/nuevodosisinsulina">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(dosisinsulinas) == 0:
                    <tr>
                        <td colspan="4">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for dosisinsulina in dosisinsulinas:
                    <tr class="small">
                        <td>{{dosisinsulina['id']}}</td>
                        <td>{{dosisinsulina['fecha_hora']}}</td>
                        <td>{{dosisinsulina['unidades_aplicadas']}}</td>
                        <td>{{dosisinsulina['observacion']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_health/dosisinsulinas/{{dosisinsulina['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>
<script>

window.addEventListener('load', (event) => {
    const img_resumen = document.getElementById("img_resumen");
    const marca_tiempo = (new Date()).getTime();
    img_resumen.src="/xpd_health/sujetos/{{objeto['id']}}/resumen.png?" + marca_tiempo;
});

</script>

% include('xpd_health/pie.tpl', usuario = usuario)
