var departmentApp = angular.module('departmentApp', []);

departmentApp.controller('departmentController', function($scope, $http) {
  $scope.currentUser = getCookie("username");
  let params = (new URL(document.location)).searchParams;
  $scope.idEnterprise = params.get("idEnterprise");
  // alert("enterprise " +$scope.idEnterprise)
  $scope.currentItem = null;
  $scope.list = [];
  $scope.consultar = ()=>{
    $http.get("/api/enterprise/" + $scope.idEnterprise + "/department")
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
    $scope.currentItem = { 'id':null, 'createdBy': null, 'createdDate': null, 'modifiedBy': null, 'modifiedDate': null, 'status': true, 'description': '', 'name':'', 'phone':'' };
  };

  $scope.editar = ( item )=>{
    $scope.currentItem = item ;
    // $scope.currentItem.modifiedBy = $scope.currentUser;
  };
  
  $scope.doEmployees = ( item )=>{
    document.location.href = "department_employees.html?idDepartment="+item.id;
  };

  $scope.guardar = ()=>{
    $scope.currentItem.idEnterprise = $scope.idEnterprise;
    $scope.currentItem.modifiedDate = (new Date()).toISOString();
    $scope.currentItem.modifiedBy = $scope.currentUser;
    if($scope.currentItem.id == null){
      $scope.currentItem.createdDate = $scope.currentItem.modifiedDate;
      $scope.currentItem.createdBy = $scope.currentUser;
    }

    var url = ($scope.currentItem.id == null)?'/api/enterprise/' + $scope.idEnterprise + '/department':'/api/department/' + $scope.currentItem.id
    $http.post(url, $scope.currentItem )
      .then( (response)=>{
        $scope.currentItem = response.data;
      })
      .catch( (err_ )=>{
        alert( "Error al guardar: " + err_ );
      });
  };

  $scope.esInvalido = ()=>{
    if( $scope.currentItem.description == null || $scope.currentItem.description == ""){
      return true;
    }
    if( $scope.currentItem.name == null || $scope.currentItem.name == ""){
      return true;
    }
    if( $scope.currentItem.phone == null || $scope.currentItem.phone == ""){
      return true;
    }
    return false;
  };

  $scope.cancelar = ()=>{
    $scope.consultar();
  };

  $scope.consultar();
});



