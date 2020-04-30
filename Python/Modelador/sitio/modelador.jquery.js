
var DESPLEGADO ="&#x25A0;";
var REPLEGADO  ="&#x25A1;";
var ICON_AGREGAR="&#x2795;";

var PREFIJO = "";
var SUBFIJO = ".html";

var CATALOGOS = {};

function xmd_mostrarPantalla( pantalla1 ){
    var pantallas = [
        "#divMenuPrincipal",
        "#divModelView",        
        "#frmCrearModelo",
        "#frmAbrirModelo",
        "#frmEliminarObjetoModelo",
        "#frmEditarObjetoModelo",
        "#frmMantenimiento",
        "#frmGenerador",
        "#frmDesplegarContenido",
        "#frmParches",
        "#frmExportarModelo",
        "#frmExpReg",
        "#frmImportarModelo",
        "#frmSeleccionarReferencia"

    ];
    var indice;
    for( indice in pantallas ){
        if( pantallas[indice] == pantalla1){
            $( pantallas[indice] ).show();
        }else{
            $( pantallas[indice] ).hide();
        }
    }
}

function xmd_desplegarLista(idObjeto,idJerarquia){
  //alert ("Despliega "+idJerarquia+" de "+idObjeto );
  var ul = $("#o_"+idObjeto+"_l_"+idJerarquia).children("ul:first");
  ul.html("Despliega "+idJerarquia+" de "+idObjeto );
  
  $.post( PREFIJO + "/getObjetosByPadre" + SUBFIJO , {"idObjeto":idObjeto,"idJerarquia":idJerarquia},function(data,status){
    //alert(ul);
    if(status == "success"){
      //alert("despliega "+data.lista.length+"elementos");
      ul.html("");
      for(var i = 0; i < data.lista.length ; i++){
        //alert("recupera "+data.lista[i].nombre);
        var nodo = xmd_getNodoObjeto(data.lista[i]);
        if(i==0){
          nodo.find(".moverArriba").hide();
        }
        if(i== data.lista.length -1){
          nodo.find(".moverAbajo").hide();
        }
        ul.append( nodo );
      }
      ul.find(".expansor").click(xmd_expansor_click);
      ul.find(".anadirHijo").click(xmd_anadirHijo_click);
      ul.find(".linkPropiedades").click(xmd_linkPropiedades_click);
      ul.find(".moverArriba").click(xmd_moverArriba_click);
      ul.find(".moverAbajo").click(xmd_moverAbajo_click);
      ul.find(".eliminarNodo").click(xmd_eliminarNodo_click);
    }else{
      alert("Error al recuperar Jerarquia");
      //ul.html( "Error al recuperar "+idJerarquia+" de "+idObjeto );
    }
  });
}

