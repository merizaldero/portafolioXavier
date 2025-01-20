
let xkt_PRESIONADO = null;

function xkt_sincronizar_items(){
    const rng_items = document.getElementById('xkt_rng_items');
    const txt_items = document.getElementById('xkt_txt_items');
    txt_items.innerHTML = rng_items.value;
}

async function xkt_poblar_grados(){
}

function xkt_shuffle_array(array1) {
    const array = array1.slice();
    let currentIndex = array.length;


    // While there remain elements to shuffle...
    while (currentIndex != 0) {

// Pick a remaining element...
        let randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
    }
  return array;
}

function xkt_kanji_ondragstart(event){
    event.target.classList.add("text_bg_primary");
    event.dataTransfer.setData('text', event.target.id);    
}

function xkt_receptor_ondragover(event){
    event.preventDefault();
}

function xkt_receptor_ondrop(event){
    event.preventDefault();
    
    let target = event.target;
    while(target != null && !target.classList.contains('receptor')){
        target = target.parentNode;
    }
    if(target==null){
        return;
    }
    const div_kanji = document.getElementById(event.dataTransfer.getData('text'));
    const current_kanji_parent = div_kanji.parentNode;
    let current_target_child = null;
    if(target.childNodes.length > 0){
        current_target_child = target.childNodes[0];
    }
    target.appendChild(div_kanji);
    if(current_target_child != null){
        current_kanji_parent.appendChild(current_target_child);
    }

    xkt_evaluar();
}

function xkt_boton_click(event){
    if(xkt_PRESIONADO == null){
        if(event.target.dataset.id_kanji==""){
            return;
        }
        xkt_PRESIONADO = event.target;
        xkt_PRESIONADO.classList.remove("text-bg-success","text-bg-danger");
        xkt_PRESIONADO.classList.add("text-bg-primary");
    }else{
        const parent_presionado = xkt_PRESIONADO.parentNode;
        const parent_target = event.target.parentNode;
        const target = event.target;
        parent_target.appendChild(xkt_PRESIONADO);
        parent_presionado.appendChild(target);
        xkt_PRESIONADO = null;
        xkt_evaluar();
    }
}

function xkt_evaluar(){
    const receptores = document.getElementsByClassName('receptor');
    let indice;
    let conteo_evaluadores = 0;
    let conteo_correctos = 0;
    for(indice = 0; indice < receptores.length; indice ++){
        const receptor = receptores[indice];
        const hijo_receptor = receptor.childNodes[0];
        hijo_receptor.classList.remove('text-bg-primary', 'text-bg-success', 'text-bg-danger');        
        if(receptor.classList.contains('receptor-eval')){
            conteo_evaluadores ++;
            if(receptor.dataset.id_kanji == hijo_receptor.dataset.id_kanji){
                conteo_correctos ++;
                hijo_receptor.classList.add('text-bg-success');
            }else if(hijo_receptor.dataset.id_kanji != ''){
                hijo_receptor.classList.add('text-bg-danger');
            }
        }
    }
    if(conteo_evaluadores == conteo_correctos){
        setTimeout(xkt_ganar, 500);
    }
}

function xkt_ganar(){
    alert("Has ganado!!");
    const respuesta = confirm("Desas jugar otro?");
    if (respuesta){
        xkt_inicializar_juego();
    }
}

