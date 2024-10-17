var modeladorApp = angular.module('modeladorApp', []);
modeladorApp.controller('modeladorController', function($scope, $http) {
    $scope.currentScreen = "#divMenuPrincipal";
    
    $scope.PREFIJO = "";
    $scope.SUBFIJO = ".html";
    
    $scope.metamodelos = [];
    $scope.modelos = [];
    $scope.modelo = {};
    $scope.pilaObjetosModelo = [];
    $scope.objetoModelo = {};
    $scope.atributos = [];
    $scope.jerarquias =[];
    $scope.listas = [];
    $scope.listaHijos = [];
    $scope.catalogos = {};
    $scope.cambiado = false;
    
    $scope.irAInicio = function(){
        $scope.currentScreen = "#divMenuPrincipal";
    };
    
    // Crear Modelo
    $scope.seleccionarMetamodelo = function( indiceSeleccion ){
        $scope.indiceSeleccionado = indiceSeleccion;
        for( var indice in $scope.metamodelos ){
            $scope.metamodelos[indice].cssSeleccionado = ( indice == indiceSeleccion )?"active":"";
        }
    };
    $scope.crearModelo = function(){
        if ($scope.indiceSeleccionado === undefined || !( $scope.indiceSeleccionado in $scope.metamodelos ) ){
            return;
        }
        var nombreModelo = prompt("Nombre nuevo Modelo");
        if(nombreModelo === undefined || nombreModelo == null || nombreModelo.trim() == ""){
            $scope.irAInicio();
            return;
        }
        var parametros = "idMetamodelo=" + $scope.metamodelos[ $scope.indiceSeleccionado ].idMetamodelo + "&nombreModelo=" + encodeURI(nombreModelo.trim()) ;
        //alert(parametros);
        $http.post( $scope.PREFIJO + '/crearModelo' + $scope.SUBFIJO , parametros ).then( 
            (response) => {
                $scope.cargarModelo(response.data);
            }, 
            ( response ) => {
                alert("Error al crear Modelo");
                $scope.irAInicio();
            });
    };
    
    $scope.mostrarCrearModelo = function(){
    
        $http.get( $scope.PREFIJO + '/metamodelos' + $scope.SUBFIJO ).then( 
            (response) => {
                $scope.metamodelos = response.data.registros;
                for( var indice in $scope.metamodelos ){
                    $scope.metamodelos[indice].cssSeleccionado = "";
                }
                $scope.currentScreen = "#frmCrearModelo";
            }, 
            ( response ) => {
                alert("Error al obtener metamodelos");
            });
            
    };
    
    // Abrir Modelo
    
    $scope.mostrarAbrirModelo = function(){
        $http.get( $scope.PREFIJO + '/listaModelos' + $scope.SUBFIJO ).then( 
            (response) => {
                $scope.modelos = response.data.registros;
                for( var indice in $scope.modelos ){
                    $scope.modelos[indice].cssSeleccionado = "";
                }
                $scope.currentScreen = "#frmAbrirModelo";
            }, 
            ( response ) => {
                alert("Error al obtener modelos");
            });
    };
    $scope.seleccionarModelo = function( indiceSeleccion ){
        $scope.indiceSeleccionado = indiceSeleccion;
        for( var indice in $scope.modelos ){
            $scope.modelos[indice].cssSeleccionado = ( indice == indiceSeleccion )?"active":"";
        }
    };
    $scope.abrirModelo = function(){
        if ($scope.indiceSeleccionado === undefined || !( $scope.indiceSeleccionado in $scope.modelos ) ){
            return;
        }
        $scope.cargarModelo( $scope.modelos[ $scope.indiceSeleccionado ] );
        
    };
    
    $scope.cargarModelo = function( modelo ){
        //alert("cargando modelo " + JSON.stringify(modelo));
        $scope.modelo = modelo;
        var parametros = "idModelo=" + modelo.idModelo ;
        $http.post( $scope.PREFIJO + '/getRaizModelo' + $scope.SUBFIJO , parametros ).then( 
            (response) => {
                $scope.cargarObjetoModelo( response.data );
            }, 
            ( response ) => {
                alert("Error al cargar modelo");
            });
        $scope.cargarCatalogos( modelo.idModelo );
    };
    
    $scope.onCambiarCampo = function(){
        $scope.cambiado = true;
    };
    
    $scope.cssCambiado = function(cambiado,noCambiado){
        return ($scope.cambiado)?cambiado:noCambiado;
    };
    
    $scope.cargarObjetoModelo = async function( objetoModelo ){
        //alert("cargando objetoModelo " + JSON.stringify(objetoModelo));
        $scope.objetoModelo = objetoModelo;
        
        let parametros = "idObjeto=" + objetoModelo.idObjeto ;

        //recupero ancestros
        
        $http.post( $scope.PREFIJO + '/getAncestrosObjeto' + $scope.SUBFIJO , parametros ).then(
            (response)=>{
                $scope.pilaObjetosModelo = response.data.lista;
            },(response_error)=>{
                alert("No se pudo recuperar ancestros");
                $scope.pilaObjetosModelo = [];
            });

        //recupero atributos
        $http.post( $scope.PREFIJO + '/getAtributosObjeto' + $scope.SUBFIJO , parametros ).then( 
            (response) => {
                
                $scope.jerarquias = response.data._jerarquias;
                $scope.listas = response.data._listas;
                $scope.listaHijos = [];
                $scope.cambiado = false;
        
                $scope.atributos = response.data._atributos;
                
                //alert('aqui llego al cargar atributos');
                
                for(var indice in $scope.atributos ){
                    $scope.atributos[indice].mensajeError = null;

                }

                // marco primera lista como activa y despliego su contenido
                if($scope.listas.length > 0){
                    $scope.cargarLista(0);
                }
                
                //alert( "cargado atributos " + JSON.stringify( $scope.atributos ) );
                $scope.currentScreen = "#divModelView";
            }, 
            (response) => {
                $scope.atributos = []
                alert("Error al cargar modelo");
            });
        
    };
    
    $scope.cargarLista = function(indice){
    
        var parametros = "idObjeto=" + $scope.objetoModelo.idObjeto + "&idJerarquia=" + $scope.listas[indice].idJerarquia ;
        $http.post( $scope.PREFIJO + '/getObjetosByPadre' + $scope.SUBFIJO , parametros ).then( 
            (response) => {
                for( var indiceLista in $scope.listas){
                    $scope.listas[indiceLista].cssSeleccionado = (indiceLista == indice)?"active bg-active":"";
                }
                $scope.listaHijos = response.data.lista;
                //alert( "cargada lista " + JSON.stringify( $scope.listaHijos ) );
            }, 
            (response) => {
                $scope.listaHijos = [];
                alert("Error al cargar lista de hijos");
            });
    };
    
    $scope.cargarCatalogos = function(idModelo){
        var parametros = "idModelo=" + idModelo ;
        $http.post( $scope.PREFIJO + '/catalogos' + $scope.SUBFIJO , parametros ).then( 
            (response) => {
                $scope.catalogos = response.data;
                //alert( "cargado catalogos " + JSON.stringify( $scope.catalogos ) );
            }, 
            ( response ) => {
                alert("Error al cargar catalogos");
            });
    };
    
    $scope.obtenerMaxLength = function(atributo){
        if( atributo.longitudAtributo ==  0 ){
           if( atributo.idTipoPrimitivo == "INTEGER"){
               return 5;
           } else if( atributo.idTipoPrimitivo == "LONG"){
               return 10;
           } else {
               return 64;
           }
        } else {
            return atributo.longitudAtributo;
        }
    };
    
    $scope.guardarObjetoModelo = function(){
        return new Promise(function(aceptar , rechazar){
            if($scope.cambiado){
                //alert("sí, he cambiado");
            }else{
                //alert("no he cambiado");
                aceptar();
                return;
            }
            // codifica inputs para guardado
            var parametros = "__idObjeto="     + encodeURI( $scope.objetoModelo.idObjeto ) 
                           + "&__nombre="      + encodeURI( $scope.objetoModelo.nombre )
                           + "&__descripcion=" + encodeURI( $scope.objetoModelo.descripcion );
            for(var indice in $scope.atributos){
                parametros += "&" + $scope.atributos[indice].idAtributoMetamodelo + "=" + encodeURI( $scope.atributos[indice].valor );
            }
            $http.post( $scope.PREFIJO + '/actualizarAtributos' + $scope.SUBFIJO , parametros ).then( 
              (response) => {
                if( response.data.__errorCode == 0){
                    $scope.cambiado = false;
                    aceptar();
                } else {
                    //alert("Errores " + JSON.stringify(response.data.__mensajes));
                    alert('Los campos están incorrectos. Verificar');
                    var mensajesError;
                    for( var indice in $scope.atributos ){
                        mensajesError = response.data.__mensajes.filter( item => {return item.idAtributoMetamodelo == $scope.atributos[indice].idAtributoMetamodelo ;} );
                        $scope.atributos[indice].mensajeError = (mensajesError.lenght > 0) ? mensajesError[0].mensaje : null;
                    }
                    rechazar();
                }
              }, 
              ( response ) => {
                alert("Error al cargar guardar");
                rechazar();
              });
        });
    };
    
    $scope.mostrarObjetoModeloPila = function( indice ){
        var objetoModelo = $scope.pilaObjetosModelo[indice];
        $scope.cargarObjetoModelo( objetoModelo );
    };
    
    $scope.moverObjeto = function( objetoModelo, moverArriba ){
        var parametros = "idObjeto=" + objetoModelo.idObjeto + "&moverArriba=" + moverArriba ;
        //alert(parametros);
        $http.post( $scope.PREFIJO + '/moverObjeto' + $scope.SUBFIJO , parametros ).then( 
            (response) => {
                for( var indice in $scope.listas ){
                    if( $scope.listas[indice].cssSeleccionado != "" ){
                        $scope.cargarLista(indice);
                        break;
                    }
                }
            }, 
            ( response ) => {
                alert("Error al cargar modelo");
            });
    };
    
    $scope.crearHijo = function(){
        
        var listaActual = $scope.listas.filter( item=>{return item.cssSeleccionado != ""} )[0];
        var nombreObjeto = prompt("Ingrese nombre para nuev@ " + listaActual.idTipoMetamodelo);
        if(nombreObjeto === undefined || nombreObjeto == null || nombreObjeto.trim() == ""){
            return;
        }
        var parametros = "idObjetoPadre=" + encodeURI($scope.objetoModelo.idObjeto) + "&idJerarquia=" + encodeURI(listaActual.idJerarquia) + "&nombre=" + encodeURI(nombreObjeto.trim());
        $http.post( $scope.PREFIJO + '/crearObjetoHijo' + $scope.SUBFIJO , parametros ).then( 
             (response) => {
                 $scope.cargarLista( $scope.listas.indexOf(listaActual) );
             }, ( response ) => {
                 alert("Error al cargar modelo");
             }
        );
    };
    
    $scope.abrirHijo = function(objetoModeloHijo){
        $scope.guardarObjetoModelo().then(
            ()=>{
                $scope.cargarObjetoModelo(objetoModeloHijo);
            },()=>{
            }
        );
    };

    $scope.opcionesReubicacion=[];

    $scope.mostrarOpcionesReubicacionObjetoModelo = ()=>{
        const parametros = "idObjeto="+ $scope.objetoModelo.idObjeto;
        $http.post( $scope.PREFIJO + '/getOpcionesReubicacion' + $scope.SUBFIJO , parametros ).then(
            (response)=>{
                $scope.opcionesReubicacion = response.data.lista;
                $scope.currentScreen = "#frmSeleccionarPadre";
            },(response_err)=>{
                alert("No se pudo obtener opciones de validacion");
            }
        );
    };

    $scope.seleccionarNuevoPadre = (indice)=>{
        const nuevoPadre = $scope.opcionesReubicacion[indice];
        if(nuevoPadre.idObjeto == $scope.objetoModelo.idObjetoPadre){
            alert("Ya es Padre actual");
            return;
        }
        const parametros = "idObjeto="+ $scope.objetoModelo.idObjeto + "&idObjetoPadre=" + nuevoPadre.idObjeto + "&idJerarquia=" + nuevoPadre.idJerarquia ;
        $http.post( $scope.PREFIJO + '/setObjetoModeloPadre' + $scope.SUBFIJO , parametros ).then(
            (response)=>{
                $scope.cargarObjetoModelo($scope.objetoModelo);
            },(response_err)=>{
                alert("No se pudo reubicar Objeto");
                $scope.cargarObjetoModelo($scope.objetoModelo);
            }
        );
    };
    
    $scope.eliminarObjetoModelo = function(){
        if(! confirm( "Desea eliminar " + $scope.objetoModelo.nombre + " ?" ) ){
            return;
        }
        var parametros = "idObjeto=" + $scope.objetoModelo.idObjeto;
        $http.post( $scope.PREFIJO + '/eliminarObjeto' + $scope.SUBFIJO , parametros ).then( 
             (response) => {
                 $scope.mostrarObjetoModeloPila( $scope.pilaObjetosModelo.length - 1 );
             }, ( response ) => {
                 alert("Error al cargar modelo");
             }
        );
    };
    
    $scope.exportarModelo = function(){
        
        $scope.guardarObjetoModelo().then(
            ()=>{
                alert("Se procede con descarga");
                var forma = document.getElementById("frmExportarModelo");
                forma.idModelo.value = $scope.objetoModelo.idModelo;
                forma.submit();
            },()=>{
            }
        );
        
    };
    
    // Validar Modelo
    
    $scope.frmValidaciones = {
        lista:[],
        puedeGenerar : function(){
            var listaDanger = this.lista.filter( item => { return item.nivel == 'danger'; });
            return (listaDanger.length == 0);
        }
    };
    
    $scope.validarModelo = function(){
        $scope.guardarObjetoModelo().then(
            ()=>{
                var parametros = "idModelo=" + encodeURI($scope.modelo.idModelo) ;
                $http.post( $scope.PREFIJO + '/validarModelo' + $scope.SUBFIJO , parametros ).then( 
                    (response) => {
                        //alert('he validado');
                        $scope.frmValidaciones.lista = response.data.lista ;
                        $scope.currentScreen = "#divValidacion";
                    }, ( response ) => {
                        alert("Error al validar modelo");
                    }
                );
            },()=>{
                alert("error en grabacion de objeto");
            }
        );
    };
    
    $scope.seleccionarValidacion = function(indice){
        try{
            $scope.cargarObjetoModelo($scope.frmValidaciones.lista[indice]);
        }catch(ex){
            alert(ex.message);
        }
    };
    
    // Generacion de codigo
    
    $scope.frmGeneracion = {
        generadores : [],
        archivos : []
    };
    
    $scope.mostrarGeneradores = function(){
        var parametros = "idModelo=" + $scope.modelo.idModelo;
        $http.post( $scope.PREFIJO + '/getGeneradores' + $scope.SUBFIJO , parametros ).then( 
             (response) => {
                 if ('lista' in response.data){
                     $scope.frmGeneracion.generadores = response.data.lista;
                     $scope.currentScreen = "#divGeneradores";
                 }else{
                     alert("Error al obtener generadores");
                 }
             }, ( response ) => {
                 alert("Error al cargar generadores");
             }
        );
    };
    
    $scope.generarCodigo = function(indice){
        
        var parametros = "idModelo=" + $scope.modelo.idModelo + "&idGenerador=" + encodeURI( $scope.frmGeneracion.generadores[indice].idGenerador );
        $http.post( $scope.PREFIJO + '/generarModelo' + $scope.SUBFIJO , parametros ).then( 
             (response) => {
                 if ('archivos' in response.data){
                     $scope.frmGeneracion.archivos = response.data.archivos;
                     $scope.currentScreen = "#frmDesplegarContenido";
                 }else if ('error' in response.data){
                     alert('py: ' + response.data.error);
                 }else{
                     alert("Error al cargar codigo");
                 }
             }, ( response ) => {
                 alert("Error al cargar codigoo");
             }
        );
        
    };
    
    // Mantenimiento
    
    $scope.crearBaseDatos = function(){
        if(confirm("Este procedimiento debe ser realizado solo antes del primer uso\nDesea continuar?")){
            var parametros ="idMetamodelo=1";
            $http.post( $scope.PREFIJO + '/inicializarBase' + $scope.SUBFIJO , parametros).then( 
            (response) => {
                alert(response.data);
            }, 
            ( response ) => {
                alert(response.status);
            });
        }
    };
    $scope.regenerarMetamodelo = function(){
        if(confirm("Se procederá a regenerar Metamodelo. \nDesea continuar?")){
            var parametros ="idMetamodelo=1";
            $http.post( $scope.PREFIJO + '/regenerarMetamodelo' + $scope.SUBFIJO , parametros).then( 
            (response) => {
                alert(response.data);
            }, 
            ( response ) => {
                alert(response.status);
            });
        }
    };
    $scope.ejecutarPruebasUnitarias = function(){
        if(confirm("Proceder con la secuencia de Pruebas?")){
            $http.get( $scope.PREFIJO + '/__test' ).then( 
            (response) => {
                alert(response.data);
            }, 
            ( response ) => {
                alert(response.status);
            });
        }
    };
    
    $scope.frmExpresionesRegulares = { expresion:"" , texto:"" , expresionValida:false, textoMatchs:false };
    
    $scope.mostrarMantenimiento = function(){
        $scope.currentScreen = "#frmMantenimiento";
    }
    
    $scope.mostrarExpresionesRegulares = function(){
        $scope.currentScreen = "#frmExpReg";
    };
    
    $scope.evaluarExpReg = function(){
        var cadena = $scope.frmExpresionesRegulares.texto;
        var expresion = $scope.frmExpresionesRegulares.expresion;
        try{
            var expReg = new RegExp(expresion);
            $scope.frmExpresionesRegulares.expresionValida = true;
            $scope.frmExpresionesRegulares.textoMatchs = ( expReg.test(cadena) ) ;
        }catch(ex){
            $scope.frmExpresionesRegulares.expresionValida = false;
            $scope.frmExpresionesRegulares.textoMatchs = false;
        }
    };
    
    //seleccion de referencia
    $scope.frmSeleccionarReferencia = {
        idTipoMetamodelo : "",
        objetos : [],
        indiceAtributo:-1
    };
    $scope.mostrarSeleccionarReferencia = function(indice){
        $scope.frmSeleccionarReferencia.indiceAtributo = indice
        $scope.frmSeleccionarReferencia.idTipoMetamodelo = $scope.atributos[ indice ].idTipoMetamodeloRef;
        
        var parametros = "idModelo=" + $scope.objetoModelo.idModelo + "&idTipoMetamodelo=" + encodeURI( $scope.frmSeleccionarReferencia.idTipoMetamodelo );
        $http.post( $scope.PREFIJO + '/getObjetosByModeloTipo' + $scope.SUBFIJO , parametros).then( 
            (response) => {
                $scope.frmSeleccionarReferencia.objetos = response.data.lista;
                $scope.currentScreen = "#frmSeleccionarReferencia";
            }, 
            ( response ) => {
                alert(response.status);
            });
    }
    $scope.irAObjetoModelo = function(){
        $scope.currentScreen = "#divModelView";
    };
    $scope.seleccionarReferencia = function(indice){
                    
        try{
            var objetoSeleccionado = $scope.frmSeleccionarReferencia.objetos[indice];
            var atributo = $scope.atributos[ $scope.frmSeleccionarReferencia.indiceAtributo ];
            //alert(JSON.stringify(objetoSeleccionado));
            atributo.valor = objetoSeleccionado.idObjeto;
            atributo.nombreRef = objetoSeleccionado.nombre;
            $scope.onCambiarCampo();
            //alert(JSON.stringify(atributo))
        }catch(ex){
            alert(ex);
        }finally{
            $scope.irAObjetoModelo();
        }
        
    };
    
    //importar Modelo
    
    $scope.mostrarImportarModelo = function(){
        $scope.currentScreen ="#frmImportarModelo";
    }
    
    //alert("inicializado");
});


    

