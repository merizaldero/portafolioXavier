var SESION = null;
var USUARIO = null;

window.onload = async function() {
  if( ! await validarUsuario() ){
    alert("Usuario no valido");
    document.location.href="/static/ingreso.html";
    return;
  }

  USUARIO = getUsuario();
  SESION = getToken();

  const nombreUsuario = document.getElementById("nombre_usuario");
  nombreUsuario.innerText = USUARIO.nombre;

    // Consulta los géneros
  let response = await fetch('/api/generos');
  if(response.status != 200){
    return;
  }
  try{
    let data = await response.json();
    let generosHtml = '';
    data.lista.forEach(function(genero) {
      generosHtml += '<div class="col-sm-4">';
      generosHtml += '<button type="button" class="btn btn-outline-primary bg-light btn-lg" onclick="seleccionarGenero(' + genero.id + ')">';
      generosHtml += '<div class="d-flex flex-column">'
      generosHtml += '<span class="genero-simbolo">' + genero.simbolo + '</span>';
      generosHtml += '<span class="genero-nombre">' + genero.nombre + '</span>';
      generosHtml += '</div>'
      generosHtml += '</button>';
      generosHtml += '</div>';
    });
    document.getElementById('generos').innerHTML = generosHtml;
  }catch(ex){
    console.log("Error", ex);
  }

}

function seleccionarGenero(generoId) {
  // Implementar acción de selección de género
  console.log('Genero seleccionado: ', generoId);
  const form_seleccion = document.getElementById("form_seleccion");
  form_seleccion.querySelector('#form_id_genero').value = generoId;
  form_seleccion.querySelector('#form_id_usuario').value = SESION;
  form_seleccion.submit();
}