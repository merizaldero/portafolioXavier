const app = angular.module("keyhunter_app", []);
app.controller("keyhunter_controller", function($scope) {
    $scope.personajes = [
        {
          id: 1,
          nombre: "Cabris",
          img_personaje: 'img/personaje_1.png',
          img_caja: 'img/caja_sorpresa_1.png',
          img_llave: 'img/llave_1.png',
          vendido: false,
          llave: 1,
        },
        {
          id: 2,
          nombre: "Gatis",
          img_personaje: 'img/personaje_2.png',
          img_caja: 'img/caja_sorpresa_2.png',
          img_llave: 'img/llave_2.png',
          vendido: false,
          llave: 2,
        },
        {
          id: 3,
          nombre: "Zombi",
          img_personaje: 'img/personaje_3.png',
          img_caja: 'img/caja_sorpresa_3.png',
          img_llave: 'img/llave_3.png',
          vendido: false,
          llave: 3,
        },
        {
          id: 4,
          nombre: "Michi",
          img_personaje: 'img/personaje_4.png',
          img_caja: 'img/caja_sorpresa_4.png',
          img_llave: 'img/llave_4.png',
          vendido: false,
          llave: 4,
        },
        {
          id: 5,
          nombre: "Kachis",
          img_personaje: 'img/personaje_5.png',
          img_caja: 'img/caja_sorpresa_5.png',
          img_llave: 'img/llave_5.png',
          vendido: false,
          llave: 5,
        },
        {
          id: 6,
          nombre: "Vampis",
          img_personaje: 'img/personaje_6.png',
          img_caja: 'img/caja_sorpresa_6.png',
          img_llave: 'img/llave_6.png',
          vendido: false,
          llave: 6,
        },
      ];
    $scope.getPersonajes = function (){
        return $scope.personajes;
    };

    $scope.defaultItemClass = function(index){
        return (index == 0) ? "active" : "" ;
    };

    $scope.encabezado_modal = "";
    $scope.mensaje_modal = "";

    $scope.mostrar_modal = function(encabezado, mensaje){
        $scope.encabezado_modal = encabezado;
        $scope.mensaje_modal = mensaje;
        const modal_final = new bootstrap.Modal(document.getElementById('modal_final'), {});
        try{
            modal_final.show();
        }catch(ex){
            alert(ex);
        }

    };

    $scope.agregar_seleccionado = function(indice){
        if( $scope.personajes_seleccionados.indexOf( $scope.personajes[indice] ) < 0){
            $scope.personajes_seleccionados.push( $scope.personajes[indice] );
            $scope.personajes[indice].vendido = true;
            if( $scope.personajes_seleccionados.length >= 6 ){
                $scope.mostrar_modal("Partida Perdida", "Tuviste que elegir todas las Muñecas para poder tener todas las llaves");
            }
            else if($scope.es_ganador() ){
                let numero_logrado = $scope.personajes_seleccionados.length;
                $scope.mostrar_modal("Has Ganado", `Lograste reunir todas las llaves seleccionando ${numero_logrado} de Muñecas`);
            }
        }
    };

    $scope.seleccionado_con_llave = function(indice){
        const seleccion = $scope.personajes_seleccionados.filter(item =>{ return item.llave == indice; });
        if(seleccion.length == 0){
            return null;
        }
        return seleccion[0].nombre;
    };

    $scope.personajes_seleccionados = [];

    $scope.repartirLlaves = function () {
        const llaves = [1, 2, 3, 4, 5, 6];
        let indice = 0;
        $scope.personajes.forEach(personaje => {
            indice = Math.floor(Math.random() * llaves.length);
            personaje.llave = llaves[indice];
            llaves.splice(indice, 1);  
        });
    };

    $scope.es_ganador = function () {
        if($scope.personajes_seleccionados.length == $scope.personajes.length ){
            return false;
        }
        let ids = $scope.personajes_seleccionados.map( (item) => { return item.id; } );
        ids.sort();
        let llaves = $scope.personajes_seleccionados.map( (item) => { return item.llave; } );
        llaves.sort();
        console.log(ids);
        console.log(llaves);
        let igual = true;
        for (let indice = 0; igual && indice<ids.length; indice ++){
            igual = ids[indice] == llaves[indice];
        }
        return igual;
    };

    $scope.repartirLlaves();

  });
