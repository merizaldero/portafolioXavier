% include('xpd_alicuotas/encabezado.tpl', titulo="Datos de EventoLimpezaAlicuota", usuario = usuario, estilo = "")
% if lvl != "" :
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end
<form method="POST" enctype="multipart/form-data">
    <div class="row">
        <label class="col form-label" for="id_alicuota">
        Seleccionar Al&iacute;cuota pendiente:
        </label>
    </div>
    <table class="mt-2 table table-striped">
        <thead>
            <tr>

                <th>
                    
                </th>

                <th>
                    Anio / Mes
                </th>

                <th>
                    Monto
                </th>

                <th>
                    Observaciones
                </th>
            </tr>
        </thead>
        <tbody>
% for indice, alicuota in enumerate(alicuotas):
            <tr>
                <td><input type="radio" name="id_alicuota" value="{{alicuota['id']}}"></td>
                <td>{{alicuota['anio']}} / {{alicuota['mes']}}</td>
                <td>{{alicuota['monto']}}</td>
                <td>{{alicuota['observaciones']}}</td>
            </tr>
% end
        </tbody>
    </table>

    <div class="mt-5 d-flex flex-row justify-content-around border-top border-bottom pt-1 pb-1">
        <a class="btn btn-secondary" href="{{ruta_cancelar}}">
            Cancelar
        </a>
        <input type="submit" value="Guardar" class="btn btn-primary">
    </div>
</form>
% include('xpd_alicuotas/pie.tpl', usuario = usuario)