function xmd_desplegarAtributos(objetoModelo){
    $("#frmEditarObjetoModelo").find("input[name='idObjeto']").val(objetoModelo.idObjeto);
    $("#frmEditarObjeto_idTipoMetamodelo").text(objetoModelo.idTipoMetamodelo);
    $("#frmEditarObjetoModelo").find("input[name='nombreObjeto']").val(objetoModelo.nombre);
    $("#frmEditarObjetoModelo").find("input[name='descripcion']").val(objetoModelo.descripcion);
    var seccionCampos = $("#frmEditarObjetoModelo").find(".contenidoVinetasEditor").html("");
    for(var i=0; i<objetoModelo._atributos.length ; i++){
        var atributo = objetoModelo._atributos[i];
        var tr = $("<tr></tr>")
        var tdEtiqueta = $("<td></td>")
        var tdValor = $("<td></td>")
        var tr2 = $("<tr></tr>")
        var tdMensaje = $("<td></td>")
        tr.addClass("lineaAtributo");
        tdEtiqueta.addClass("etiquetaAtributo");
        tdEtiqueta.text( atributo.idAtributoMetamodelo );
        tr.append(tdEtiqueta);
        tdValor.addClass("valorAtributo");
	
        var inputAtributo = $("<input></input>");
        if(atributo.idCatalogo != null){
            inputAtributo = $("<select name=\"" + atributo.idAtributoMetamodelo + "\" class=\"idCatalogo"+ atributo.idCatalogo +"\"><option value=\"\">-Seleccionar-</option></select>");
            //alert("desplegando catalogo" + atributo.idCatalogo );
            for(var indiceCatalogo = 0; indiceCatalogo < CATALOGOS[ atributo.idCatalogo ].length; indiceCatalogo ++){
                var valorCatalogo = CATALOGOS[ atributo.idCatalogo ] [indiceCatalogo];
                var opcionValorCatalogo = $("<option value=\"" + valorCatalogo["clave"] + "\" " + ( valorCatalogo["clave"] == atributo.valor ? "SELECTED" : "" ) + " >" + valorCatalogo["etiqueta"] + "</option>");
                inputAtributo.append(opcionValorCatalogo);
            }
        } else if( atributo.idTipoMetamodeloRef != null){
            inputAtributo = $("<span class=\"spanSelectorReferencia\"><input type=\"hidden\" name=\"" + atributo.idAtributoMetamodelo + "\" value=\"" + ((atributo.valor==null)?"":atributo.valor) + "\"><input type=\"text\" name=\"" + atributo.idAtributoMetamodelo + "_xmdetiqueta\" value=\"" + ((atributo.nombreObjetoRef ==null)?"":atributo.nombreObjetoRef) + "\" readonly><button class=\"selectorReferencia\" data-idmodelo=\"" + objetoModelo.idModelo + "\" data-idtipometamodeloref=\"" + atributo.idTipoMetamodeloRef + "\">...</button></span>");
        }else{
            inputAtributo.attr("type","text");
    	       inputAtributo.attr("name", atributo.idAtributoMetamodelo );
    	       inputAtributo.val( atributo.valor );
    	   }
    
    
    /*
    if( atributo. expRegularValidacion != null ){
      inputAtributo.data("expRegularValidacion",atributo.expRegularValidacion );
    }
    if( atributo.longitudAtributo != null && atributo.longitudAtributo > 0 ){
      inputAtributo.attr("maxlength",atributo.longitudAtributo);
    }
    */
    
    tdValor.append( inputAtributo);
    tr.append(tdValor);
    seccionCampos.append(tr);
    tdMensaje.attr("id","msg_"+ atributo.idAtributoMetamodelo );
    tdMensaje.attr("colspan",2);
    tdMensaje.addClass("mensajeError");
    tr2.append(tdMensaje);
    seccionCampos.append(tr2);
  }
  
  //Habilita accion de asignar referencias
  seccionCampos.find(".selectorReferencia").click(function(){
    //alert("Desplegando lista para seleccion");
    xmd_desplegarSelectorReferencia( $(this).data("idmodelo") , $(this).data("idtipometamodeloref") , $(this) );
  });
  
  xmd_mostrarPantalla("#frmEditarObjetoModelo");
  
}

function xmd_desplegarSelectorReferencia(idModelo, idTipoMetamodeloRef, referenciaSelector){
	//alert("preparando selector para idModelo "+ idModelo + ", tipo " + idTipoMetamodeloRef )
	$("#divListaSeleccionReferencia").data("idmodelo", idModelo);
	$("#divListaSeleccionReferencia").data("idtipometamodelofef", idTipoMetamodeloRef);
	$("#divListaSeleccionReferencia").data("referenciaselector", referenciaSelector);
	$("#divListaSeleccionReferencia").data("idobjeto", null);
	$("#divListaSeleccionReferencia").data("nombreobjeto", null);
	$("#divListaSeleccionReferencia").html("");
	$.post( PREFIJO + "/objetos4Seleccion" + SUBFIJO , {"idModelo" : idModelo, "idTipoMetamodelo" : idTipoMetamodeloRef } ,function(data,status){
		if(status == "success"){
			$("#divListaSeleccionReferencia").append("<div class=\"filaSeleccionRegistro\"><input type=\"radio\" name=\"idObjeto\" value=\"\" data-nombreobjeto=\"\"><span>-Ninguno-</span><span>-Ninguno-</span></div>");
			for(var indiceObjeto = 0; indiceObjeto < data.registros.length; indiceObjeto ++){
				var objetoModelo = data.registros[indiceObjeto];
				$("#divListaSeleccionReferencia").append("<div class=\"filaSeleccionRegistro\"><input type=\"radio\" name=\"idObjeto\" value=\"" + objetoModelo.idObjeto + "\" data-nombreobjeto=\"" + objetoModelo.nombre + "\"><span>" + objetoModelo.nombre + "</span><span>" + objetoModelo.nombrePadre + "</span></div>");
			}
			$("#divListaSeleccionReferencia").find("input").click(function(){
				$("#divListaSeleccionReferencia").data( "idobjeto", $(this).val() );
				$("#divListaSeleccionReferencia").data( "nombreobjeto", $(this).data("nombreobjeto") );
			});
			
			xmd_mostrarPantalla("#frmSeleccionarReferencia");
			
		} else {
			alert("Error al obtener listado de objetos para Seleccion");
		}
	});
}

function xmd_aSeleccionarReferencia_click(){
	var etiqueta = $("#divListaSeleccionReferencia").data("referenciaselector").prev();
	var escondido = etiqueta.prev();
	etiqueta.val( $("#divListaSeleccionReferencia").data("nombreobjeto") );
	escondido.val( $("#divListaSeleccionReferencia").data("idobjeto") );
	
	xmd_mostrarPantalla( "#frmEditarObjetoModelo" );

}

