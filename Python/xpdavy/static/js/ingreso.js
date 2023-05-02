window.addEventListener('load', function() {
    // Cargar lista de usuarios al cargar la página
    cargarUsuarios();
  
    // Obtener referencia al formulario de login
    var form = document.getElementById('form_login');
  
    // Agregar evento click a cada item de la lista
    var userList = document.getElementById('user-list');
    userList.addEventListener('click', async function(event) {
      // Obtener el elemento de la lista que se ha hecho clic
      var listItem = event.target.closest('li');
      if (!listItem) return; // Si no se encuentra ningún elemento li, salir
  
      // Obtener el usuario asociado al elemento de la lista
      var usuario = JSON.parse(listItem.dataset.usuario);

      const form = new FormData();
      form.append("nombre", usuario.nombre);
      form.append("clave", usuario.clave);
  
      let response = await fetch("/login", {
        method: "POST",
        body: form
      });

      if(response.status == 200){
        try{
          let data = await response.text();
          sessionStorage.setItem("ssntoken", data);
          sessionStorage.setItem("ssnusr", JSON.stringify(usuario) );
          console.log("usuario " + sessionStorage.getItem("ssnusr") );
          document.location.href="/static/avatares.html";
        }catch(ex){
          console.log("Error", ex);
        }
      }

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