var USUARIO = null;
var SESION = null;
window.onload = function() {
    // Consulta usuario
    validarUsuario( (usuario, sesion)=>{
        USUARIO = usuario;
        SESION = sesion;
        const nombreUsuario = document.getElementById("nombre_usuario");
        nombreUsuario.innerText = usuario.nombre;
      } ); 

    // Consulta los géneros
    fetch('/api/generos')
      .then(function(response) {
        if (!response.ok) {
          throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
      })
      .then(function(data) {
        var generosHtml = '';
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
      })
      .catch(function(error) {
        console.log('Error en la consulta: ', error);
      });

  }
  
  function seleccionarGenero(generoId) {
    // Implementar acción de selección de género
    console.log('Genero seleccionado: ', generoId);
    const form_seleccion = document.getElementById("form_seleccion");
    form_seleccion.querySelector('#form_id_genero').value = generoId;
    form_seleccion.querySelector('#form_id_usuario').value = SESION;
    form_seleccion.submit();
  }