function xmd_aCancelarSeleccionarReferencia_click(){

	xmd_mostrarPantalla( "#frmEditarObjetoModelo" );
	
}

var xmd_importarModelo_click = function(){
  
  //$("#frmImportarModelo").show();
  
  mostrarGuardar( false, {"idModelo":null}, null , function(path,datosExtra){
    $("#divProtector").show();
    //alert("importa desde " + path);
    
    $.post( PREFIJO + "/importarModelo" + SUBFIJO , {"nombreArchivo":path} ,function(data,status){
      if(status == "success"){
        if(data.estado != 0 || isNaN(data.idModelo)){
          alert("Ha ocurrido un error al importar el modelo");
        }else{
          xmd_desplegarModelo(data.idModelo);
          alert("Importacion Exitosa");
        }
      }else{
        alert("La aplicacion no responde");
      }
      $("#divProtector").hide();
    } );
    
  } );
  
};

var xmd_exportarModelo_click = function(){
  var idModelo = $(this).parent().parent().data("idModelo");
  
  mostrarGuardar( true, {"idModelo":idModelo}, $("#divModelView").data("nombreModelo")+".txt" , function(path,datosExtra){
    $("#divProtector").show();
    //alert("exporta "+ datosExtra["idModelo"] + " a "+ path);
    
    $.post( PREFIJO + "/exportarModelo" + SUBFIJO, {"idModelo": datosExtra["idModelo"] ,"path":path} ,function(data,status){
      if(status == "success"){
        alert("Exportacion Exitosa");
      }else{
        alert("La aplicacion no responde");
      }
      $("#divProtector").hide();
    } );
    
  } );
  
};

function xmd_desplegarGeneradores( listaGeneradores , idModelo ){
  //alert("idModelo"+idModelo);
  $("#frmGenerador").find("input[name='idModelo']").val(idModelo)
  var ul = $("#frmGenerador").find(".listaGeneradores");
  ul.html("");
  for(var i =0; i< listaGeneradores.__lista.length ;i++ ){
    var li = $("<li></li>");
    var input1 = $("<input></input>");
    input1.attr("type","radio");
    input1.attr("name","idGenerador");
    input1.val( listaGeneradores.__lista[i].idGenerador );
    input1.data( "extension" , listaGeneradores.__lista[i].extension )
    li.append(input1);
    li.append( listaGeneradores.__lista[i].nombreGenerador );
    ul.append(li);
  }
  
  xmd_mostrarPantalla( "#frmGenerador" );
  
}


var xmd_getGeneradores_click = function(){
  var idModelo = $(this).parent().parent().data("idModelo");
  $("#divProtector").show();
  
  $.post( PREFIJO + "/getGeneradores" + SUBFIJO ,{"idModelo":idModelo},function(data,status){
    if(status == "success"){
      try{
        //despliega formulario Atributos
        xmd_desplegarGeneradores(data,idModelo)
      }catch(ex){
        alert(ex.message);
      }
    }else{
      alert("La aplicacion no responde");
    }
    $("#divProtector").hide();
  });
  
};

var timerGeneracion = null;

function xmd_generarModelo(){
  var seleccionado = $("#frmGenerador").find("input:radio[name='idGenerador']:checked").val();
  if(seleccionado === undefined){
      alert("Debe seleccionar un Generador.");
  }else{
    var nombreArchivo =  $("#divModelView").data("nombreModelo") +"."+ $("#frmGenerador").find("input:radio[name='idGenerador']:checked").data("extension");
    
    xmd_mostrarPantalla( "#divModelView" );
    
    var idModelo = $("#frmGenerador").find("input[name='idModelo']").val();
  
    mostrarGuardar( true, {"idModelo":idModelo,"idGenerador":seleccionado}, nombreArchivo, function(path,datosExtra){
      $("#divProtector").show();
      //alert("genera "+ datosExtra["idGenerador"] +" en modelo "+ datosExtra["idModelo"] + " a "+ path);
    
      $.post(PREFIJO + "/crearEventoGeneracion" + SUBFIJO, {"idModelo": datosExtra["idModelo"] , "idGenerador":datosExtra["idGenerador"] ,"nombreArchivo":path} ,function(data,status){
        $("#divProtector").hide();
        if(status == "success"){
          alert("Generacion Exitosa");
        }else{
          alert("La aplicacion no responde");
        }
      } );
    
    } );
    
    //$("#frmGenerador").submit();
    //$("#frmDesplegarContenido").show();
  }
}

var xmd_cerrarModelo_click = function(){
  if( confirm( "Desea cerrar este Modelo?") ){
    $("#divModelView").find("ul:first").html("");
    
    xmd_mostrarPantalla( "#divMenuPrincipal" );
    
  }
};

