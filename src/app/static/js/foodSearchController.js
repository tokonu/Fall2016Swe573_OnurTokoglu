'use strict';

app.controller('FoodSearchCtrl',function ($scope, UserInfoService, $http) {
    $scope.searchQuery = "";
    $scope.foodList = [{
        name: "FoodName",
        ndbno: "45051439"
    },
    {
        name: "FoodName2",
        ndbno: "ndbno2"
    },
    {
        name: "FoodName3",
        ndbno: "ndbno3"
    },
    {
        name: "FoodName4",
        ndbno: "ndbno4"
    }];

    $scope.nutrientReport = {};
    $scope.nutrientSectionVisible = {};

    $scope.searchFoods = function() {
        var qStr = $scope.searchQuery;
        if (qStr.length < 4){
            alert("Enter a string longer than 3 characters");
            return;
        }
        setLoading();

        $http.post('/userarea/searchFood', {query:qStr})
            .success(function (data) {
                stopLoading();
                if (data.error){
                    alert(data.error);
                }else if (data.list) {
                    $scope.foodList = data.list;
                }
                //alert(JSON.stringify(data, null, 4));
            })
            .error(function (err) {
                alert(err);
                stopLoading();
            });

    };

    $scope.foodClicked = function (ndbno) {
        if ($scope.nutrientSectionVisible[ndbno]){
            $scope.nutrientSectionVisible[ndbno] = false;
            return;
        }
        if ($scope.nutrientReport[ndbno]){
            $scope.nutrientSectionVisible[ndbno] = true;
        }else{
            getNutrients(ndbno, function (done) {
                if (done){
                    $scope.nutrientSectionVisible[ndbno] = true;
                }
            });
        }
    };

    var getNutrients = function(ndbno, callback){
        //setLoading();

        // $http.post('/userarea/getNutrients', {ndbno:ndbno})
        //     .success(function (data) {
        //         stopLoading();
        //         if (data.error){
        //             alert(data.error);
        //         }else if (data) {
        //
        //         }
        //         alert(JSON.stringify(data, null, 4));
        //     })
        //     .error(function (err) {
        //         alert(err);
        //         stopLoading();
        //     });

        $scope.nutrientReport[ndbno] = dummydata;
        callback(true);
    };


    var setLoading = function () {
        $(function () {
            var $btn = $('#foodSearchButton').button('loading');
        });
    };

    var stopLoading = function () {
        $(function () {
            var $btn = $('#foodSearchButton').button('reset');
        });
    };


    var dummydata = {
    "measures": [
        {
            "eqv": 114,
            "label": "g",
            "qty": 114,
            "value": "170"
        }
    ],
    "ndbno": "45051439",
    "nutrients": [
        {
            "group": "Proximates",
            "name": "Energy",
            "nutrient_id": "208",
            "unit": "kcal",
            "value": "149"
        },
        {
            "group": "Proximates",
            "name": "Protein",
            "nutrient_id": "203",
            "unit": "g",
            "value": "4.39"
        },
        {
            "group": "Proximates",
            "name": "Total lipid (fat)",
            "nutrient_id": "204",
            "unit": "g",
            "value": "1.75"
        },
        {
            "group": "Proximates",
            "name": "Carbohydrate, by difference",
            "nutrient_id": "205",
            "unit": "g",
            "value": "28.07"
        },
        {
            "group": "Proximates",
            "name": "Fiber, total dietary",
            "nutrient_id": "291",
            "unit": "g",
            "value": "0.9"
        },
        {
            "group": "Proximates",
            "name": "Sugars, total",
            "nutrient_id": "269",
            "unit": "g",
            "value": "0.88"
        },
        {
            "group": "Minerals",
            "name": "Calcium, Ca",
            "nutrient_id": "301",
            "unit": "mg",
            "value": "18"
        },
        {
            "group": "Minerals",
            "name": "Iron, Fe",
            "nutrient_id": "303",
            "unit": "mg",
            "value": "1.26"
        },
        {
            "group": "Minerals",
            "name": "Sodium, Na",
            "nutrient_id": "307",
            "unit": "mg",
            "value": "430"
        },
        {
            "group": "Vitamins",
            "name": "Vitamin C, total ascorbic acid",
            "nutrient_id": "401",
            "unit": "mg",
            "value": "5.3"
        },
        {
            "group": "Vitamins",
            "name": "Vitamin A, IU",
            "nutrient_id": "318",
            "unit": "IU",
            "value": "0"
        },
        {
            "group": "Lipids",
            "name": "Fatty acids, total saturated",
            "nutrient_id": "606",
            "unit": "g",
            "value": "0.44"
        },
        {
            "group": "Lipids",
            "name": "Fatty acids, total trans",
            "nutrient_id": "605",
            "unit": "g",
            "value": "0.00"
        },
        {
            "group": "Lipids",
            "name": "Cholesterol",
            "nutrient_id": "601",
            "unit": "mg",
            "value": "4"
        }
    ]
};

});
