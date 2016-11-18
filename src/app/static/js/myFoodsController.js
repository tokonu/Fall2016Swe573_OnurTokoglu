'use strict';

app.controller('MyFoodsCntr',function ($scope, MealBoxService, $http) {

    $scope.foodList = {};
    $scope.filteredList = {};


    $scope.foodClicked = function (food) {
        if (food.nutrientsVisible){
            food.nutrientsVisible = false;
            return;
        }
        if (food.nutrients){
            food.nutrientsVisible = true;
        }else{
            getNutrients(food, function (done) {
                if (done){
                    food.nutrientsVisible = true;
                }
            });
        }
    };

    var getNutrients = function(food, callback) {
        $http.post('/userarea/getNutrientsFromLocal/'+food.ndbno)
            .success(function (data) {
                if (data.nutrients){
                    food.nutrients = data.nutrients;
                    food.selectedMeasure = food.measures[0];
                    callback(true);
                }
            })
            .error(function (err) {
                alert(err);
            })
    };

    $scope.getMultiplier = function(food){
        var selected = food.selectedMeasure;
        return selected.qty * selected.eqv/100;
    };

    $scope.addToMealbox = function(food){
        MealBoxService.addFood(food);
    };

    var getMyFoods = function() {
        $http.post('/userarea/getMyFoods')
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.foods){
                    $scope.foodList = data.foods;
                    $scope.filteredList = $scope.foodList;
                }
            })
            .error(function (err) {
                alert(err);
            });
    };

    $scope.searchChanged = function (text) {
        if (!text || text == ''){
            $scope.filteredList = $scope.foodList;
        }
        $scope.filteredList = {};
        for (var ndbno in $scope.foodList){
            var food = $scope.foodList[ndbno];
            if (food.name.toLowerCase().indexOf(text.toLowerCase()) != -1){
                $scope.filteredList[ndbno] = food;
            }
        }
    };


    getMyFoods();


});