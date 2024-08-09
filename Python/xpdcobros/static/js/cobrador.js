function editar_cobrador(event){
    const frm_cobrador = document.getElementById('frm_cobrador');
    frm_cobrador.accion.value = 'form_editar_cobrador';
    frm_cobrador.submit();
}

function agregar_usuario(event){
    let email = prompt("Ingrese correo de usuario:");
    if (! email){
        return;
    }
    const frm_cobrador = document.getElementById('frm_cobrador');
    frm_cobrador.accion.value = 'agregar_usuario';
    frm_cobrador.email.value = email.trim().toLowerCase();
    frm_cobrador.submit();
}

function habilitar_usuario(event){
    const frm_cobrador = document.getElementById('frm_cobrador');
    frm_cobrador.accion.value = 'habilitar_usuario';
    frm_cobrador.id_usuario_cobrador.value = event.target.dataset.id_usuario_cobrador;
    frm_cobrador.submit();
}

function deshabilitar_usuario(event){
    const frm_cobrador = document.getElementById('frm_cobrador');
    frm_cobrador.accion.value = 'deshabilitar_usuario';
    frm_cobrador.id_usuario_cobrador.value = event.target.dataset.id_usuario_cobrador;
    frm_cobrador.submit();
}

function habilitar_cuenta(event){
    const frm_cobrador = document.getElementById('frm_cobrador');
    frm_cobrador.accion.value = 'habilitar_cuenta';
    frm_cobrador.id_cuenta.value = event.target.dataset.id_cuenta;
    frm_cobrador.submit();
}

function deshabilitar_cuenta(event){
    const frm_cobrador = document.getElementById('frm_cobrador');
    frm_cobrador.accion.value = 'deshabilitar_cuenta';
    frm_cobrador.id_cuenta.value = event.target.dataset.id_cuenta;
    frm_cobrador.submit();
}

window.addEventListener("load", (event)=>{
    let indice;
    
    const btn_editar_cobrador = document.getElementById('btn_editar_cobrador');
    btn_editar_cobrador.addEventListener('click', editar_cobrador);
    
    const btn_agregar_usuario = document.getElementById('btn_agregar_usuario');
    btn_agregar_usuario.addEventListener('click', agregar_usuario);
    
    const btn_habilitar_usuario = document.getElementsByClassName('btn_habilitar_usuario');
    for(indice = 0; indice<btn_habilitar_usuario.length; indice++){
        btn_habilitar_usuario[indice].addEventListener('click', habilitar_usuario);
    }
    
    const btn_deshabilitar_usuario = document.getElementsByClassName('btn_deshabilitar_usuario');
    for(indice = 0; indice<btn_deshabilitar_usuario.length; indice++){
        btn_deshabilitar_usuario[indice].addEventListener('click', deshabilitar_usuario);
    }

    const btn_habilitar_cuenta = document.getElementsByClassName('btn_habilitar_cuenta');
    for(indice = 0; indice<btn_habilitar_cuenta.length; indice++){
        btn_habilitar_cuenta[indice].addEventListener('click', habilitar_cuenta);
    }
    
    const btn_deshabilitar_cuenta = document.getElementsByClassName('btn_deshabilitar_cuenta');
    for(indice = 0; indice<btn_deshabilitar_cuenta.length; indice++){
        btn_deshabilitar_cuenta[indice].addEventListener('click', deshabilitar_cuenta);
    }
    
});