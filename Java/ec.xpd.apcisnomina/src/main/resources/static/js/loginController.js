var loginApp = angular.module('loginApp', []);

loginApp.controller('loginController', function($scope, $http) {
    $scope.currentUser = getCookie("username");
    $scope.currentItem = null;
    $scope.doEnterprise = ()=>{
        document.location.href="enterprises.html";
    };
    $scope.doEmployee = ()=>{
        document.location.href="employees.html";
    };
});

