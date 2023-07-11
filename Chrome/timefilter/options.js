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
        "xpdtf_sitios": JSON.stringify(sitios)
    };

    chrome.storage.local.set( valores ).then(()=>{
        console.log("Options saved.");
        document.getElementById("message").textContent = "Options saved.";
    }).catch(err=>{
        console.log("Error Saving options." + err.toString() );
        document.getElementById("message").textContent = "Options saved."  + err.toString() ;
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

async function autenticar(){
    const password = document.getElementById("password").value;
    const item = await chrome.storage.local.get("xpdtf_admin")
    if (password === item.xpdtf_admin ) {
        loadOptions();
    } else {
        document.getElementById("message").textContent = "Invalid admin password.";
        alert("Invalid admin password........");
    }
    return false;
}
  
document.getElementById("save-options").addEventListener("click", saveOptions);

document.getElementById("submit-auth").addEventListener("click", autenticar);


