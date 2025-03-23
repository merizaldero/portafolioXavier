//alert('compila');

var visorApp = angular.module('visorApp', []);
visorApp.controller('visorController', function($scope, $http) {
    $scope.actividad={
        idObjeto:0,
        nombre:'dummy',
        __listas:{Entradas:[],Salidas:[]}
        };
    $scope.actividades = [];
    $scope.artefactos = [];
    $scope.idActividad = 0;
    
    $scope.cargarActividad = function( idA ){
        
        $scope.idActividad = idA;
        const actividad = $scope.actividades.find( item => idA == item.idObjeto );
        if(actividad){
          $scope.actividad = actividad;
        }else{
          alert("No se ha encontrado Proceso " + idA);
          $scope.actividad = { idObjeto:0, nombre:"No encontrdo", entradas:[], salidas:[]};
        }
        
    };
    
    $scope.cargarActividades = function(){
        
        $http.get('PmBok.json?2').then(
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
        const actividades = data.__objetoRaiz.__listas.Procesos;
        const areas = data.__objetoRaiz.__listas['Areas Conocimiento'];
        areas.forEach(area => {
            area.__listas.Procesos.forEach(proceso =>{
                proceso.nombre = area.nombre + " - " + proceso.nombre;
                actividades.push(proceso);
            });            
        });
        //alert(JSON.stringify(actividades));
        const artefactos = [];
        actividades.forEach(actividad=>{
            let artefacto;
            actividad.entradas = [];
            actividad.__listas.Entradas.forEach( entrada=>{
                artefacto = artefactos.find(item => item.nombre === entrada.nombre);
                if(artefacto){
                    artefacto.destinos.push(actividad);
                }else{
                    artefacto = {nombre:entrada.nombre, origenes:[], destinos:[actividad] };
                    artefactos.push(artefacto);
                }
                actividad.entradas.push(artefacto);
            });
            actividad.salidas = [];
            actividad.__listas.Salidas.forEach( salida=>{
                artefacto = artefactos.find(item => item.nombre === salida.nombre);
                if(artefacto){
                    artefacto.origenes.push(actividad);
                }else{
                    artefacto = {nombre:salida.nombre, origenes:[actividad], destinos:[] };
                    artefactos.push(artefacto);
                }
                actividad.salidas.push(artefacto);
            });
        });
        
        $scope.actividades = actividades;
        artefactos.sort( (a,b) => a.nombre.localeCompare(b.nombre));
        $scope.artefactos = artefactos;
        
        $scope.cargarActividad( $scope.actividades[0].idObjeto );
        //alert("cargado");
    };
    
    $scope.cargarActividades();
});
