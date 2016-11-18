'use strict';

app.controller('TopbarCtrl',function ($scope, UserInfoService, $http) {
    $scope.user = UserInfoService.getUser();
    $scope.user.bmi = function () {
        return ($scope.user.weight / Math.pow($scope.user.height/100,2)).toFixed(1);
    };

    //Form Functions

    $scope.formError = "";
    $scope.updatedUser = {};
    $scope.resetForm = function (form) {
        $scope.updatedUser = {};
        $scope.updatedUser = angular.copy($scope.user);
        $scope.formError = "";
    };

    $scope.sendForm = function () {
        setLoading();
        $http.post('/userarea/edituser',$scope.updatedUser)
            .success(function (data) {
                alert(data);
                stopLoading()
                if (data != "ok"){
                    $scope.formError = data;
                }else{
                    $scope.formError = "";
                    $scope.user = $scope.updatedUser;
                    hideModal();
                }
            })
            .error(function (err) {
                alert(err);
                stopLoading()
                $scope.formError = "Error. Try again later";
            });
    };

    var setLoading = function () {
        $(function () {
            var $btn = $('#profileSubmitButton').button('loading');
        });
    };

    var stopLoading = function () {
        $(function () {
            var $btn = $('#profileSubmitButton').button('reset');
        });
    };

    var hideModal = function () {
        $(function () {
            $('#editModal').modal('hide')
        });
    };

});
