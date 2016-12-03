
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
    };

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
    };

    return {
        setFromDate: setFromDate,
        getFromDate: getFromDate,
        setToDate: setToDate,
        getToDate: getToDate,
        registerCallback: registerCallback,
        triggerCallback: triggerCallback
    }

});



app.service('RecommendedValueService',function (UserInfoService) {
    var recommendedMultiplier = UserInfoService.getUser().recommendedIntake / 2000;
    var recommendedValues = {
        "203": 50, //Protein
        "204": 65, //Total fat
        "205": 300, //Total Carbohydrate
        "208": 2000, //Energy kcal
        "291": 25, //Fiber
        "301": 1000, //Calcium
        "303": 18, //Iron
        "304": 400, //Magnesium
        "305": 1000, //Phosphorus
        "306": 3500, //Potassium
        "307": 2400, //Sodium
        "309": 15, //Zinc
        "312": 2, //Copper
        "315": 2, //Manganese
        "317": 70, //Selenium
        "318": 5000, //Vitamin A
        "324": 400, //Vitamin D
        "401": 60, //Vitamin C
        "404": 1.5, //Thiamin
        "405": 1.7, //Riboflavin
        "406": 20, //Niacin
        "410": 10, //Pantothenic acid
        "415": 2, //Vitamin B6
        "417": 400, //Folate
        "418": 6, //Vitamin B12
        "430": 80, //Vitamin K
        "601": 300, //Cholesterol
        "606": 20 //Saturated fat
    };

    for (var id in recommendedValues){
        recommendedValues[id] = Math.floor(recommendedValues[id]*100*recommendedMultiplier)/100;
    }

    return {
        recommendedValues: recommendedValues
    }
});




