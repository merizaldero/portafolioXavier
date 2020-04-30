
//Carga configuracion local
function loadLocalConfig( url , parametrosPost, nodo){
  $.post( url , parametrosPost ,function(data,status){
    if(status == "success"){
      try{
        for(clave in data){
          nodo.data(clave ,data[clave])
          //alert(clave + "=" + data[clave])
        }
      }catch(ex){
        alert(ex.message);
      }
    }else{
      alert("La aplicacion no responde");
    }
  });
}

var _FILEDIALOG = null;

var frmFileDialog_item_click = function(){
  var archivo = $(this).data("archivo");
  var tipo = $(this).data("tipo");
  $(this).parent().find("li").removeClass("seleccionado");
  $(this).addClass("seleccionado");
  if(tipo=="arch"){
    _FILEDIALOG.find("input[name='nombreArchivo']").val(archivo);
  } else {
    var nuevoPath = "";
    if(archivo == "..") {
      var paths = _FILEDIALOG.find("input[name='path']").val().split("/");
      for (var i =0; i < paths.length - 1; i ++){
        if( nuevoPath != "" ){
          nuevoPath += "/";
        }
        nuevoPath += paths[i];
      }
    } else {
      nuevoPath = _FILEDIALOG.find("input[name='path']").val();
      if(nuevoPath ==""){
        nuevoPath = archivo;
      }else{
        nuevoPath += "/" + archivo;
      }
    }
    _FILEDIALOG.find("input[name='path']").val( nuevoPath );
    frmFileDialog_cargarLista();
  }

};

function frmFileDialog_cargarLista(){
  var path = _FILEDIALOG.find("input[name='path']").val();
  $.post("/listarFs.html",{"folder": path },function(data,status){
    if(status == "success"){
      if( "error" in data ){
        alert(data["error"]);
      }
      if( "lista" in data ){
        var ul = _FILEDIALOG.find(".listaArchivos");
        ul.html("");
        for( var i= 0; i < data["lista"].length; i++ ){
          var archivo = data["lista"][i];
          var li =$("<li></li>");
          li.data("archivo", archivo["archivo"]);
          li.data("tipo", archivo["tipo"]);
          if(archivo["tipo"]=="arch"){
            li.text(archivo["archivo"]);
          }else{
            li.text("[" + archivo["archivo"] + "]");
          }
          ul.append(li);
        }
        ul.find("li").click( frmFileDialog_item_click );
      }
    }else{
      alert("La aplicacion no responde");
    }
  });
}

// manejo de dialogo de texto

function initFrmFileDialog(fileDialog){
  _FILEDIALOG = fileDialog;
  _FILEDIALOG.hide();
  

}

function mostrarGuardar(modoGuardar, dataExtra, nombreArchivo ,funcionHandler ){

  //llena el dialogo
  _FILEDIALOG.html("");
  var div1 = $("<div></div>");
  div1.append( "<div class=\"tituloDialogo\">Abrir o Guardar</div>");
  div1.append( "<div class=\"instrucciones\">Elegir archivo</div>");
  div1.append( "<div class=\"instrucciones\"><input name=\"path\" disabled=\"disabled\"/></div>");
  div1.append( "<ul class=\"listaArchivos\"></ul>");
  div1.append( "<table class=\"instrucciones\"><tr><td class=\"nombreArchivo\"><input name=\"nombreArchivo\"/></td><td class=\"extensionArchivo\"></td></tr></table>");
  div1.append( "<div class=\"barraBotones\"><a class=\"btnEscogerArchivo botonDialogo boton \">Aceptar</a><a class=\"btnCancelarArchivo botonDialogo boton\">Cancelar</a></div>");
  _FILEDIALOG.append(div1);
  
  _FILEDIALOG.find("input[name='path']").val("");

  // prepara dialogo
  _FILEDIALOG.data("modoGuardar",modoGuardar);
  _FILEDIALOG.find(".tituloDialogo").text(modoGuardar?"Guardar como":"Abrir");
  _FILEDIALOG.data("dataExtra",dataExtra);
  frmFileDialog_cargarLista();
  _FILEDIALOG.find("input[name='nombreArchivo']").val( (nombreArchivo!=null)?nombreArchivo:"");
  _FILEDIALOG.find(".btnEscogerArchivo").click(function(){
    var nombreArchivo = _FILEDIALOG.find("input[name='nombreArchivo']").val();
    var modoGuardar = _FILEDIALOG.data("modoGuardar");
    //var conteoSeleccion = _FILEDIALOG.find("li.seleccionado").size();
    var conteoSeleccion = _FILEDIALOG.find("li[data-archivo='"+nombreArchivo+"']").size();

    var procederHandler = true;
    //alert( modoGuardar ? "guardando" : "abriendo");
    if( modoGuardar && conteoSeleccion > 0){
      procederHandler = confirm("Desea sobreescribir \n"+nombreArchivo+" ?");
    }
    if( !modoGuardar && nombreArchivo=="" ){
      procederHandler = false;
    }
    if( procederHandler ){
      var path = _FILEDIALOG.find("input[name='path']").val();
      var datosExtra = _FILEDIALOG.data("dataExtra");
      if(path != ""){
        nombreArchivo = path+"/"+nombreArchivo;
      }
      _FILEDIALOG.hide();
      funcionHandler(nombreArchivo,datosExtra);
    }
    
  });
  _FILEDIALOG.find(".btnCancelarArchivo").click(function(){
    _FILEDIALOG.hide();
  });

  _FILEDIALOG.show();
}


