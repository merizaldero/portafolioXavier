% include('xpd_alicuotas/encabezado.tpl', titulo="Condominio", usuario = usuario, estilo = "")

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
        saldo:
    </span>
    <span class="col">
        {{objeto['saldo']}}
    </span>
</div>

    <div class="d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="/xpd_alicuotas/condominios">
            Volver
        </a>
        <a class="btn btn-primary" href="/xpd_alicuotas/condominios/{{objeto['id']}}/editar">
            Editar
        </a>
        <a class="btn btn-secondary" href="/xpd_alicuotas/condominios/{{objeto['id']}}/eliminar" onclick="return confirm('Desea proceder con eliminación?');">
            Eliminar
        </a>
    </div>

    <div class="card">
        <div class = "card-body d-flex justify-content-center">
            <img id="img_alicuotas" src="/static/graficas/alicuotas_{{objeto['id']}}.png">        
        </div>
        <div class = "card-footer d-flex justify-content-center">
            <button id="btn_refrescar_alicuotas" class="btn btn-secondary">Actualizar</button>
        </div>
    </div>

    <ul class="mt-3 nav nav-tabs nav-justified">

        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#divDepartamentos">Departamentos ({{len(departamentos)}})</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divTransaccions">Transaccions ({{len(transaccions)}})</a>
        </li>

        <li class="nav-item">
            <a class="nav-link " data-bs-toggle="tab" href="#divEgresos">Egresos ({{len(egresos)}})</a>
        </li>

    </ul>
    <div class="tab-content">    

        <div class="tab-pane container active" id="divDepartamentos">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Numero_dep
                        </th>

                        <th>
                            Propietario
                        </th>

                        <th>
                            Arrendatario
                        </th>

                        <th>
                            Saldo
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_alicuotas/condominios/{{objeto['id']}}/nuevodepartamento">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(departamentos) == 0:
                    <tr>
                        <td colspan="5">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for departamento in departamentos:
                    <tr class="small">
                        <td>{{departamento['id']}}</td>
                        <td>{{departamento['numero_dep']}}</td>
                        <td>{{departamento['propietario']}}</td>
                        <td>{{departamento['arrendatario']}}</td>
                        <td>{{departamento['saldo']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_alicuotas/departamentos/{{departamento['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divTransaccions">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Fecha
                        </th>

                        <th>
                            Concepto
                        </th>

                        <th>
                            Monto
                        </th>

                        <th>
                            Saldo_antes
                        </th>

                        <th>
                            Saldo_despues
                        </th>

                        <th>
                            Anulado
                        </th>

                        <th>
                            Id_abono
                        </th>

                        <th>
                            Id_egreso
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_alicuotas/condominios/{{objeto['id']}}/nuevotransaccion">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(transaccions) == 0:
                    <tr>
                        <td colspan="9">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for transaccion in transaccions:
                    <tr class="small">
                        <td>{{transaccion['id']}}</td>
                        <td>{{transaccion['fecha']}}</td>
                        <td>{{transaccion['concepto']}}</td>
                        <td>{{transaccion['monto']}}</td>
                        <td>{{transaccion['saldo_antes']}}</td>
                        <td>{{transaccion['saldo_despues']}}</td>
                        <td>{{transaccion['anulado']}}</td>
                        <td>{{transaccion['id_abono']}}</td>
                        <td>{{transaccion['id_egreso']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_alicuotas/transaccions/{{transaccion['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
        <div class="tab-pane container fade" id="divEgresos">
            <table class="mt-2 table table-striped small">
                <thead>
                    <tr class="small">

                        <th>
                            Id
                        </th>

                        <th>
                            Fecha
                        </th>

                        <th>
                            Destino
                        </th>

                        <th>
                            Monto
                        </th>

                        <th>
                            Observaciones
                        </th>

                        <th>
                            Anulado
                        </th>

                        <th>
                            <a class="btn btn-primary btn-sm" href="/xpd_alicuotas/condominios/{{objeto['id']}}/nuevoegreso">Crear Nuevo</a>
                        </th>
                    </tr>
                </thead>
                <tbody>
% if len(egresos) == 0:
                    <tr>
                        <td colspan="6">
                            No hay registros disponibles
                        </td>
                    </tr>
% end
% for egreso in egresos:
                    <tr class="small">
                        <td>{{egreso['id']}}</td>
                        <td>{{egreso['fecha']}}</td>
                        <td>{{egreso['destino']}}</td>
                        <td>{{egreso['monto']}}</td>
                        <td>{{egreso['observaciones']}}</td>
                        <td>{{egreso['anulado']}}</td>
                        <td>
                            <a class="btn btn-primary btn-sm" href = "/xpd_alicuotas/egresos/{{egreso['id']}}">Mostrar</a>
                        </td>
                    </tr>
% end
                </tbody>
            </table>
        </div>
    </div>    
<script lang="javascript">
    const btn_refrescar_alicuotas = document.getElementById("btn_refrescar_alicuotas");
    
    btn_refrescar_alicuotas.addEventListener("click", async (event) => {
        const img_alicuotas = document.getElementById("img_alicuotas");
        respuesta = await fetch("/xpd_alicuotas/condominios/{{objeto['id']}}/graficar");
        img_alicuotas.src = "/static/graficas/alicuotas_{{objeto['id']}}.png?" + Date.now()

    });
</script>

% include('xpd_alicuotas/pie.tpl', usuario = usuario)
