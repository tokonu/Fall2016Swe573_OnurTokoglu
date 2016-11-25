
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

    var clearFoods = function(){
        foods = {};
    }

    return {
        addFood: addFood,
        getFoods: getFoods,
        deleteFood: deleteFood,
        clearFoods: clearFoods
    };
});


app.service('ReportsDateService',function () {

    var fromDate = "01-01-2016";
    var toDate = "12-12-2016";
    var callback;

    var setFromDate = function(date){
        fromDate = date;
    };

    var getFromDate = function () {
        return fromDate;
    };

    var setToDate = function (date) {
        toDate = date;
    };

    var getToDate = function () {
        return toDate;
    };

    var registerCallback = function (c) {
        callback = c;
    };

    var triggerCallback = function () {
        callback();
    }

    return {
        setFromDate: setFromDate,
        getFromDate: getFromDate,
        setToDate: setToDate,
        getToDate: getToDate,
        registerCallback: registerCallback,
        triggerCallback: triggerCallback
    }

});








