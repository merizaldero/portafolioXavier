//alert('compila');

var visorApp = angular.module('visorApp', []);
visorApp.controller('visorController', function($scope, $http) {
    $scope.actividad={
        idObjeto:0,
        nombre:'dummy',
        __listas:{Entradas:[],Salidas:[]}
        };
    $scope.actividades = [];
    $scope.idActividad = 0;
    
    $scope.cargarActividad = function( idA ){
        
        $scope.idActividad = idA;
        $scope.actividad = $scope.actividades.filter( item => { return idA == item.idObjeto })[0];
        
    };
    
    $scope.cargarActividades = function(){
        
        $http.get('assets/CadenaValorServicios.json').then(
            (result) => {
                $scope.procesarData(result.data)
            },
            (result) => {
                 alert("se fue a la porra \n"+JSON.stringify(result));
            }
        );
        
    };
    
    $scope.procesarData = function(data){
        //alert(JSON.stringify(data));
        var actividades = data.__objetoRaiz.__listas.Procesos;        
        //alert(JSON.stringify(actividades));
        for( indiceActividad in actividades ) {
            var actividad = actividades[indiceActividad];
            var salidas = actividad.__listas.Salidas;
            for(var indiceSalida in salidas){
                salidas[indiceSalida].destinos = [];
            }
            for( indiceActividad1 in actividades ) {
                if( indiceActividad == indiceActividad1 ){
                    continue;
                }
                var actividad1 = actividades[indiceActividad1];
                var entradas = actividad1.__listas.Entradas;
                for(var indiceEntrada in entradas){
                    var entrada = entradas[indiceEntrada]
                    for(var indiceSalida in salidas){
                        var salida = salidas[indiceSalida];
                        if(entrada.__atributos.referencia == salida.idObjeto.toString()){
                            // match
                            salida.destinos.push(actividad1);
                            entrada.origen = actividad;
                        }
                    }
                }
            }
        }
        $scope.actividades = actividades;
        
        $scope.cargarActividad( $scope.actividades[0].idObjeto );
        //alert("cargado");
    };
    
    $scope.cargarActividades();
});