var xmd_expansor_click =function(){
  var liLista = $(this).parent().parent();
  // var ul = $(this).parent().siblings("ul:first");
  var ul = liLista.children("ul:first");
  if($(this).html() == DESPLEGADO){
    ul.slideUp();
    $(this).html(REPLEGADO);
  }else{
    if(ul.length == 0){
      ul=$("<ul style=\"padding-left:20px;\" class='panel-body'></ul>");
      var li=$("<li></li>");
      li.append("Cargando...");
      ul.append(li);
      liLista.append(ul);
      //alert("xxxx");
      
      var liObjeto = liLista.parent().parent();
      var idJerarquia = liLista.data("idJerarquia");
      var idObjeto = liObjeto.data("idObjeto");
      xmd_desplegarLista(idObjeto, idJerarquia);
    }
    ul.slideDown();
    $(this).html(DESPLEGADO);
  }
};

var xmd_linkPropiedades_click = function(){
  var liObjeto = $(this).parent().parent();
  var idObjeto = liObjeto.data("idObjeto");
  $("#divProtector").show();
  $.post(PREFIJO + "/getAtributosObjeto" + SUBFIJO, {"idObjeto":idObjeto},function(data,status){
    if(status == "success"){
      try{
        //despliega formulario Atributos
        xmd_desplegarAtributos(data)
      }catch(ex){
        alert(ex.message);
      }
    }else{
      alert("La aplicacion no responde");
    }
    $("#divProtector").hide();
  });
  
}

var xmd_anadirHijo_click = function(){
  var liLista = $(this).parent().parent();
  var nombreObjeto = prompt("Ingrese nombre para nuev@ "+liLista.data("idTipoMetamodelo"));
  if(nombreObjeto != null && nombreObjeto.trim() != ""){
    var liObjeto=liLista.parent().parent();
    var idObjetoPadre = liObjeto.data("idObjeto");
    var idJerarquia = liLista.data("idJerarquia");
    //alert("crear objeto "+nombreObjeto+" bajo el listado "+idJerarquia+" del objeto "+idObjetoPadre);
    $("#divProtector").show();
    $.post(PREFIJO + "/crearObjetoHijo" + SUBFIJO, {"idObjetoPadre":idObjetoPadre,"idJerarquia":idJerarquia,"nombre":nombreObjeto.trim()},function(data,status){
      if(status == "success"){
        try{
          xmd_desplegarLista(data.idObjetoPadre, data.idJerarquia);
        }catch(ex){
          alert(ex.message);
        }
      }else{
        alert("La aplicacion no responde");
      }
      $("#divProtector").hide();
    });
  }
}
  
var xmd_eliminarNodo_click = function(){
    //alert("elimina nodo" );
    var nodos = $(this).parent().parent();
    var idObjeto = nodos.data("idObjeto");
    var nombreObjeto = nodos.find("span:first").text();
    nodos = nodos.parent().parent();
    var idJerarquia = nodos.data("idJerarquia");
    nodos = nodos.parent().parent();
    var idObjetoPadre = nodos.data("idObjeto");
    if( confirm("Desea eliminar \""+nombreObjeto+"\"?") ){
      $("#divProtector").show();
      $.post( PREFIJO + "/eliminarObjeto" + SUBFIJO, {"idObjeto":idObjeto} ,function(data,status){
        if(status == "success"){
          if(data == "1"){
            alert(nombreObjeto + " eliminado");
            try{
              xmd_desplegarLista(idObjetoPadre, idJerarquia);
            }catch(ex){
              alert(ex.message);
            }
          }else{
            alert("Ha ocurrido un error al eliminar el objeto");
          }
        }else{
          alert("La aplicacion no responde");
        }
        $("#divProtector").hide();
      });
      //alert("eliminado "+idObjeto+":"+idJerarquia+":"+idObjetoPadre);
    }
  };
  
var xmd_moverArriba_click = function(){
    //alert("elimina nodo" );
    var nodos = $(this).parent().parent();
    var idObjeto = nodos.data("idObjeto");
    var nombreObjeto = nodos.find("span:first").text();
    nodos = nodos.parent().parent();
    var idJerarquia = nodos.data("idJerarquia");
    nodos = nodos.parent().parent();
    var idObjetoPadre = nodos.data("idObjeto");
    $("#divProtector").show();
    $.post(PREFIJO + "/moverObjeto" + SUBFIJO, {"idObjeto":idObjeto,"moverArriba":1} ,function(data,status){
      if(status == "success"){
        if(data == "1"){
          try{
            xmd_desplegarLista(idObjetoPadre,idJerarquia);
          }catch(ex){
            alert(ex.message);
          }
        }else{
          alert("Ha ocurrido un error al mover el objeto");
        }
      }else{
        alert("La aplicacion no responde");
      }
      $("#divProtector").hide();
    });
    //alert("eliminado "+idObjeto+":"+idJerarquia+":"+idObjetoPadre);
  };
  
