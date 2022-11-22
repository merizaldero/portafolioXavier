var enterpriseApp = angular.module('enterpriseApp', []);

enterpriseApp.controller('enterpriseController', function($scope, $http) {
  $scope.currentUser = getCookie("username");
  //alert(document.cookie);
  $scope.currentItem = null;
  $scope.list = [];
  $scope.consultar = ()=>{
    $http.get("/api/enterprise")
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
    $scope.currentItem = { 'id':null, 'createdBy': null, 'createdDate': null, 'modifiedBy': null, 'modifiedDate': null, 'status': true, 'address': '', 'name':'', 'phone':'' };
  };

  $scope.editar = ( item )=>{
    $scope.currentItem = item ;
    $scope.currentItem.modifiedBy = $scope.currentUser;
  };

  $scope.guardar = ()=>{
    $scope.currentItem.modifiedDate = (new Date()).toISOString();
    $scope.currentItem.modifiedBy = $scope.currentUser;
    if($scope.currentItem.id == null){
      $scope.currentItem.createdDate = $scope.currentItem.modifiedDate;
      $scope.currentItem.createdBy = $scope.currentUser;
    }

    var url = ($scope.currentItem.id == null)?'/api/enterprise':'/api/enterprise/' + $scope.currentItem.id
    $http.post(url, $scope.currentItem )
      .then( (response)=>{
        $scope.currentItem = response.data;
      })
      .catch( (err_ )=>{
        alert( "Error al guardar: " + err_ );
      });
  };

  $scope.esInvalido = ()=>{
    if( $scope.currentItem.name == null || $scope.currentItem.name == ""){
      return true;
    }
    if( $scope.currentItem.address == null || $scope.currentItem.address == ""){
      return true;
    }
    if( $scope.currentItem.phone == null || $scope.currentItem.phone == ""){
      return true;
    }
    return false;
  };

  $scope.verDepartamentos = (item)=>{
    document.location.href = "departments.html?idEnterprise=" + item.id;
  };

  $scope.cancelar = ()=>{
    $scope.consultar();
  };

  $scope.consultar();
});



