  var USUARIO = null;
window.onload = function() {
    validarUsuario( (usuario)=>{
      USUARIO = usuario;
      const nombreUsuario = document.getElementById("nombre_usuario");
      nombreUsuario.innerText = usuario.nombre;
      consultarAvatares(usuario['id']);
    } );    

    //Funcionalidad Nuevo Usuario
    const btn_nuevo_avatar = document.getElementById("btn_nuevo_avatar");
    btn_nuevo_avatar.onclick = (event) =>{
        document.location.href="/static/sel_genero.html";
    };

  };

  function consultarAvatares(id_usuario){
    fetch("/api/user/" + id_usuario + "/avatares", {
        method: "GET"
      })
      .then(response => response.json())
      .then(data => {
            var avatarList = document.getElementById('avatares');
            data.lista.forEach( (avatar)=>{
            // Crear un elemento de lista para cada usuario
            var listItem = document.createElement('a');
            listItem.href = `/avatar/${avatar.id}`
            listItem.classList.add('list-group-item');
            listItem.classList.add('avatar');
            listItem.dataset.avatar = JSON.stringify(avatar);
    
            // Agregar el nombre del usuario al elemento de lista
            var nombre = document.createTextNode(avatar.nombre);
            listItem.appendChild(nombre);
    
            // Agregar el elemento de lista a la lista de usuarios
            avatarList.appendChild(listItem);
        });
      })
      .catch(error => {
        console.log("Error:", error);
      });
  }