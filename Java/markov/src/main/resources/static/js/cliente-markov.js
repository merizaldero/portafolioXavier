function aplicarMarkov(userName, idMenu, claseMenuItem){
	
	function extraerClavePagina(ruta){
		var pos = ruta.indexOf('?');
		if(pos >= 0){
			ruta = ruta.substring(0,pos);
		}
		pos = ruta.lastIndexOf('/');
		if(pos >= 0){
			ruta = ruta.substring(pos+1);
		}
		return ruta;
	}
	
	function obtenerRequest(){
		if (window.XMLHttpRequest) {
			// code for modern browsers
			return new XMLHttpRequest();
		} else {
			// code for old IE browsers
			return new ActiveXObject("Microsoft.XMLHTTP");
		}
	}
	
	function enlaceEventHandler( event ){
		
	}
	
	document.addEventListener("load",function(){
		var contenedorMenu = document.getElementById(idMenu);
		if(contenedorMenu == null){
			return;
		}
		var itemsMenu = contenedorMenu.getElementsByClassName(classMenuItem);
		var listaMenu = [];
		var enlace;
		var origen = extraerClavePagina(document.location.pathname);
		for(var indice = 0 ; indice< itemsMenu.length; indice++){
			//Obtiene lista de Items
			var item = itemsMenu[indice];
			enlace = item.getElementsByTagName('a')[0];
			listaMenu[listaMenu.length] = { opcion: extraerClavePagina(enlace.href), item:item, outerHtml = item.outerHTML; probabilidad: 0.0 };
		}
		
		var xmlhttp = obtenerRequest();

		xmlhttp.onreadystatechange = function() {
		    if (this.readyState == 4 && this.status == 200) {
		        var opcionesOrdenandas = JSON.parse(this.responseText);
		        // Atribuye probabilidades obtenidas
		        for(var i = 0 ; i < opcionesOrdenandas.length; i++){
		        	var listaFiltrada = listaMenu.filter((item)=>{return item.opcion == opcionesOrdenandas[i].destino });
		        	if(listaFiltrada.length > 0){
		        		listaFiltrada[0].probabilidad = opcionesOrdenandas[i].probabilidad;
		        	}
		        }
		        // Reordena opciones por probabilidad
		        listaMenu = listaMenu.sort( (a,b) => {return b.probabilidad - a.probabilidad;} );
		        
		        //Vacia menu
		        contenedorMenu.innerHTML = "";
		        
		        // llenaMenu con elementos reordenados
		        for(var i = 0 ; i < listaMenu.length; i++){
		        	contenedorMenu.innerHTML += listaMenu[i].outerHtml;
		        }
		        
		        
		        
		        //Obtiene menus insertados
		        itemsMenu = contenedorMenu.getElementsByClassName(classMenuItem);
		        for(var indice = 0 ; indice< itemsMenu.length; indice++){
		        	var item = itemsMenu[indice];
					enlace = item.getElementsByTagName('a')[0];
					// agrega evento click para elemento a
					enlace.addEventListener("click",function(event){
						
					});
		        }
		    }
		};
		xmlhttp.open('GET', 'http://localhost:8080/opciones/' + userName + '/' + origen , true);
		xmlhttp.send(); 
		
	});
	
}