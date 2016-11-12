
app.service('MealBoxService',function () {

    var foods = {};

    var addFood = function (food) {
        foods[food.ndbno] = food;
    };

    var getFoods = function () {
        return foods;
    };

    var deleteFood = function (food) {
        delete foods[food.ndbno];
    };

    return {
        addFood: addFood,
        getFoods: getFoods,
        deleteFood: deleteFood
    };
});