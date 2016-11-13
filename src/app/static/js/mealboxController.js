

app.controller('MealboxCntr',function ($scope, MealBoxService, $http) {

    $scope.foods = MealBoxService.getFoods();
    $scope.mealbox  = {};

    $scope.hasFood = function () {
        if (Object.keys($scope.foods).length > 0){
            return true;
        }
        return false;
    };

    $scope.deleteFood = function(food){
        MealBoxService.deleteFood(food);
    };
    
    $scope.saveAndAdd = function () {
        
    };

    $scope.addWithoutSaving = function(){
        var meal = {
            date: $scope.mealbox.date,
            foods: $scope.foods
        };
        $http.post('/userarea/saveFoodConsumption', {mealbox:meal})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                MealBoxService.clearFoods();
                $scope.foods = MealBoxService.getFoods(); //weird bug fix
            })
            .error(function(err){
                alert(json.stringify(err));
            });
    }


});