var xmd_moverAbajo_click = function(){
    //alert("elimina nodo" );
    var nodos = $(this).parent().parent();
    var idObjeto = nodos.data("idObjeto");
    var nombreObjeto = nodos.find("span:first").text();
    nodos = nodos.parent().parent();
    var idJerarquia = nodos.data("idJerarquia");
    nodos = nodos.parent().parent();
    var idObjetoPadre = nodos.data("idObjeto");
    $("#divProtector").show();
    $.post( PREFIJO + "/moverObjeto" + SUBFIJO, {"idObjeto":idObjeto,"moverArriba":0} ,function(data,status){
      if(status == "success"){
        if(data == "1"){
          try{
            xmd_desplegarLista(idObjetoPadre,idJerarquia);
          }catch(ex){
            alert(ex.message);
          }
        }else{
          alert("Ha ocurrido un error al mover el objeto");
        }
      }else{
        alert("La aplicacion no responde");
      }
      $("#divProtector").hide();
    });
    //alert("eliminado "+idObjeto+":"+idJerarquia+":"+idObjetoPadre);
  };

function xmd_getNodoObjeto(objetoModelo){
  //alert("arma nodo para "+ objetoModelo.nombre);
  var li = $("<li></li>");
  var p = $("<p></p>");
  var span = $("<span></span>");
  var ul = $("<ul style=\"padding-left:2em;\"></ul>");
  span.text(objetoModelo.nombre);
  p.addClass("nodoArbol");
  p.append("<button class=\"expansor\">"+REPLEGADO+"</button>");
  p.append(span);
  p.append("<button class=\"linkPropiedades\">&equiv;</button> <button class=\"moverArriba\">&#x25B2;</button> <button class=\"moverAbajo\">&#x25BC;</button> <button class=\"eliminarNodo\">&#x274C;</button>");
  
  for(var i = 0; i< objetoModelo._jerarquias.length; i++){
    var jerarquia = objetoModelo._jerarquias[i];
    var li1 = xmd_getNodoObjeto(jerarquia);
    ul.append(li1);
  }
  //alert("Elemento Listas "+ objetoModelo.x_listas[0] );
  for(var i = 0; i < objetoModelo._listas.length ; i++){
    var lista = objetoModelo._listas[i];
    var li1 = $("<li class='panel'></li>");
    var p1 = $("<p class='panel-heading'></p>");
    var span1 = $("<span></span>");
    //alert("Elemento Lista"+lista);
    span1.text(lista.idJerarquia);
    p1.addClass("nodoArbol");
    p1.append("<button class=\"expansor\">"+REPLEGADO+"</button>");
    p1.append(span1);
    p1.append("<button class=\"anadirHijo\">"+ICON_AGREGAR+"</button>");
    li1.append(p1);
    li1.data("idJerarquia",lista.idJerarquia);
    li1.data("idTipoMetamodelo",lista.idTipoMetamodeloHijo);
    li1.attr("id","o_"+objetoModelo.idObjeto+"_l_"+lista.idJerarquia);
    ul.append(li1);
  }
  li.append(p,ul);
  li.data("idObjeto",objetoModelo.idObjeto);
  li.data("idTipoMetamodelo",objetoModelo.idTipoMetamodelo);
  ul.hide();
  return li;
}

function xmd_cargarCatalogos( idModelo ){
	//alert('Cargando catalogos');
	$.post(PREFIJO + "/catalogos" + SUBFIJO, {idModelo : idModelo} ,function(data,status){
		if(status == "success"){
			CATALOGOS = data;
			alert('catalogos cargados');
		}else{
			alert("error al Cargar Catalogos");
		}
	});
}

