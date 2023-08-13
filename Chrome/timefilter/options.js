function saveOptions() {
    const sites = document.getElementById("site-list").options;
    let sitios = [];
    
    for( let indice = 0; indice < sites.length; indice ++){
        sitios.push(sites[indice].value);
    }        

    const valores = {
        "xpdtf_admin": document.getElementById("admin-password").value ,
        "xpdtf_moderador": document.getElementById("mod-password").value ,
        "xpdtf_duracion_inicial": document.getElementById("initial-time").value,
        "xpdtf_duracion_extendida": document.getElementById("extended-time").value,
        "xpdtf_redireccion": document.getElementById("redirection-url").value,
        "xpdtf_sitios": JSON.stringify(sitios),
        'xpdtf_tiempos': '{}'
    };

    chrome.storage.local.set( valores ).then(()=>{
        console.log("Options saved.");
        alertar("Opciones Guardadas.");
    }).catch(err=>{
        console.log("Error Saving options." + err.toString() );
        alertar("Error al Guardar"  + err.toString(),"danger" );
    });
    
}

function loadOptions(){

    const auth_form = document.getElementById("auth_form");
    auth_form.style.display="none";
    auth_form.style.visibility="hidden";

    const opciones_form = document.getElementById("opciones-form");
    opciones_form.style.display="block";
    opciones_form.style.visibility="visible";

    chrome.storage.local.get(["xpdtf_admin", "xpdtf_moderador", "xpdtf_duracion_inicial", "xpdtf_duracion_extendida", "xpdtf_redireccion", "xpdtf_sitios"]
    ).then( miStorage =>{        
        document.getElementById("admin-password").value = miStorage.xpdtf_admin;
        document.getElementById("mod-password").value = miStorage.xpdtf_moderador;
        document.getElementById("initial-time").value = miStorage.xpdtf_duracion_inicial;
        document.getElementById("extended-time").value = miStorage.xpdtf_duracion_extendida;
        document.getElementById("redirection-url").value = miStorage.xpdtf_redireccion;
        const sites = document.getElementById("site-list");
        sites.innerHTML = "";

        JSON.parse( miStorage.xpdtf_sitios ).forEach( element => {
            let opcion = document.createElement("option");
            opcion.innerText = element;
            opcion.value = element;
            sites.appendChild(opcion);
        });
    }).catch( err => {
        console.log( err.toString() );
    });

    return false;

}

function agregarSitio(){

    let nuevo_sitio = prompt("Patron de nuevo sitio");

    if( nuevo_sitio == null || nuevo_sitio.trim() === "" ){
        return;
    }

    const site_list = document.getElementById("site-list");
    // valida que no esté repetido
    let sitios = [];
    
    for( let indice = 0; indice < site_list.options.length; indice ++){
        sitios.push(site_list.options[indice].value);
    }

    if(sitios.indexOf(nuevo_sitio) >= 0 ){
        return;
    }

    let opcion = document.createElement("option");
    opcion.innerText = nuevo_sitio;
    opcion.value = nuevo_sitio;
    site_list.appendChild(opcion);
}

function removerSitios(){
    const site_list = document.getElementById("site-list");
    let sitios_remover = [];

    for( let indice = 0; indice < site_list.options.length; indice ++){
        if(site_list.options[indice].selected){
            sitios_remover.push(site_list.options[indice]);
        }
    }

    sitios_remover.forEach(item=>{site_list.removeChild(item)});

}

async function autenticar(){
    const password = document.getElementById("password").value;
    const item = await chrome.storage.local.get("xpdtf_admin")
    if (password === item.xpdtf_admin ) {
        loadOptions();
    } else {
        alertar("Invalid admin password........","danger");
    }
    return false;
}

function alertar(texto, modo="success"){
    const mensajero = document.getElementById("mensaje");
    mensajero.getElementsByTagName("span")[0].innerText = texto;
    if(modo ==="success"){
        mensajero.classList.remove("alert-danger");
        mensajero.classList.add("alert-success");
    }else{
        mensajero.classList.remove("alert-success");
        mensajero.classList.add("alert-danger");    
    }    
    mensajero.classList.remove("collapse");
}

function cerrarVentana(){
    window.close();
}


async function consultarAccesos(){
    const { xpdtf_tiempos } = await chrome.storage.local.get( [ 'xpdtf_tiempos' ] );
    const obj_xpdtf_tiempos = JSON.parse(xpdtf_tiempos);
    let tiempos = Object.keys(obj_xpdtf_tiempos).map( sitio => { 
        return [ sitio, obj_xpdtf_tiempos[sitio].last_tic, obj_xpdtf_tiempos[sitio].tics ]; 
    });
    const tblAccesos = document.getElementById('tblAccesos');
    tblAccesos.innerHTML = "";
    tiempos.forEach( item=> {
        let tr = document.createElement("tr");
        item.forEach(campo =>{
            let td = document.createElement("td");
            td.appendChild(document.createTextNode( campo ));
            tr.append(td)
        });        
        tblAccesos.appendChild(tr);
    });
    //alert("listado actualizado");
}

document.getElementById("btn_guardar").addEventListener("click", saveOptions);
document.getElementById("btn_login").addEventListener("click", autenticar);
document.getElementById("btn_add_filter").addEventListener("click", agregarSitio);
document.getElementById("btn_remove_filter").addEventListener("click", removerSitios);
// document.getElementById("btn_close_window").addEventListener("click", cerrarVentana);

document.addEventListener("load", consultarAccesos);
document.getElementById("btn_actualizar_accesos").addEventListener("click", consultarAccesos);
