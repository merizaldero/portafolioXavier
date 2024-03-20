

function txt_buscar_OnKeypress(event){
    const texto_buscar = event.target.value.trim().toLowerCase();
    const bvhs = document.getElementsByClassName('bvh');
    for( let indice = 0; indice < bvhs.length; indice ++){
        const a_bvh = bvhs[indice];
        if( texto_buscar == '' || a_bvh.dataset.directorio.toLowerCase().indexOf(texto_buscar) >= 0 ){
            a_bvh.classList.remove('collapse');
        }else{
            a_bvh.classList.add('collapse');
        }
    }
}

window.addEventListener('load', async ()=>{
    const txt_buscar = document.getElementById('txt_buscar');
    txt_buscar.addEventListener('keypress', txt_buscar_OnKeypress );



});