//despliega un modelo
function xmd_desplegarModelo(idModelo){
  //alert("Despliega Modelo "+idModelo);
  
  //recupera objetoRaiz de Modelo
  $.post(PREFIJO + "/getRaizModelo" + SUBFIJO,{"idModelo":idModelo},function(data,status){
        if(status == "success"){
          //alert(data.toString());
          
          $("#divModelView").data("idModelo",idModelo);
          $("#divModelView").data("nombreModelo",data["nombre"]);
          
          $("#divModelView").html("");
          var divToolBar = $("<div></div>");
          divToolBar.addClass("barraBotones");
          
          /*
          var aExportar = $("<button></button>");
          aExportar.addClass("exportarModelo");
          aExportar.addClass("boton");
          aExportar.text("Exportar...");
          divToolBar.append( aExportar );
          */
          
          var aGenerar = $("<button></button>");
          aGenerar.addClass("generarModelo");
          aGenerar.addClass("boton");
          aGenerar.text("Generar...");
          divToolBar.append( aGenerar );
          
          var aCerrarModelo = $("<button></button>");
          aCerrarModelo.addClass("cerrarModelo");
          aCerrarModelo.addClass("boton");
          aCerrarModelo.text("Cerrar Modelo");
          divToolBar.append( aCerrarModelo );
          
          $("#divModelView").append(divToolBar);
          
          var ul = $("<ul style=\"padding-left:20px;\"></ul>");
          ul.append( xmd_getNodoObjeto(data) );
          
          $("#divModelView").append(ul);
          
          $("#divModelView").find(".expansor").click(xmd_expansor_click);
          $("#divModelView").find(".anadirHijo").click(xmd_anadirHijo_click);
          $("#divModelView").find(".linkPropiedades").click(xmd_linkPropiedades_click);
          
          $("#divModelView").find(".exportarModelo").click(xmd_exportarModelo_click);
          $("#divModelView").find(".generarModelo").click( xmd_getGeneradores_click );
          $("#divModelView").find(".cerrarModelo").click( xmd_cerrarModelo_click );
          
          $("#divModelView").find(".eliminarNodo").hide();
          $("#divModelView").find(".moverArriba").hide();
          $("#divModelView").find(".moverAbajo").hide();

          $("#frmCrearModelo").hide();
          $("#frmAbrirModelo").hide();
          $("#divMenuPrincipal").hide();
          $("#divModelView").show();
          
          xmd_cargarCatalogos( idModelo );
          
        }else{
          alert(status);
        }
        $("#divProtector").hide();
      });
      
}

function xmd_eliminarObjetoModelo(idObjeto){
  $("#frmEliminarObjetoModelo").hide();
}

function xmd_guardarObjetoModelo(){
  //itera cada atributo
  var peticion = new Object();
  
  peticion.__idObjeto = $("#frmEditarObjetoModelo").find("input[name='idObjeto']").val();
  peticion.__nombre = $("#frmEditarObjetoModelo").find("input[name='nombreObjeto']").val();
  peticion.__descripcion = $("#frmEditarObjetoModelo").find("input[name='descripcion']").val();
  
  
  var atributos = $("#frmEditarObjetoModelo").find(".contenidoVinetasEditor").find("input,select").toArray();
  
  for( var i=0 ; i< atributos.length ; i++){
    var atributo = atributos[i];
    if( atributo.name.endsWith("_xmdetiqueta") ){
    	continue;
    }
	//alert("leyendo atributo " + atributo.name);
    peticion[ atributo.name ] = atributo.value;	

    
  }
  
  
  $("#divProtector").show();
  
  $.post(PREFIJO + "/actualizarAtributos" + SUBFIJO, peticion ,function(data,status){
    if(status == "success"){
      try{
        if(data.__errorCode == 0){
          xmd_desplegarLista(data.idObjetoPadre,data.idJerarquia);
          
          xmd_mostrarPantalla( "#divModelView" );
          
        }else{
          $(".mensajeError").text("");
          for(var i=0; i< data.__mensajes.length; i++){
            $("#msg_"+ data.__mensajes[i].idAtributoMetamodelo ).text( data.__mensajes[i].mensaje );
          }
          alert("Se han encontrado valores no validos");
        }
      }catch(ex){
        alert(ex.message);
      }
    }else{
      alert("La aplicacion no responde");
    }
    $("#divProtector").hide();
  });
  
}

function xmd_desplegarParches(parches){
  var ul = $("#frmParches_ul");
  ul.html("");
  if(parches.__lista.length == 0){
    ul.append("No se encontraron parches disponibles.");
  }
  for(var i =0; i< parches.__lista.length ;i++ ){
    var li = $("<li></li>");
    var input1 = $("<input></input>");
    input1.attr("type","radio");
    input1.attr("name","archivoParche");
    input1.val( parches.__lista[i].archivoParche );
    li.append(input1);
    li.append( parches.__lista[i].archivoParche );
    ul.append(li);
  }
  
  xmd_mostrarPantalla( "#frmParches" );
  
}

function xmd_cargarParches(){
  var checkIncluirAplicados = $("#frmParches").find("input:checkbox[name='incluirAplicados']:checked").val();
  if( checkIncluirAplicados != "1"){
    checkIncluirAplicados = "0";
  }
  //alert( checkIncluirAplicados);
  $.post(PREFIJO + "/getParches" + SUBFIJO,{"incluirAplicados": checkIncluirAplicados },function(data,status){
    if(status == "success"){
      try{
        xmd_desplegarParches(data)
      }catch(ex){
        alert(ex.message);
      }
    }else{
      alert("La aplicacion no responde");
    }
  });
}

