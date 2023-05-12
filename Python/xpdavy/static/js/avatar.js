const arreglo_url = window.location.href.split("/");
const id_avatar = arreglo_url[ arreglo_url.length - 1 ];

var AVATAR_DATA = {};
var id_parte_actual = null;

var USUARIO = null;

window.onload = async function() {
  if( ! await validarUsuario() ){
    alert("Usuario no valido");
    document.location.href="/static/ingreso.html";
    return;
  }

  USUARIO = getUsuario();
  const nombreUsuario = document.getElementById("nombre_usuario");
  nombreUsuario.innerText = USUARIO.nombre;

  // Código que se ejecutará al cargar la página
  console.log(`El id del avatar es ${id_avatar}`);

  await cargarAvatar();

}

async function cargarAvatar(){
    let response = await fetch(`/api/avatar/${id_avatar}`);
    try{
        let data = await response.json();
        AVATAR_DATA = data;
        document.getElementById('txt_nombre').value = AVATAR_DATA.nombre;
        await cargarPartes();
        await cargarImagenAvatar();
    }catch(ex){
        console.log("Error ", ex);
    }
}

async function cargarImagenAvatar(){
    const bodyAvatar = JSON.stringify(AVATAR_DATA);
    response = await fetch('/imagen/avatartemporal',  {
        method: "POST",
        body: bodyAvatar,
        headers: { 'Content-Type': 'application/json'}
    });

    if(response.status != 200){
    
        console.log (response.status, await response.text() );
        return;
    }

    try{
        let data = await response.text();
        let svg_data = data.toString();
        const div_avatar = document.getElementById("div_avatar");
        div_avatar.innerHTML = svg_data;
    }catch(ex){
        console.log("Error ", ex);
    }

}

async function cargarPartes(){    
    response = await fetch('/api/partes');
    if(response.status != 200){
        console.log (response.status, response.text );
        return;
    }

    try{
        let data = await response.json()
        let div_partes = document.getElementById('div_partes');
        div_partes.innerHTML = "";
        let event_handler = (event)=>{
            let id_parte = event.target.dataset.id_parte;
            seleccionarParte(id_parte);
        };
        data.lista.forEach(parte => {
            let div_item = document.createElement('button');
            div_item.classList.add('btn');
            div_item.classList.add('btn-outline-primary');
            div_item.classList.add('btn-sm');
            div_item.classList.add('parte');
            div_item.dataset.id_parte=parte.id;
            div_item.id = `div_parte_${parte.id}`;

            div_item.textContent = parte.nombre;
            div_partes.appendChild(div_item);
    
            div_item = document.getElementById(`div_parte_${parte.id}`);
            div_item.addEventListener('click', event_handler);
        });
    }catch(ex){
        console.log("Error ", ex);
    }
       
}

function resaltarSeleccionGrupo(className, prefijo, id_seleccionado){    
    let botones = document.getElementsByClassName(className);
    for(var indice = 0; indice < botones.length; indice ++ ){
        var boton = botones.item(indice); 
        if(boton.id == prefijo + id_seleccionado){
            boton.classList.remove('btn-outline-primary');
            boton.classList.add('btn-primary');
        }else{
            boton.classList.remove('btn-primary');
            boton.classList.add('btn-outline-primary');
        }
    }
}

async function seleccionarParte(id_parte){
    resaltarSeleccionGrupo("parte", "div_parte_",id_parte);
    id_parte_actual = id_parte;
    // carga las prendas disponibles por parte
    response = await fetch(`/api/genero/${AVATAR_DATA.id_genero}/parte/${id_parte}/prendas`);
    if(response.status != 200){
        console.log (response.status, response.text );
        return;
    }

    try{
        let data = await response.json();
        let div_prendas = document.getElementById('div_prendas');
        div_prendas.innerHTML = "";
        let event_handler = async (event)=>{
            let prenda = JSON.parse(event.target.dataset.prenda);
            seleccionarPrenda(prenda);
        };
        data.lista.forEach(prenda => {
            let div_item = document.createElement('button');
            div_item.classList.add('btn');
            div_item.classList.add('btn-outline-primary');
            div_item.classList.add('btn-sm');
            div_item.classList.add('prenda');
            div_item.dataset.prenda=JSON.stringify(prenda);
            div_item.id = `div_prenda_${prenda.id_prenda}`;
            
            div_item.textContent = prenda.nombre;

            div_prendas.appendChild(div_item);
    
            div_item = document.getElementById(`div_prenda_${prenda.id_prenda}`);
            div_item.addEventListener('click', event_handler);
        });
    }catch(ex){
        console.log("Error ", ex);
    }
       
}

async function seleccionarPrenda(prenda){
    resaltarSeleccionGrupo("prenda", "div_prenda_",prenda.id_prenda);
    
    //TODO Incorpora el id de prenda a la prenda correspondiente del avatar
    AVATAR_DATA.prendas.forEach( (prendax)=>{
        if( prendax.id_parte.toString() == id_parte_actual.toString() ){
            prendax.id_prenda = prenda.id_prenda;
            prendax.svg = prenda.svg;
        }
    } );

    await cargarImagenAvatar();
}