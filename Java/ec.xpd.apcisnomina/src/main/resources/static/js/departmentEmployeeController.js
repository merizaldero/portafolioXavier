var departmentEmployeeApp = angular.module('departmentEmployeeApp', []);

departmentEmployeeApp.controller('departmentEmployeeController', function($scope, $http) {
  $scope.currentUser = getCookie("username");
  let params = (new URL(document.location)).searchParams;
  $scope.idDepartment = params.get("idDepartment");
  // alert("enterprise " +$scope.idDepartment)
  $scope.currentItem = null;
  $scope.list = [];
  $scope.listEmployees = [];
  $scope.consultar = ()=>{
    $http.get("/api/department/" + $scope.idDepartment + "/employee")
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
    $http.get("/api/department/" + $scope.idDepartment + "/notemployee")
      .then( (response)=>{
        if(response.status == 200){
          $scope.listEmployees = response.data.lista;
        }else{
          alert("Error al obtener listado");
        }
      })
      .catch( (error_ )=>{
        alert( "error carga" + error_ );
      });
  };

  $scope.nuevo = ()=>{
    $scope.currentItem = { 'id':null, 'createdBy': null, 'createdDate': null, 'modifiedBy': null, 'modifiedDate': null, 'status': true, 'idEmployee':null };
    
  };

  $scope.editar = ( item )=>{
    $scope.currentItem = item ;
    $scope.listEmployees.push(item.employee);
    // $scope.currentItem.modifiedBy = $scope.currentUser;
  };

  $scope.guardar = ()=>{
    $scope.currentItem.idDepartment = $scope.idDepartment;
    $scope.currentItem.modifiedDate = (new Date()).toISOString();
    $scope.currentItem.modifiedBy = $scope.currentUser;
    if($scope.currentItem.id == null){
      $scope.currentItem.createdDate = $scope.currentItem.modifiedDate;
      $scope.currentItem.createdBy = $scope.currentUser;
    }

    var url = ($scope.currentItem.id == null)?'/api/department/' + $scope.idDepartment + '/employee':'/api/departmentemployee/' + $scope.currentItem.id
    $http.post(url, $scope.currentItem )
      .then( (response)=>{
        $scope.currentItem = response.data;
      })
      .catch( (err_ )=>{
        alert( "Error al guardar: " + err_ );
      });
  };

  $scope.esInvalido = ()=>{
    if( $scope.currentItem.idEmployee == null ){
      return true;
    }
    return false;
  };

  $scope.cancelar = ()=>{
    $scope.consultar();
  };

  $scope.consultar();
});



