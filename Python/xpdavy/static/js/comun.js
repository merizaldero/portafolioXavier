function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  function validarUsuario(calback){
    const sesion = getCookie("ssn");
    const form = new FormData();
    form.append("ses", sesion);
  
    // Recupera informacion de usuario
    fetch("/user/info", {
      method: "POST",
      body: form
    })
    .then(response => response.json())
    .then(data => {
      calback(data, sesion);      
    })
    .catch(error => {
      console.log("Error:", error);
    });
  }