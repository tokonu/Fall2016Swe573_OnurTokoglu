

app.controller('MealboxCntr',function ($scope, MealBoxService, $http) {

    $scope.foods = MealBoxService.getFoods();
    $scope.mealbox  = {};

    $scope.hasFood = function () {
        if (Object.keys($scope.foods).length > 0){
            return true;
        }
        return false;
    }

    $scope.deleteFood = function(food){
        MealBoxService.deleteFood(food);
    }
    
    $scope.saveAndAdd = function () {
        
    }

    $scope.save = function(){

    }


});