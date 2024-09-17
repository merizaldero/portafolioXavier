<div class="wrap">
    <h1 class="wp-heading-inline">Taller de Entidades</h1>
    <button id="xpdwf_btn_reset" class="page-title-action">Comenzar de Nuevo</button>
    <hr>    
    <table class="form-table">
        <tbody>
            <tr class="form-field form-required">
                <th scope="row">
                    <label for="nombreTabla">Nombre de Tabla:</label>
                </th>
                <td>
                    <input type="text" name="nombreTabla" id="xpdwf_txt_nombreTabla">
                </td>
            </tr>
        </tbody>
    </table>
    <hr>
    <div class="tablenav top">
        <div class="alignleft actions bulkactions">
            <h2 class="wp-heading-inline">Campos</h2>
            <select id="xpdwf_sel_accion_propiedades">
                <option value="-1">Acciones en lote</option>
                <option value="eliminar">Eliminar Seleccionados</option>
            </select>
            <button id="xpdwf_btn_accion_propiedades" class="button action">Aplicar</button>
        </div>
    </div>
    <table class="wp-list-table widefat fixed striped table-view-list pages">
        <thead>
            <tr>
                <td class="manage-column check-column">
                    <input type="checkbox" id="xpdwf_chk_all_propiedades_1">
                </td>
                <th scope="col" class="manage-column">Nombre</th>
                <th scope="col" class="manage-column">Nombre Campo</th>
                <th scope="col" class="manage-column">Tipo</th>
                <th scope="col" class="manage-column">Tama&ntilde;o</th>
                <th scope="col" class="manage-column">Precisi&oacute;n</th>
                <th scope="col" class="manage-column">C. Primaria</th>
                <th scope="col" class="manage-column">Actualizacion</th>
                <td scope="col" class="manage-column"><i>Acciones</i></td>
                <td scope="col" class="manage-column"><i>Mover</i></td>
            </tr>
        </thead>
        <tbody id="xpdwf_tbody_propiedades"></tbody>
        <tbody>
            <tr>
                <td></td>
                <td><input type="text" id="xpdwf_txt_nuevapropiedad_nombre" size="10"></td>
                <td><input type="text" id="xpdwf_txt_nuevapropiedad_nombreCampo" size="10"></td>
                <td>
                    <select id="xpdwf_sel_nuevapropiedad_tipo">
                        <option value="XPDSTRING">String</option>
                        <option value="XPDINTEGER">Integer</option>
                        <option value="XPDREAL">Real</option>
                        <option value="XPDBOOLEAN">Boolean</option>
                        <option value="XPDDATE">Date</option>                        
                    </select>
                </td>
                <td><input type="text" id="xpdwf_txt_nuevapropiedad_tamano" size="5" maxlength="5"></td>
                <td><input type="text" id="xpdwf_txt_nuevapropiedad_precision" size="2" maxlength="1"></td>
                <td>
                    <input type="checkbox" id="xpdwf_chk_nuevapropiedad_pk" value="1">
                    Clave Primaria
                    <br>
                    <input type="checkbox" id="xpdwf_chk_nuevapropiedad_incremental" value="1">
                    Incremental
                </td>
                <td>
                    <input type="checkbox" id="xpdwf_chk_nuevapropiedad_insert" value="1">
                    Insertar
                    <br>
                    <input type="checkbox" id="xpdwf_chk_nuevapropiedad_update" value="1">
                    Actualizar
                </td>
                <td>
                    <a href="#" id="xpdwf_btn_nuevapropiedad_agregar">Agregar</a>
                </td>
                <td></td>
            </tr>
        </tbody>
    </table>
    <hr>
    <div class="tablenav top">
        <div class="alignleft actions bulkactions">
            <h2 class="wp-heading-inline">Named Queries</h2>
            <select id="xpdwf_sel_accion_namedqueries">
                <option value="-1">Acciones en lote</option>
                <option value="eliminar">Eliminar Seleccionados</option>
            </select>
            <button id="xpdwf_btn_accion_namedqueries" class="button action">Aplicar</button>
        </div>
    </div>
    <table class="wp-list-table widefat fixed striped table-view-list pages">
        <thead>
            <tr>
                <td class="manage-column check-column">
                    <input type="checkbox" id="xpdwf_chk_all_namedqueries_1">
                </td>
                <th scope="col" class="manage-column">Nombre</th>
                <th scope="col" class="manage-column">Where</th>
                <th scope="col" class="manage-column">Order By</th>
                <td scope="col" class="manage-column"><i>Acciones</i></td>
            </tr>
        </thead>
        <tbody id="xpdwf_tbody_namedqueries"></tbody>
        <tbody>
            <tr>
                <td></td>
                <td><input type="text" id="xpdwf_txt_nuevaquery_nombre"></td>
                <td><input type="text" id="xpdwf_txt_nuevaquery_where"></td>
                <td><input type="text" id="xpdwf_txt_nuevaquery_orderby"></td>
                <td>
                    <a href="#" id="xpdwf_btn_nuevaquery_agregar">Agregar</a>
                </td>
                <td></td>
            </tr>
        </tbody>
    </table>    
    <hr>
    <table class="form-table">
        <tbody>
            <tr>
                <th>
                    Notacion JSON:
                </th>
            </tr>
            <tr>
                <td>
                    <form target="_blank" method="POST" action="/wordpress/?rest_route=/xpdwpf/v1/metamodelo">
                    <textarea class="form-control" name="metamodelo" id="xpdwf_txt_metamodelo" class="form-label" rows="10" cols="80"></textarea>
                    <br>
                    <input class="button action" type="submit" value="Probar Api">
                    <a href="#" id="xpdwf_btn_generar" class="button action">Generar</a>
                    </form>
                </td>
            </tr>
        </tbody>
        <tbody id="xpdwf_div_resultado">
            <tr>
                <td>
                    <label class="form-label">Notacion PHP:</label>
                    <br>
                    <textarea class="form-control" id="xpdwf_txt_metamodelo_php" class="form-label" rows="10" cols="80"></textarea>
                </td>
            </tr>
            <tr>
                <td>
                    <label class="form-label">Create Table:</label>
                    <br>
                    <textarea class="form-control" id="xpdwf_txt_create_table" class="form-label" rows="10" cols="80"></textarea>            
                </td>            
            </tr>
        </tbody>
        <tbody id="xpdwf_div_queries">
        </tbody>
    </table>
</div>