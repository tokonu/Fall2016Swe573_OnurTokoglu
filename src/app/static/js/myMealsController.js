'use strict';

app.controller('MyMealsCntr',function ($scope, MealBoxService, $http) {
    $scope.recipeList = {};
    $scope.filteredList = {};


    $scope.addToMealbox = function(recipe){
        for (var ndbno in recipe.foods){
            MealBoxService.addFood(recipe.foods[ndbno]);
        }
    };

    $scope.recipeClicked = function (recipe) {
        if (recipe.foodsVisible){
            recipe.foodsVisible = false;
            return;
        }
        if (recipe.foods){
            recipe.foodsVisible = true;
        }else{
            getFoods(recipe, function (done) {
                if (done){
                    recipe.foodsVisible = true;
                }
            });
        }
    };
    
    var getFoods = function (recipe, callback) {
        $http.post('/userarea/getFoodsInRecipe/'+recipe.id.toString())
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.foods){
                    recipe.foods = data.foods;
                    callback(true);
                }
            })
            .error(function (err) {
                alert(err);
            });
    };

    var getMyRecipes = function() {
        $http.post('/userarea/getMyRecipes')
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.recipes){
                    $scope.recipeList = data.recipes;
                    $scope.filteredList = $scope.recipeList;
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
        for (var id in $scope.recipeList){
            var recipe = $scope.recipeList[id];
            if (recipe.name.toLowerCase().indexOf(text.toLowerCase()) != -1){
                $scope.filteredList[id] = recipe;
            }
        }
    }


    getMyRecipes();
});