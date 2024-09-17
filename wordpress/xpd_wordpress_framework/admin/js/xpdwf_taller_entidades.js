//document.addEventListener('load',(event)=>{
//    alert('iniciando scripting');
    const xpdwf_btn_reset = document.getElementById("xpdwf_btn_reset");
    const xpdwf_txt_nombreTabla = document.getElementById("xpdwf_txt_nombreTabla");
    
    const xpdwf_sel_accion_propiedades = document.getElementById("xpdwf_sel_accion_propiedades");
    const xpdwf_btn_accion_propiedades = document.getElementById("xpdwf_btn_accion_propiedades");
    const xpdwf_chk_all_propiedades_1 = document.getElementById("xpdwf_chk_all_propiedades_1");
    const xpdwf_tbody_propiedades = document.getElementById("xpdwf_tbody_propiedades");

    const xpdwf_txt_nuevapropiedad_nombre = document.getElementById("xpdwf_txt_nuevapropiedad_nombre");
    const xpdwf_txt_nuevapropiedad_nombreCampo = document.getElementById("xpdwf_txt_nuevapropiedad_nombreCampo");
    const xpdwf_sel_nuevapropiedad_tipo = document.getElementById("xpdwf_sel_nuevapropiedad_tipo");
    const xpdwf_txt_nuevapropiedad_tamano = document.getElementById("xpdwf_txt_nuevapropiedad_tamano");
    const xpdwf_txt_nuevapropiedad_precision = document.getElementById("xpdwf_txt_nuevapropiedad_precision");
    const xpdwf_chk_nuevapropiedad_pk = document.getElementById("xpdwf_chk_nuevapropiedad_pk");
    const xpdwf_chk_nuevapropiedad_incremental = document.getElementById("xpdwf_chk_nuevapropiedad_incremental");
    const xpdwf_chk_nuevapropiedad_insert = document.getElementById("xpdwf_chk_nuevapropiedad_insert");
    const xpdwf_chk_nuevapropiedad_update = document.getElementById("xpdwf_chk_nuevapropiedad_update");
    const xpdwf_btn_nuevapropiedad_agregar = document.getElementById("xpdwf_btn_nuevapropiedad_agregar");

    const xpdwf_sel_accion_namedqueries = document.getElementById("xpdwf_sel_accion_namedqueries");
    const xpdwf_btn_accion_namedqueries = document.getElementById("xpdwf_btn_accion_namedqueries");
    const xpdwf_chk_all_namedqueries_1 = document.getElementById("xpdwf_chk_all_namedqueries_1");
    const xpdwf_tbody_namedqueries = document.getElementById("xpdwf_tbody_namedqueries");

    const xpdwf_txt_nuevaquery_nombre = document.getElementById("xpdwf_txt_nuevaquery_nombre");
    const xpdwf_txt_nuevaquery_where = document.getElementById("xpdwf_txt_nuevaquery_where");
    const xpdwf_txt_nuevaquery_orderby = document.getElementById("xpdwf_txt_nuevaquery_orderby");
    const xpdwf_btn_nuevaquery_agregar = document.getElementById("xpdwf_btn_nuevaquery_agregar");

    const xpdwf_txt_metamodelo = document.getElementById('xpdwf_txt_metamodelo');
    const xpdwf_btn_generar = document.getElementById('xpdwf_btn_generar');
    const xpdwf_div_resultado = document.getElementById('xpdwf_div_resultado');
    const xpdwf_txt_metamodelo_php = document.getElementById('xpdwf_txt_metamodelo_php');
    const xpdwf_txt_create_table = document.getElementById('xpdwf_txt_create_table');
    const xpdwf_div_queries = document.getElementById('xpdwf_div_queries');

    xpdwf_btn_generar.addEventListener('click', ()=>{
        const metamodelo_x = xpdwf_txt_metamodelo.value;
        try{
            JSON.parse(metamodelo_x);
        }catch(ex){
            alert ("La entrada no puede parsearse a JSON\n" + ex.toString());
            return;
        }
        const formdata = new FormData();
        formdata.append('metamodelo',metamodelo_x);
        fetch('/wordpress/?rest_route=/xpdwpf/v1/metamodelo',{method:'POST', body:formdata}).then( (respuesta)=>{
            if(respuesta.status != 200){ 
                alert("Se ha producido un error en la petición a la API " + respuesta.status);
                xpdwf_div_resultado.classList.add('collapse');
                xpdwf_div_queries.classList.add('collapse');
                return;
            }
            respuesta.json().then( (resultado_obj)=>{
                xpdwf_txt_metamodelo_php.value = resultado_obj.metamodelo_php;
                xpdwf_txt_create_table.value = resultado_obj.create_statement;
                xpdwf_div_resultado.classList.remove('collapse');
                xpdwf_div_queries.innerHTML = "";
                resultado_obj.namedQueries.forEach( namedQuery => {
                    const tr_nodo = document.createElement("tr");
                    const td_nodo = document.createElement("td");
                    tr_nodo.appendChild(td_nodo);
                    const lbl_label = document.createElement('label');
                    lbl_label.classList.add('form-label');
                    lbl_label.innerText = namedQuery.nombre;
                    td_nodo.appendChild(lbl_label);
                    const txt_textarea = document.createElement('textarea');
                    txt_textarea.cols = 80;
                    txt_textarea.rows = 10;
                    txt_textarea.value = namedQuery.sql;
                    td_nodo.appendChild(document.createElement("br"));                    
                    td_nodo.appendChild(txt_textarea);
                    xpdwf_div_queries.appendChild(tr_nodo);
                });
                xpdwf_div_queries.classList.remove('collapse');
            }).catch( (ex)=>{
                alert("Se ha producido un error al interpretar JSON " + ex);
                xpdwf_div_resultado.classList.add('collapse');
                xpdwf_div_queries.classList.add('collapse');
            } );
        }).catch( (ex)=>{
            alert("Se ha producido un error consultar el servicio " + ex);
            xpdwf_div_resultado.classList.add('collapse');
            xpdwf_div_queries.classList.add('collapse');
        });
    
        
    });

    const xpdwf_construir_metamodelo = ()=>{
        const resultado = { nombreTabla:xpdwf_txt_nombreTabla.value, propiedades:[],namedQueries:[] };
        const tr_propiedades = document.getElementsByClassName("tr-propiedad");
        let indice;
        for( indice = 0; indice < tr_propiedades.length; indice++ ){
            resultado.propiedades.push( JSON.parse(tr_propiedades[indice].dataset.objeto) );
        }
        const tr_namedqueries = document.getElementsByClassName("tr-namedquery");
        for( indice = 0; indice < tr_namedqueries.length; indice++ ){
            resultado.namedQueries.push( JSON.parse(tr_namedqueries[indice].dataset.objeto) );
        }
        xpdwf_txt_metamodelo.value = JSON.stringify(resultado);
    };

    xpdwf_txt_nombreTabla.addEventListener('change', (event)=>{
        xpdwf_txt_nombreTabla.value = xpdwf_txt_nombreTabla.value.trim().toUpperCase();
        xpdwf_txt_nombreTabla.value = xpdwf_txt_nombreTabla.value.replaceAll(' ', '_');
        if(xpdwf_txt_nombreTabla.value.length > 0){
            xpdwf_construir_metamodelo();
        }        
    });

    xpdwf_txt_nuevapropiedad_nombre.addEventListener('change', (event)=>{
        xpdwf_txt_nuevapropiedad_nombre.value = xpdwf_txt_nuevapropiedad_nombre.value.trim().toLowerCase();
        xpdwf_txt_nuevapropiedad_nombre.value = xpdwf_txt_nuevapropiedad_nombre.value.replaceAll(' ', '_');
        xpdwf_txt_nuevapropiedad_nombreCampo.value = xpdwf_txt_nuevapropiedad_nombre.value.toUpperCase();
    });

    xpdwf_txt_nuevapropiedad_nombreCampo.addEventListener('change', (event)=>{
        xpdwf_txt_nuevapropiedad_nombreCampo.value = xpdwf_txt_nuevapropiedad_nombreCampo.value.trim().toUpperCase();
        xpdwf_txt_nuevapropiedad_nombreCampo.value = xpdwf_txt_nuevapropiedad_nombreCampo.value.replaceAll(' ', '_');
    });

    xpdwf_btn_nuevapropiedad_agregar.addEventListener('click',(event)=>{
        const objeto = {nombre:xpdwf_txt_nuevapropiedad_nombre.value.trim(), nombreCampo:xpdwf_txt_nuevapropiedad_nombreCampo.value.trim(), tipo: xpdwf_sel_nuevapropiedad_tipo.value};
        if(objeto.nombre == ""){
            alert("Nombre Requerido");
            xpdwf_txt_nuevapropiedad_nombre.focus();
            return;
        }
        if(objeto.nombreCampo == ""){
            alert("Nombre de Campo Requerido");
            xpdwf_txt_nuevapropiedad_nombreCampo.focus();
            return;
        }
        // determina si requiere tamano
        if( ["XPDSTRING", "XPDREAL"].indexOf(objeto.tipo) >= 0 ){
            if(isNaN (xpdwf_txt_nuevapropiedad_tamano.value.trim())){
                alert("Tamaño Requerido");
                xpdwf_txt_nuevapropiedad_tamano.focus();
                return;
            }
            objeto.tamano = parseInt(xpdwf_txt_nuevapropiedad_tamano.value.trim(), 10);
            if(objeto.tamano <= 0){
                alert("Tamaño no válido");
                xpdwf_txt_nuevapropiedad_tamano.focus();
                return;
            }
        }
        if( objeto.tipo == "XPDREAL" ){
            if(isNaN (xpdwf_txt_nuevapropiedad_precision.value.trim())){
                alert("Precisión Requerida");
                xpdwf_txt_nuevapropiedad_precision.focus();
                return;
            }
            objeto.precision = parseInt(xpdwf_txt_nuevapropiedad_precision.value.trim(), 10);
            if(objeto.precision <= 0 || objeto.precision >= 10){
                alert("Precisión no válida");
                xpdwf_txt_nuevapropiedad_precision.focus();
                return;
            }
        }
        if(xpdwf_chk_nuevapropiedad_pk.checked){
            objeto.pk = true;
            if(xpdwf_chk_nuevapropiedad_incremental.checked){
                objeto.incremental = true;
            }
        }
        if(xpdwf_chk_nuevapropiedad_insert.checked){
            objeto.insert = true;
        }
        if(xpdwf_chk_nuevapropiedad_update.checked){
            objeto.update = true;
        }

        const fila = document.createElement('tr');
        fila.classList.add("tr-propiedad");
        fila.dataset.objeto = JSON.stringify(objeto);
        fila.dataset.nombre = objeto.nombre;

        let columna = document.createElement("td");
        const chk_fila = document.createElement("input");
        chk_fila.type = "checkbox";
        chk_fila.classList.add("chk-propiedad");
        chk_fila.dataset.nombre = objeto.nombre;
        columna.appendChild(chk_fila);
        fila.appendChild(columna);

        columna = document.createElement("td");
        columna.innerText = objeto.nombre;
        fila.appendChild(columna);

        columna = document.createElement("td");
        columna.innerText = objeto.nombreCampo;
        fila.appendChild(columna);
        
        columna = document.createElement("td");
        columna.innerText = objeto.tipo;
        fila.appendChild(columna);

        columna = document.createElement("td");
        if(objeto.tamano){
            columna.innerText = objeto.tamano;
        }
        fila.appendChild(columna);

        columna = document.createElement("td");
        if(objeto.precision){
            columna.innerText = objeto.precision;
        }
        fila.appendChild(columna);

        columna = document.createElement("td");
        columna.innerText = "";
        if(objeto.pk){
            columna.innerText += "Pk";
        }
        if(objeto.incremental){
            columna.innerText += " Incremental";
        }
        fila.appendChild(columna);

        columna = document.createElement("td");
        if(objeto.insert){
            columna.innerText += " Insert";
        }
        if(objeto.update){
            columna.innerText += " Update";
        }
        fila.appendChild(columna);

        columna = document.createElement("td");
        const btn_eliminar = document.createElement("a");
        btn_eliminar.href = "#";
        btn_eliminar.innerText = "Eliminar";
        columna.appendChild(btn_eliminar);
        fila.appendChild(columna);

        xpdwf_tbody_propiedades.appendChild(fila);
        btn_eliminar.addEventListener('click', ()=>{
            xpdwf_tbody_propiedades.removeChild(fila);
        });

        xpdwf_txt_nuevapropiedad_nombre.value = "";
        xpdwf_txt_nuevapropiedad_nombreCampo.value = "";
        xpdwf_txt_nuevapropiedad_tamano.value = "";
        xpdwf_txt_nuevapropiedad_precision.value = "";
        xpdwf_txt_nuevapropiedad_tamano.value = "";
        xpdwf_chk_nuevapropiedad_pk.checked = false;        
        xpdwf_chk_nuevapropiedad_incremental.checked = false;
        xpdwf_construir_metamodelo();
        xpdwf_txt_nuevapropiedad_nombre.focus();
    });

    xpdwf_txt_nuevaquery_nombre.addEventListener('change',()=>{        
        xpdwf_txt_nuevaquery_nombre.value = xpdwf_txt_nuevaquery_nombre.value.trim().replaceAll(' ', '_');
    });

    xpdwf_txt_nuevaquery_where.addEventListener('change',()=>{            
        let partes = xpdwf_txt_nuevaquery_where.value.toLowerCase().split(",");
        partes = partes.map(item=>{
            return item.trim().replaceAll(' ', '_');
        });
        xpdwf_txt_nuevaquery_where.value = partes.reduce( (previous_value,current_value,current_index,arreglo) =>{
            if(current_index == 0){
                return current_value;
            }
            return `${previous_value},${current_value}`;
        } );
    });

    xpdwf_txt_nuevaquery_orderby.addEventListener('change',()=>{            
        let partes = xpdwf_txt_nuevaquery_orderby.value.toLowerCase().split(",");
        partes = partes.map(item=>{
            return item.trim().replaceAll(' ', '_');
        });
        xpdwf_txt_nuevaquery_orderby.value = partes.reduce( (previous_value,current_value,current_index,arreglo) =>{
            if(current_index == 0){
                return current_value;
            }
            return `${previous_value},${current_value}`;
        } );
    });

    xpdwf_btn_nuevaquery_agregar.addEventListener('click',(event)=>{
        const objeto = {nombre:xpdwf_txt_nuevaquery_nombre.value.trim()};
        const tr_propiedades = document.getElementsByClassName("tr-propiedad");
        let indice;
        const nombres_propiedades = [];
        for( indice = 0; indice < tr_propiedades.length; indice++ ){
            nombres_propiedades.push(tr_propiedades[indice].dataset.nombre);
        }
        if(objeto.nombre == ""){
            alert("Nombre de Query requerido");
            xpdwf_txt_nuevaquery_nombre.focus();
            return;
        }
        let columnas, columnas_invalidas;
        if(xpdwf_txt_nuevaquery_where.value.trim().length > 0){
            columnas = xpdwf_txt_nuevaquery_where.value.trim().split(",");
            columnas_invalidas = columnas.filter( item=>{ return nombres_propiedades.indexOf(item) < 0 });
            if(columnas_invalidas.length > 0){
                alert(`Campo ${columnas_invalidas[0]} no es válido`);
                xpdwf_txt_nuevaquery_where.focus();
                return;
            }
            if(columnas.length > 0){
                objeto.whereClause = columnas;
            }
        }
        if(xpdwf_txt_nuevaquery_orderby.value.trim().length > 0){
            columnas = xpdwf_txt_nuevaquery_orderby.value.split(",");
            columnas_invalidas = columnas.filter( item=>{ return nombres_propiedades.indexOf(item) < 0 });
            if(columnas_invalidas.length > 0){
                alert(`Campo ${columnas_invalidas[0]} no es válido`);
                xpdwf_txt_nuevaquery_orderby.focus();
                return;
            }
            if(columnas.length > 0){
                objeto.orderBy = columnas;
            }
        }
        const fila = document.createElement('tr');
        fila.classList.add("tr-namedquery");
        fila.dataset.objeto = JSON.stringify(objeto);
        fila.dataset.nombre = objeto.nombre;

        let columna = document.createElement("td");
        const chk_fila = document.createElement("input");
        chk_fila.type = "checkbox";
        chk_fila.classList.add("chk-namedquery");
        chk_fila.dataset.nombre = objeto.nombre;
        columna.appendChild(chk_fila);
        fila.appendChild(columna);

        columna = document.createElement("td");
        columna.innerText = objeto.nombre
        fila.appendChild(columna);

        columna = document.createElement("td");
        if(objeto.whereClause){
            columna.innerText = objeto.whereClause.reduce( (previous_value,current_value,current_index,arreglo) =>{
                if(current_index == 0){
                    return current_value;
                }
                return `${previous_value}, ${current_value}`;
            } )
        }
        fila.appendChild(columna);

        columna = document.createElement("td");
        if(objeto.orderBy){
            columna.innerText = objeto.orderBy.reduce( (previous_value,current_value,current_index,arreglo) =>{
                if(current_index == 0){
                    return current_value;
                }
                return `${previous_value}, ${current_value}`;
            } )
        }
        fila.appendChild(columna);

        columna = document.createElement("td");
        const btn_eliminar = document.createElement("a");
        btn_eliminar.href = "#";
        btn_eliminar.innerText = "Eliminar";
        columna.appendChild(btn_eliminar);
        fila.appendChild(columna);

        xpdwf_tbody_namedqueries.appendChild(fila);
        btn_eliminar.addEventListener('click', ()=>{
            xpdwf_tbody_namedqueries.removeChild(fila);
        });

        xpdwf_txt_nuevaquery_nombre.value = "";
        xpdwf_txt_nuevaquery_where.value = "";
        xpdwf_txt_nuevaquery_orderby.value = "";
        xpdwf_construir_metamodelo();
        xpdwf_txt_nuevaquery_nombre.focus();

    });

    // alert('finalizado scripting');
// });
// alert('Cargado por fuera');