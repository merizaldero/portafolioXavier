var monitorApp = angular.module('monitorApp', []);
monitorApp.controller('monitorController', function($scope, $http) {
    $scope.horas = [
    	{
    		"codigoHora": 8,
    		"horaInicio": "00:00",
    		"horaFin": "08:00"
    	},
    	{
    		"codigoHora": 10,
    		"horaInicio": "08:00",
    		"horaFin": "10:00"
    	},
    	{
    		"codigoHora": 12,
    		"horaInicio": "10:00",
    		"horaFin": "12:00"
    	},
    	{
    		"codigoHora": 14,
    		"horaInicio": "12:00",
    		"horaFin": "14:00"
    	},
    	{
    		"codigoHora": 16,
    		"horaInicio": "14:00",
    		"horaFin": "16:00"
    	},
    	{
    		"codigoHora": 18,
    		"horaInicio": "16:00",
    		"horaFin": "18:00"
    	}
    ];
    
	$scope.aplicaciones = [
    	{
    		"nombre": "Aplicacion 1",
    		"color": "#ffffcc",
    		"items": [
    			{
    				"nombre": "Item Monitoreo 1",
    				"totalTrx" : 0,
    				"conteoExitosos": 0,
    				"porcentajeExitosos": 0.0,
    				"conteoFallidos": 0,
    				"porcentajeFallidos": 0.0,
    				"calculaAcumulado": false
    			},
    			{
    				"nombre": "Item Monitoreo 2",
    				"totalTrx" : 0,
    				"conteoExitosos": 0,
    				"porcentajeExitosos": 0.0,
    				"conteoFallidos": 0,
    				"porcentajeFallidos": 0.0,
    				"calculaAcumulado": true
    			},
    			{
    				"nombre": "Item Monitoreo 3",
    				"totalTrx" : 0,
    				"conteoExitosos": 0,
    				"porcentajeExitosos": 0.0,
    				"conteoFallidos": 0,
    				"porcentajeFallidos": 0.0,
    				"calculaAcumulado": false
    			},
    		]
    	},
    	
    	{
    		"nombre": "Aplicacion 2",
    		"color": "#ffccff",
    		"items": [
    			{
    				"nombre": "Item Monitoreo 1",
    				"totalTrx" : 0,
    				"conteoExitosos": 0,
    				"porcentajeExitosos": 0.0,
    				"conteoFallidos": 0,
    				"porcentajeFallidos": 0.0,
    				"calculaAcumulado": false
    			},
    			{
    				"nombre": "Item Monitoreo 2",
    				"totalTrx" : 0,
    				"conteoExitosos": 0,
    				"porcentajeExitosos": 0.0,
    				"conteoFallidos": 0,
    				"porcentajeFallidos": 0.0,
    				"calculaAcumulado": false
    			},
    			{
    				"nombre": "Item Monitoreo 3",
    				"totalTrx" : 0,
    				"conteoExitosos": 0,
    				"porcentajeExitosos": 0.0,
    				"conteoFallidos": 0,
    				"porcentajeFallidos": 0.0,
    				"calculaAcumulado": false
    			},
    		]
    	},
    	
    ];
	var fechaActual = new Date();
	$scope.fecha = new Date( fechaActual.getFullYear(), fechaActual.getMonth() , fechaActual.getDate() );
    
	$scope.hora = -1;
	var hora = fechaActual.getHours();
	var indiceHora;
	for (indiceHora in $scope.horas){
		$scope.hora = $scope.horas[indiceHora]["codigoHora"].toString();
		if( $scope.horas[indiceHora]["codigoHora"] >= hora ){
			break;
		}
	};
	
	$scope.getFechaIso = function(){
		var anio = $scope.fecha.getFullYear().toString();
		var mes = ($scope.fecha.getMonth() + 1).toString() ;
		var dia = $scope.fecha.getDate().toString() ;
		if(mes.length == 1){
			mes = "0" + mes;
		}
		if(dia.length == 1){
			dia = "0" + dia;
		}
		return anio + "-" + mes + "-" + dia;
	};
	
	$scope.cargaIniciada = false;
	
	$scope.terminarCarga = function(){
		$scope.horaActual = $scope.horaAnterior = null;
		$scope.dataActual = $scope.dataAnterior = null;
		$scope.cargaIniciada = false;
	};
	
	$scope.iniciarCargaData = function(){
		
		if( $scope.cargaIniciada ){
			return;
		}
		
		$scope.cargaIniciada = true;
		
		// Identifica instancia de hora, y si se encuentra disponible instancia anterior
		$scope.horaActual = $scope.horaAnterior = null;
		var indiceHora;
		for(indiceHora in $scope.horas){
			if($scope.horas[indiceHora]["codigoHora"].toString() == $scope.hora){
				$scope.horaActual = $scope.horas[indiceHora];
				break;
			} else {
				$scope.horaAnterior = $scope.horas[indiceHora];
			}
		}
		
		var fechaIso = $scope.getFechaIso();
		
		//Realizar llamado 
		var ruta = "data/"+ $scope.getFechaIso() + "/" + $scope.horaActual["codigoHora"] + ".json";
		
		$http.get(ruta, { responseType : "json" }).then(
				function exitoRuta(response){
					if($scope.horaAnterior == null){
						$scope.procesarInformacion(response.data , null);
					} else {
						$scope.dataActual = response.data;
						var rutaAnterior = "data/"+ $scope.getFechaIso() + "/" + $scope.horaAnterior["codigoHora"] + ".json";
						$http.get(rutaAnterior, { responseType : "json" }).then(
								function exitoRutaAnterior(response){
									$scope.dataAnterior = response.data;
									$scope.procesarInformacion( $scope.dataActual , response.data );
								},
								function errorRutaAnterior(response){
									alert("No se pudo obtener data anterior");
									$scope.procesarInformacion( $scope.dataActual , null );
								}
							);
					}
				},
				function errorRuta(response){
					alert("no se ha podido obtener Datos");
					$scope.terminarCarga();
				}
			);
	};
	
	$scope.procesarInformacion = function(dataActual, dataAnterior){
		var aplicacion;
		var item;
		var dataItem;
		var dataItemAnterior;
		for( claveAplicacion in $scope.aplicaciones){
			aplicacion = $scope.aplicaciones[claveAplicacion];
			for( claveItem in aplicacion["items"] ){
				item = aplicacion["items"][claveItem];
				dataItem = dataActual[ aplicacion["nombre"] ][ item["nombre"] ];
				item["totalTrx"] = item["conteoExitosos"] = item["conteoFallidos"] = 0;
				item["porcentajeExitosos"] = item["porcentajeFallidos"] = 0.0;
				try{
					if( !item["calculaAcumulado"] || dataAnterior == null ){
						item["conteoFallidos"] = dataItem["conteoFallidos"];
						if("conteoExitosos" in dataItem){
							item["conteoExitosos"] = dataItem["conteoExitosos"];
							item["totalTrx"] = dataItem["conteoExitosos"] + dataItem["conteoFallidos"];
						} else if("totalTrx" in dataItem){
							item["totalTrx"] = dataItem["totalTrx"];
							item["conteoExitosos"] = dataItem["totalTrx"] - dataItem["conteoFallidos"];
						} else {
							item["totalTrx"] = dataItem["conteoFallidos"];
							item["conteoExitosos"] = 0 ;
						}
					} else {
						dataItemAnterior = dataAnterior[ aplicacion["nombre"] ][ item["nombre"] ];
						item["conteoFallidos"] = dataItem["conteoFallidos"] - dataItemAnterior["conteoFallidos"];
						if("conteoExitosos" in dataItem){
							item["conteoExitosos"] = dataItem["conteoExitosos"] - dataItemAnterior["conteoExitosos"];
							item["totalTrx"] = dataItem["conteoExitosos"] + dataItem["conteoFallidos"];
						} else if("totalTrx" in dataItem){
							item["totalTrx"] = dataItem["totalTrx"] - dataItemAnterior["totalTrx"];
							item["conteoExitosos"] = dataItem["totalTrx"] - dataItem["conteoFallidos"];
						} else {
							item["totalTrx"] = dataItem["conteoFallidos"];
							item["conteoExitosos"] = 0 ;
						}
					}
					item["porcentajeExitosos"] = ((dataItem["totalTrx"] == 0)? 0.00 : (0.0 + item["conteoExitosos"] ) / item["totalTrx"] * 100.00).toFixed(2);
					item["porcentajeFallidos"] = ((dataItem["totalTrx"] == 0)? 0.00 : (0.0 + item["conteoFallidos"] ) / item["totalTrx"] * 100.00).toFixed(2);
				}catch(ex){
					item["totalTrx"] = item["conteoExitosos"] = item["conteoFallidos"] = "Error";
					item["porcentajeExitosos"] = item["porcentajeFallidos"] = "Error";
				}
				
			}			
		}
		
		$scope.terminarCarga();
	};
	
	$scope.iniciarCargaData();
	
});