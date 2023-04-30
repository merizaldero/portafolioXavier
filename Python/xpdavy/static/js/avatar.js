// Obtener el id_avatar del query string

//const queryString = window.location.search;
//const urlParams = new URLSearchParams(queryString);
//const id_avatar = urlParams.get('id_avatar');
const arreglo_url = window.location.href.split("/");
const id_avatar = arreglo_url[ arreglo_url.length - 1 ];

var avatar_data = {};
var id_parte_actual = null;

window.addEventListener('load', function() {
  // Código que se ejecutará al cargar la página
  console.log(`El id del avatar es ${id_avatar}`);

  cargarAvatar();

});

function cargarAvatar(){
    fetch(`/api/avatar/${id_avatar}`)
        .then(response => response.json())
        .then(data => {
            avatar_data = data;
            document.getElementById('txt_nombre').value = avatar_data.nombre;
            cargarPartes();
            cargarImagenAvatar();
        })
        .catch(error => console.log(error));
}

function cargarImagenAvatar(){
    const formData = new FormData();
    formData.append('archivo', new Blob([ JSON.stringify(avatar_data) ]), 'input.json')

    fetch('/imagen/avatartemporal',  {
        method: "POST",
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            let svg_data = data.toString();
            const div_avatar = document.getElementById("div_avatar");
            div_avatar.innerHTML = svg_data;

        })
        .catch(error => console.log(error));
}

function cargarPartes(){    
    fetch('/api/partes')
        .then(response => response.json())
        .then(data => {
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

        })
        .catch(error => console.log(error));
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

function seleccionarParte(id_parte){
    resaltarSeleccionGrupo("parte", "div_parte_",id_parte);
    id_parte_actual = id_parte;
    // carga las prendas disponibles por parte
    fetch(`/api/genero/${avatar_data.id_genero}/parte/${id_parte}/prendas`)
        .then(response => response.json())
        .then(data => {
            let div_prendas = document.getElementById('div_prendas');
            div_prendas.innerHTML = "";
            let event_handler = (event)=>{
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

        })
        .catch(error => console.log(error));
}

function seleccionarPrenda(prenda){
    resaltarSeleccionGrupo("prenda", "div_prenda_",prenda.id_prenda);
    
    //TODO Incorpora el id de prenda a la prenda correspondiente del avatar
    avatar_data.prendas.forEach( (prendax)=>{
        if( prendax.id_parte.toString() == id_parte_actual.toString() ){
            prendax.id_prenda = prenda.id_prenda;
            prendax.svg = prenda.svg;
        }
    } );

    cargarImagenAvatar();
}