function on_tecla(event){
    const tecla = event.target.innerText;
    const txtNumero = document.getElementById("txtNumero");
    if( txtNumero.value.length >= 6 ){
        return;
    }
    txtNumero.value += tecla;
}

function btnBorrar_click(event){
    const txtNumero = document.getElementById("txtNumero");
    txtNumero.value = "";
}

async function btnConsultar_click(event){
    const txtNumero = document.getElementById("txtNumero");
    const seccion_resultado = document.getElementById("seccion_resultado");
    const valor = txtNumero.value.trim();
    if( valor.length != 6 ){
        alert("Debe ingresar 6 dígitos");
        return;
    }

    if( !seccion_resultado.classList.contains("collapse") ){
        seccion_resultado.classList.add("collapse");
    }

    let formBody = new FormData();
    formBody.append('numero', valor);
    res = await fetch('/evaluar',  {
        method: "POST",
        body: formBody
       // headers: { "Content-Type": "application/x-www-form-urlencoded",}
    });

    if(res.status!=200){
        alert("ocurrió error " + res.status);
        return;
    }

    const obj_resultado = await res.json();
    let clase = "";

    for(let indice = 0; indice < 6; indice ++){
        const btn_resultado = document.getElementById("resultado_" + indice);
        btn_resultado.classList.remove("btn-success","btn-warning","btn-danger")
        btn_resultado.innerText = valor.charAt(indice);
        clase = "btn-" + obj_resultado.resultado[indice];
        btn_resultado.classList.add(clase);
    }

    seccion_resultado.classList.remove("collapse");
}

window.addEventListener("load", event => {
    //habilita botones como teclado
    const lista_botones = document.getElementsByClassName("teclado");
    for(let indice = 0; indice< lista_botones.length; indice++){
        lista_botones[indice].addEventListener("click", on_tecla);
    }
    document.getElementById("btnBorrar").addEventListener("click", btnBorrar_click);
    document.getElementById("btnConsultar").addEventListener("click", btnConsultar_click);

});