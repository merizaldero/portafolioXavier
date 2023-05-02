var USUARIO = null;

window.onload = async function() {
  if( ! await validarUsuario() ){
    alert("Usuario no valido");
    //document.location.href="/static/ingreso.html";
    return;
  }

  USUARIO = getUsuario();
  const nombreUsuario = document.getElementById("nombre_usuario");
  nombreUsuario.innerText = USUARIO.nombre;
  await consultarAvatares( USUARIO.id );

  //Funcionalidad Nuevo Usuario
  const btn_nuevo_avatar = document.getElementById("btn_nuevo_avatar");
  btn_nuevo_avatar.onclick = (event) =>{
      document.location.href="/static/sel_genero.html";
  };

};

async function consultarAvatares(id_usuario){
  let response = await fetch("/api/user/" + id_usuario + "/avatares", {
      method: "GET"
  });
  if(response.status == 200){
    try{
      let data = await response.json()
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

    }catch(ex){
      console.log("Error", ex);
    }       
  }
    
}