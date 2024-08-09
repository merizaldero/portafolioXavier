async function input_OnChange(event){
    const formdata = new FormData();
    formdata.append("id_config", event.target.dataset.id_config);
    formdata.append("valor_config", event.target.value);
    try{
        const respuesta = await fetch("/xpdcobros/admin/config",{method:'POST', body:formdata});
        if(respuesta.status != 200){
            throw {message:'Respuesta no esperada'}
        }
        const respuesta_json = await respuesta.json();
        const div_mensaje = document.getElementById('div_mensaje');
        if(respuesta_json.lvl == 'danger'){
            div_mensaje.classList.remove('alert-success');
            div_mensaje.classList.add('alert-danger');
        }else{
            div_mensaje.classList.add('alert-success');
            div_mensaje.classList.remove('alert-danger');
        }
        div_mensaje.innerHTML = respuesta_json.mensaje;
        div_mensaje.classList.remove('collapse');
    }catch(ex){
        div_mensaje.classList.remove('alert-success');
        div_mensaje.classList.add('alert-danger');
        div_mensaje.innerHTML = ex.message;
        div_mensaje.classList.remove('collapse');
    }
    
}

window.addEventListener("load", (event)=>{
    const inputs = document.getElementsByClassName("config-input");
    for( let indice = 0; indice < inputs.length; indice ++ ){
        inputs[indice].addEventListener("change", input_OnChange);
    }
});