function xmd_aplicarParcheSeleccionado(){
  var archivoParche = $("#frmParches").find("input:radio[name='archivoParche']:checked").val();
  if(archivoParche === undefined){
    alert("Debe seleccionar un Parche");
    return;
  }
  $.post(PREFIJO + "/verificarParche" + SUBFIJO, {"archivoParche":archivoParche},function(data,status){
    if(status == "success"){
      try{
        if(data.aplicado){
          if(!confirm("Este parche ya fue sido aplicado previamente.\nConfirma la aplicacion de este parche?")){
            return;
          }
        }else{
          if(!confirm("Confirma la aplicacion de este parche?\n"+archivoParche)){
            return;
          }
        }
        
        $.post("/aplicarParche.html",{"archivoParche":archivoParche},function(data1,status1){
          if(status1 == "success"){
          
            try{
              var resultado = parseInt(data1);
              if(resultado==1){
                alert("Parche Aplicado Exitosamente");
              }else{
                alert("Parche Aplicado con Error "+data1);
              }
    
            }catch(ex){
              alert("Parche aplicado con error\n"+data1 );
            }
            
          }else{
            alert("La aplicacion no responde");
          }
          
          xmd_mostrarPantalla( "#frmMantenimiento" );
          
        });
        
      }catch(ex){
        alert(ex.message);
      }
    }else{
      alert("La aplicacion no responde");
    }
  });
}

function xmd_mostrarAbrir(selectHandler){
  
}

var xmd_aCrearModelo_click = function(){
    $("#divProtector").show();
    $.get(PREFIJO + "/metamodelos" + SUBFIJO,function(data,status){
      if(status == "success"){
        //alert(JSON.stringify(data));
        if(data.registros.length > 0){
          $("#divListaMetamodelos").html("");
		  for(var i =0; i< data.registros.length ;i++ ){
		    var div1 = $("<div></div>");
		    
		    var input1 = $("<input></input>");
		    input1.attr("type","radio");
		    input1.attr("name","idMetamodelo");
		    input1.val( data.registros[i].idMetamodelo );
		    
		    var span1 = $("<span></span>");
		    span1.text (data.registros[i].nombreMetamodelo);
		    
		    div1.append(input1);
		    div1.append(span1);
		    
		    $("#divListaMetamodelos").append(div1);
		  }          
        }else{
          $("#divListaMetamodelos").text("No existen Metamodelos Registrados");
        }
        
        xmd_mostrarPantalla( "#frmCrearModelo" );
              
      }else{
        alert(status);
      }
      $("#divProtector").hide();
    });
  };
  


var xmd_aAbrirModelo_click = function(){
    $("#divProtector").show();
    $.get(PREFIJO + "/listaModelos" + SUBFIJO,function(data,status){
      if(status == "success"){
        if(data.registros.length > 0){
          $("#divListaModelos").html("");
          for(var i =0; i< data.registros.length ;i++ ){
          	var div1 = $("<div></div>");
		    
		    var input1 = $("<input></input>");
		    input1.attr("type","radio");
		    input1.attr("name","idModelo");
		    input1.val( data.registros[i].idModelo );
		    
		    var span1 = $("<span></span>");
		    span1.text (data.registros[i].nombre);
		    
		    div1.append(input1);
		    div1.append(span1);
		    
		    $("#divListaModelos").append(div1);
		  }
        }else{
          $("#divListaModelos").text("No se ha encontrado modelos");
        }
        
        xmd_mostrarPantalla( "#frmAbrirModelo" );
        
      }else{
        alert(status);
      }
      $("#divProtector").hide();
    });
  };

var xmd_aSeleccionarMetamodelo_click = function(){
    var seleccionado = $("#frmCrearModelo").find("input:radio[name='idMetamodelo']:checked").val();
    //alert("seleccionado :"+seleccionado);
    if(seleccionado === undefined){
      alert("Debe seleccionar un Metamodelo.");
    }else{
      
      var nombreModelo = prompt("Ingrese un nombre para el nuevo modelo");
      
      xmd_mostrarPantalla( "#divMenuPrincipal" );
      
      if(nombreModelo.trim() == null){
        // usuario cancela creacion de modelo
        alert("Creacion de modelo cancelada");
      }else{
        //se crea el modelo con el nuevo nombre
        //alert("crea modelo con metamodelo " + seleccionado + " de nombre "+ nombreModelo);
        $("#divProtector").show();
        $.post(PREFIJO + "/crearModelo" + SUBFIJO, { idMetamodelo : seleccionado , nombreModelo : nombreModelo } , function(data,status){
          
          if(status == "success"){
            //alert("idmodelo " + data.idModelo);
            if(data.idModelo == "" || isNaN(data.idModelo)){
              alert("Ha ocurrido un error al crear el modelo");
            }else{
              xmd_desplegarModelo(data.idModelo);
            }
          }else{
            alert(status);
          }
          $("#divProtector").hide();
          
        });
        }
      }
    };