async function xkt_inicializar_juego(){    
    //construye lista de niveles seleccionados
    let sel_grado = "";

    const checks_nivel = document.getElementsByClassName("xkt-nivel-check");
    for(let indice = 0; indice<checks_nivel.length ; indice++){        
        const micheck = checks_nivel[indice];
        if(micheck.checked){
            if(sel_grado != ""){
                sel_grado += ",";
            }
            sel_grado += micheck.dataset.idNivel;
        }        
    }
    if(sel_grado == ""){
        alert("Seleccione al menos uno de los Niveles del listado");
        return;
    }

    console.log("selgrado = "+sel_grado);

    const rng_items = document.getElementById('xkt_rng_items');
    const formdata = new FormData();
    formdata.append('niveles',sel_grado);
    formdata.append('muestra',rng_items.value);
    //const respuesta = await fetch("../wp-json/xkt-api/v1/kanjis/",{method:'POST', body:formdata});
    const respuesta = await fetch(`../wp-json/xkt-api/v1/kanjis/?niveles=${sel_grado}&muestra=${rng_items.value}`);
    if(respuesta.status != 200){
        alert('Error en consulta de items ' + respuesta.statusText);
        console.error('Error en consulta de items ' + respuesta.statusText);
        return;
    }
    try{
        const respuesta_json = await respuesta.json();
        console.log( JSON.stringify(respuesta_json) );
        const lista1 = xkt_shuffle_array(respuesta_json.lista);
        const lista2 = xkt_shuffle_array(lista1);
        const tbl_juego = document.getElementById('xkt_tbl_juego');
        tbl_juego.innerHTML = "";
        for(let indice = 0; indice< lista1.length; indice++){
            const tr = document.createElement('tr');
            const tds = [ document.createElement('td'), document.createElement('td'), document.createElement('td') ];
            tds.forEach( (td) => {                
                tr.appendChild(td);
                td.classList.add("p-2","text-center");
            });

            tds[2].classList.remove("text-center");

            const div_emisor = document.createElement('span');
            div_emisor.classList.add("my-1","border","text-center","p-2","h3", "rounded", "receptor");            

            const div_kanji = document.createElement('span');
            div_kanji.id = "kanji_" + lista1[indice].id;
            div_kanji.draggable = true;
            div_kanji.classList.add("border","text-center","p-2","h3", "rounded");
            div_kanji.innerText = lista1[indice].kanji;
            div_kanji.dataset.id_kanji = lista1[indice].id;

            div_emisor.appendChild(div_kanji);
            
            tds[0].appendChild(div_emisor);
            
            const div_receptor = document.createElement('span');
            div_receptor.classList.add("my-1","border","text-center","p-2","h3", "rounded", "receptor", "receptor-eval")
            div_receptor.dataset.id_kanji = lista2[indice].id;

            const div_nokanji = document.createElement('span');
            div_nokanji.id = "nokanji_" + indice;
            div_nokanji.classList.add("text-center","p-2","h3")
            div_nokanji.innerText = ".";
            div_nokanji.dataset.id_kanji = "";

            div_receptor.appendChild(div_nokanji);

            tds[1].appendChild(div_receptor);

            tds[2].innerText = lista2[indice].significado;
            
            tbl_juego.appendChild(tr);

            div_kanji.addEventListener('dragstart', xkt_kanji_ondragstart);
            div_emisor.addEventListener('dragover', xkt_receptor_ondragover);
            div_receptor.addEventListener('dragover', xkt_receptor_ondragover);
            div_emisor.addEventListener('drop', xkt_receptor_ondrop);
            div_receptor.addEventListener('drop', xkt_receptor_ondrop);
            div_kanji.addEventListener('click', xkt_boton_click);
            div_nokanji.addEventListener('click', xkt_boton_click);
            
        }
        xkt_ver_juego();
    }catch(ex){
        alert('Error en tratamiento de items ' + respuesta.statusText);
        console.error('Error en consulta de items ' + respuesta.statusText);
        return;
    }
}

function xkt_ver_parametros(){
    //const btn_nuevo_juego = document.getElementById('xkt_btn_nuevo_juego');
    const btn_param = document.getElementById('xkt_btn_param');
    const div_param = document.getElementById('xkt_div_param');
    const div_juego = document.getElementById('xkt_div_juego');
    btn_param.classList.add('collapse');
    div_param.classList.remove('collapse');
    div_juego.classList.add('collapse');
}

function xkt_ver_juego(){
    //const btn_nuevo_juego = document.getElementById('xkt_btn_nuevo_juego');
    const btn_param = document.getElementById('xkt_btn_param');
    const div_param = document.getElementById('xkt_div_param');
    const div_juego = document.getElementById('xkt_div_juego');
    btn_param.classList.remove('collapse');
    div_param.classList.add('collapse');
    div_juego.classList.remove('collapse');
}

window.addEventListener("load", async (event)=>{
    xkt_sincronizar_items();

    const rng_items = document.getElementById('xkt_rng_items');
    rng_items.addEventListener('change',xkt_sincronizar_items);
    rng_items.addEventListener('mousedown',xkt_sincronizar_items);
    
    const btn_nuevo_juego = document.getElementById('xkt_btn_nuevo_juego');
    btn_nuevo_juego.addEventListener('click', xkt_inicializar_juego)
    const btn_param = document.getElementById('xkt_btn_param');
    btn_param.addEventListener('click', xkt_ver_parametros);    
});

