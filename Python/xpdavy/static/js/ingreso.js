window.addEventListener('load', function() {
    // Cargar lista de usuarios al cargar la página
    cargarUsuarios();
  
    // Obtener referencia al formulario de login
    var form = document.getElementById('form_login');
  
    // Agregar evento click a cada item de la lista
    var userList = document.getElementById('user-list');
    userList.addEventListener('click', function(event) {
      // Obtener el elemento de la lista que se ha hecho clic
      var listItem = event.target.closest('li');
      if (!listItem) return; // Si no se encuentra ningún elemento li, salir
  
      // Obtener el usuario asociado al elemento de la lista
      var usuario = JSON.parse(listItem.dataset.usuario);
  
      // Asignar el nombre y clave del usuario al formulario
      form.querySelector('#form_login_nombre').value = usuario.nombre;
      form.querySelector('#form_login_clave').value = usuario.clave;
  
      // Enviar el formulario
      form.submit();
    });
  });
  
  function cargarUsuarios() {
    fetch('/api/usuarios')
      .then(function(response) {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Error al cargar la lista de usuarios');
        }
      })
      .then(function(data) {
        // Crear la lista de usuarios
        var userList = document.getElementById('user-list');
        data.lista.forEach(function(usuario) {
          // Crear un elemento de lista para cada usuario
          var listItem = document.createElement('li');
          listItem.classList.add('list-group-item');
          listItem.dataset.usuario = JSON.stringify(usuario);
  
          // Agregar el nombre del usuario al elemento de lista
          var nombre = document.createTextNode(usuario.nombre);
          listItem.appendChild(nombre);
  
          // Agregar el elemento de lista a la lista de usuarios
          userList.appendChild(listItem);
        });
      })
      .catch(function(error) {
        console.log(error);
      });
  }