var xmd_aSeleccionarModelo_click = function(){
    var seleccionado = $("#frmAbrirModelo").find("input:radio[name='idModelo']:checked").val();
    //alert("seleccionado :"+seleccionado);
    if(seleccionado === undefined){
      alert("Debe seleccionar un Modelo.");
    }else{
      xmd_desplegarModelo(seleccionado);
    }
  };

var xpd_aVerificarExpReg_click = function(){
    var cadena = $("#frmExpReg").find("input[name='cadena']").val();
    var expresion = $("#frmExpReg").find("input[name='expresion']").val();
    try{
      var expReg = new RegExp(expresion);
      if( expReg.test(cadena)){
        alert("cadena cumple con exp reg");
      }else{
        alert(cadena+"\n no cumple con exp reg\n"+expresion);
      }
    }catch(ex){
      alert(ex.message);
    }
  } ;

var xmd_aUnitTesting_click = function(){
    if(confirm("Proceder con la secuencia de Pruebas?")){
      $.get(PREFIJO + "/__test"+subfijo,{ },function(data,status){
        if(status == "success"){
          alert(data.mensaje);
        }else{
          alert(status);
        }
      });
    }
  };

var xmd_aReiniciarBase_click = function(){
    if(confirm("Este procedimiento debe ser realizado solo antes del primer uso\nDesea continuar?")){
        $.post( PREFIJO + "/inicializarBase" + SUBFIJO , {idMetamodelo : 1} , function(data, status){
            if(status == "success"){
                alert(data);
            }else{
                alert(status);
            }
        });
    }
};

$(document).ready(function(){
  try{
  
  //alert('inicia carga');
  
  xmd_mostrarPantalla( "#divMenuPrincipal" );
    
  $("#divModelView").find("ul").html( DESPLEGADO);
  DESPLEGADO = $("#divModelView").find("ul").html();
  $("#divModelView").find("ul").html( REPLEGADO);
  REPLEGADO = $("#divModelView").find("ul").html();
  
  //loadLocalConfig( "/getLocalConfig.html",{"idModelo":1} , $("body") );
  //initFrmFileDialog( $("#frmFileDialog") );
  
  //menu principal
  
  $("#aCrearModelo").click( xmd_aCrearModelo_click );
  
  $("#aAbrirModelo").click( xmd_aAbrirModelo_click );
  
  $("#aMantenimiento , #aCancelarParches , #aCancelarExpReg").click(function(){
      xmd_mostrarPantalla("#frmMantenimiento");
  });
  //dialogo mantenimiento
  
  $("#aCancelarMantenimiento , #aCancelarCrearModelo , #aCancelarAbrirModelo , #aCerrarImportacion" ).click(function(){
    xmd_mostrarPantalla( "#divMenuPrincipal" );
  });
  
  $("#aSeleccionarMetamodelo").click( xmd_aSeleccionarMetamodelo_click );
  
  $("#aReiniciarBase").click( xmd_aReiniciarBase_click );
  
  //dialogo abrir modelo
  
  $("#aSeleccionarModelo").click( xmd_aSeleccionarModelo_click );
  
  //dialogo Eliminar Objeto Modelo
  
  $("#aCancelarEliminarObjetoModelo , #aCancelarEditarObjetoModelo , #aCancelarGenerarModelo , #aCerrarContenido").click(function(){
      xmd_mostrarPantalla( "#divModelView" );
  });
  
  $("#aEliminarObjetoModelo").click(function(){
    xmd_eliminarObjetoModelo(1);
  });
  
  //dialogo editar atributos
  
  $("#aGuardarObjetoModelo").click(function(){
    xmd_guardarObjetoModelo();
  });
  
  //generacion de modelo
  
  $("#aGenerarModelo").click(function(){
    xmd_generarModelo();
  });
  
  $("#aParches").click(function(){
    xmd_cargarParches();
  });
  
  $("#frmParches").find("input[name='incluirAplicados']").change(function(){
    xmd_cargarParches();
  });
  
  $("#aAplicarParche").click(function(){
    xmd_aplicarParcheSeleccionado();
  });
  
  //Expresiones regulares
  $("#aExpReg").click(function(){
    xmd_mostrarPantalla( "#frmExpReg" );
  });
    
  $("#aSeleccionarReferencia").click( xmd_aSeleccionarReferencia_click );
  
  $("#aCancelarSeleccionarReferencia").click( xmd_aCancelarSeleccionarReferencia_click );
  
  $("#aVerificarExpReg").click( xpd_aVerificarExpReg_click );
  
  //$("#aUnitTesting").click( xmd_aUnitTesting_click );
  
  $("#aImportarModelo").click( xmd_importarModelo_click );  
  
  $("#divProtector").hide();
  //alert("jquery cargado6");
  
  }catch( ex){
      alert( ex.message );
  }
  
});
