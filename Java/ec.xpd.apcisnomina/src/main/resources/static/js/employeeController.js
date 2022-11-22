var employeeApp = angular.module('employeeApp', []);

employeeApp.controller('employeeController', function($scope, $http) {
  $scope.currentUser = getCookie("username");
  //alert(document.cookie);
  $scope.currentItem = null;
  $scope.list = [];
  $scope.consultar = ()=>{
    $http.get("/api/employee")
      .then( (response)=>{
        if(response.status == 200){
          $scope.list = response.data.lista;
          $scope.currentItem = null;
        }else{
          alert("Error al obtener listado");
        }
      })
      .catch( (error_ )=>{
        alert( "error carga" + error_ );
      });
  };

  $scope.nuevo = ()=>{
    $scope.currentItem = { 'id':null, 'createdBy': null, 'createdDate': null, 'modifiedBy': null, 'modifiedDate': null, 'status': true, 'surname': '', 'name':'', 'position':'', 'age':18 };
  };

  $scope.editar = ( item )=>{
    $scope.currentItem = item ;
    // $scope.currentItem.modifiedBy = $scope.currentUser;
  };

  $scope.guardar = ()=>{
    $scope.currentItem.modifiedDate = (new Date()).toISOString();
    $scope.currentItem.modifiedBy = $scope.currentUser;
    if($scope.currentItem.id == null){
      $scope.currentItem.createdDate = $scope.currentItem.modifiedDate;
      $scope.currentItem.createdBy = $scope.currentUser;
    }

    var url = ($scope.currentItem.id == null)?'/api/employee':'/api/employee/' + $scope.currentItem.id
    $http.post(url, $scope.currentItem )
      .then( (response)=>{
        $scope.currentItem = response.data;
      })
      .catch( (err_ )=>{
        alert( "Error al guardar: " + err_ );
      });
  };

  $scope.esInvalido = ()=>{
    if( $scope.currentItem.surname == null || $scope.currentItem.surname == ""){
      return true;
    }
    if( $scope.currentItem.name == null || $scope.currentItem.name == ""){
      return true;
    }
    if( $scope.currentItem.position == null || $scope.currentItem.position == ""){
      return true;
    }
    if( $scope.currentItem.email == null || $scope.currentItem.email == ""){
      return true;
    }
    if( $scope.currentItem.age == null || $scope.currentItem.age == ""){
      return true;
    }
    return false;
  };

  $scope.cancelar = ()=>{
    $scope.consultar();
  };

  $scope.consultar();
});



