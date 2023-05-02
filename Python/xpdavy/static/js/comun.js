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
    return null;
  }

  async function validarUsuario(){
    return sessionStorage.getItem("ssntoken") != null;
  }

  function getUsuario(){
    let usr = sessionStorage.getItem("ssnusr");
    if( usr !=null ){
      return JSON.parse(usr);
    }
    else null;
  }

  function getToken(){
    return sessionStorage.getItem("ssntoken")
  }