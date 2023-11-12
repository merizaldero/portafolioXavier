function nuevoAvatar(){
  const selGrupos = document.getElementById("selGrupo");
  document.location.href = "/nuevo_skin/" + selGrupos.value;
}

async function cargarGrupoActual(){
  
  const selGrupos = document.getElementById("selGrupo");
  const divAvatares = document.getElementById("divAvatares");
  const grupo = selGrupos.value;

  let elementosEliminar = document.getElementsByClassName("avatar");
  while( elementosEliminar.length > 0 ){
    elementosEliminar[0].parentElement.removeChild(elementosEliminar[0]);
  }

  let respuesta = await fetch("/grupo/" + grupo , {
    method: "GET"
  });
  
  if(respuesta.status != 200){
    this.alert("No se pudo cargar listado");
    return;
  }

  try{
    let data = await respuesta.json();
    data.lista.forEach(element => {
      let divElemento = document.createElement("div");
      divElemento.classList.add('list-group-item');
      divElemento.classList.add('avatar');
      divElemento.classList.add('d-flex');
      divElemento.classList.add('d-row');

      let imgElemento = document.createElement("img");
      imgElemento.src = element.path;

      let spanElemento = document.createElement("span");
      spanElemento.appendChild(document.createTextNode(element.nombre));

      divElemento.appendChild(imgElemento);
      divElemento.appendChild(spanElemento);  
      divAvatares.appendChild(divElemento);
    });

  }catch(ex){
    console.log("Error", ex);
  }

}

window.addEventListener('load', async function() {
  // carga listados de grupos
  let respuesta = await fetch("/grupos", {
    method: "GET"
  });

  if(respuesta.status != 200){
    this.alert("No se pudo cargar grupos");
    return;
  }

  try{
    let data = await respuesta.json();
    const selGrupos = document.getElementById("selGrupo");
    let seleccionado = null;
    data.lista.forEach(element => {
      let opcion = document.createElement("option");
      opcion.value = element;
      opcion.appendChild(document.createTextNode(element));
      if(seleccionado == null){
        opcion.selected = true;
        seleccionado = element;
      }
      selGrupos.appendChild(opcion);
    });

    await cargarGrupoActual();

    selGrupos.addEventListener("change", cargarGrupoActual);

    const btnNuevo = document.getElementById("btnNuevo");

    btnNuevo.addEventListener("click", nuevoAvatar );

  }catch(ex){
    console.log("Error", ex);
  }
  

});
/*
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

  */