'use strict';

app.controller('ReportsCtrl',function ($scope, ReportsDateService) {

    $scope.fromDateChanged = function () {
        var pattern = /(\d{2})-(\d{2})-(\d{4})/;
        var from = new Date($scope.fromDate.replace(pattern,'$3-$2-$1'));
        var to = new Date($scope.toDate.replace(pattern,'$3-$2-$1'));
        if (from > to){
            $scope.toDate = $scope.fromDate;
        }
        ReportsDateService.setFromDate($scope.fromDate);
    };

    $scope.toDateChanged = function () {
        var pattern = /(\d{2})-(\d{2})-(\d{4})/;
        var from = new Date($scope.fromDate.replace(pattern,'$3-$2-$1'));
        var to = new Date($scope.toDate.replace(pattern,'$3-$2-$1'));
        if (from > to){
            $scope.toDate = $scope.fromDate;
        }
        ReportsDateService.setToDate($scope.toDate);
    };

    $scope.updateDate = function () {
        ReportsDateService.triggerCallback();
    };

    $scope.fromDate = ReportsDateService.getFromDate();
    $scope.toDate = ReportsDateService.getToDate();

});


app.controller('ReportsWeightCtrl',function ($scope, ReportsDateService, $http) {

    $scope.data = [[10,20,30],[25,35,45]];
    $scope.labels = ["a","b","c"];
    $scope.colors = ['#44ee66','#323232'];
    $scope.series = ['Weight', 'BMI'];
    $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
    $scope.options = {
        scales: {
            yAxes: [
                {
                    id: 'y-axis-1',
                    type: 'linear',
                    display: true,
                    position: 'left',
                    scaleLabel: {
                        display: true,
                        labelString: "Weight (kg)"
                    },
                    ticks: {
                        min:50,
                        max:150
                    }
                },
                {
                    id: 'y-axis-2',
                    type: 'linear',
                    display: true,
                    position: 'right',
                    scaleLabel: {
                        display: true,
                        labelString: "BMI (kg/m^2)"
                    },
                    ticks: {
                        min:10,
                        max:50
                    }
                }
            ]
        },
        legend: {
            display: true
        }
    };

    var getWeightHist = function() {
        var fromDate = ReportsDateService.getFromDate();
        var toDate = ReportsDateService.getToDate();

        $http.post('/userarea/getWeightHistory', {from:fromDate, to:toDate})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.history){
                    //alert(JSON.stringify(data.history));
                    processData(data.history);
                }
            })
            .error(function (err) {
                alert(err);
            });
    };

    ReportsDateService.registerCallback(function () {
        getWeightHist()
    });

    getWeightHist();

    var processData = function(histList){
        $scope.data = [[],[]];
        $scope.labels = [];
        for (var i = 0; i < histList.length; i++) {
            var hist = histList[i];
            $scope.data[0].push(hist.weight);
            $scope.data[1].push((hist.weight / Math.pow(hist.height/100,2)).toFixed(1));
            $scope.labels.push(hist.date);
        }
    };

});


app.controller('ReportsMyFoodsCtrl',function ($scope, ReportsDateService, $http) {

    $scope.foodHist = [];

    var getFoodHist = function() {
        var fromDate = ReportsDateService.getFromDate();
        var toDate = ReportsDateService.getToDate();

        $http.post('/userarea/getMyFoodsForDates', {from:fromDate, to:toDate})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.foodHist){
                    //alert(JSON.stringify(data.foodHist, null, 2));
                    $scope.foodHist = data.foodHist;
                }
            })
            .error(function (err) {
                alert(err);
            });
    };

    ReportsDateService.registerCallback(function () {
        getFoodHist()
    });

    getFoodHist();

    $scope.deleteClicked = function (food) {
        $http.post('/userarea/deleteFoodEntry', {entryId:food.entryId})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }else{
                    getFoodHist();
                }
            })
            .error(function (err) {
                alert(err);
            });
    }

});


app.controller('ReportsBalanceCtrl',function ($scope, ReportsDateService, $http) {

    $scope.colors = ['#45b7cd', '#ff6384', '#ff8e72'];

    $scope.labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    $scope.data = [
      [65, -59, 80, 81, -56, 55, -40],
      [28, 48, -40, 19, 86, 27, 90],
        [28, 48, -40, 19, 86, 27, 90]
    ];
    $scope.datasetOverride = [
      {
          label: "Expended*",
          borderWidth: 1,
          type: 'bar'
      }, {
            label: "Consumed",
            borderWidth: 1,
            type: 'bar'
      }, {
            label: "Balance",
            borderWidth: 3,
            hoverBackgroundColor: "rgba(255,99,132,0.4)",
            hoverBorderColor: "rgba(255,99,132,1)",
            type: 'line'
      }
    ];

    $scope.options = {
        legend: {
            display: true
        }
    };



    var getBalanceHist = function() {
        var fromDate = ReportsDateService.getFromDate();
        var toDate = ReportsDateService.getToDate();

        $http.post('/userarea/getBalance', {from:fromDate, to:toDate})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.balanceHist){
                    //alert(JSON.stringify(data.balanceHist, null, 2));
                    processData(data.balanceHist);
                }
            })
            .error(function (err) {
                alert(err);
            });
    };

    ReportsDateService.registerCallback(function () {
        getBalanceHist();
    });

    getBalanceHist();

    var processData = function (balanceHist) {
        $scope.data = [[],[],[]];
        $scope.labels = [];
        for (var i = 0; i < balanceHist.length ; i++){
            var hist = balanceHist[i];
            var expended = -(hist.expended + hist.recommended);
            var consumed = hist.consumed;
            var balance = consumed + expended;
            $scope.data[0].push(Math.floor(expended));
            $scope.data[1].push(Math.floor(consumed));
            $scope.data[2].push(Math.floor(balance));
            $scope.labels.push(hist.date);
        }
    }


});




app.controller('ReportsNutrientCtrl',function ($scope, ReportsDateService, RecommendedValueService, $http) {

    $scope.colors = ['#45b7cd', '#ff6384', '#ff8e72'];
    $scope.labels = [];
    $scope.data = [[],[]];
    $scope.datasetOverride = [
      {
        label: "Daily Intake",
        borderWidth: 1,
        type: 'bar'
      },
      {
        label: "Daily Recommended Intake",
        borderWidth: 3,
        hoverBackgroundColor: "rgba(255,99,132,0.4)",
        hoverBorderColor: "rgba(255,99,132,1)",
        type: 'line'
      }
    ];

    $scope.options = {
        legend: {
            display: true
        },
        scales: {
            yAxes: [
                {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    scaleLabel: {
                        display: true,
                        labelString: ""
                    }
                }
            ]
        },
        title: {
            display: true,
            text: ''
        }
    };

    $scope.nutrients = {};
    $scope.filteredNutrients = {};
    $scope.recommended = RecommendedValueService.recommendedValues;

    var getNutrientHist = function() {
        var fromDate = ReportsDateService.getFromDate();
        var toDate = ReportsDateService.getToDate();

        $http.post('/userarea/getNutrientHistory', {from:fromDate, to:toDate})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                    return;
                }
                if (data.nutrients){
                    //alert(JSON.stringify(data.balanceHist, null, 2));
                    //processData(data.balanceHist);
                    $scope.nutrients = data.nutrients;
                    $scope.filteredNutrients = $scope.nutrients;
                    $scope.selectionChanged(data.nutrients["203"]);
                }
            })
            .error(function (err) {
                alert(err);
            });
    };

    ReportsDateService.registerCallback(function () {
        getNutrientHist();
    });

    getNutrientHist();

    $scope.selectionChanged = function (nutrient) {
        $scope.data = [[],[]];
        $scope.labels = [];
        $scope.options.scales.yAxes[0].scaleLabel.labelString = nutrient.name + " (" + nutrient.unit + ")";
        $scope.options.title.text = nutrient.name + " Intake";
        var recommended = $scope.recommended[nutrient.id];
        if (!recommended){
            recommended = 0;
        }
        for (var i = 0; i < nutrient.history.length; i++){
            $scope.data[0].push(Math.floor(nutrient.history[i].consumption));
            $scope.data[1].push(recommended);
            $scope.labels.push(nutrient.history[i].date);
        }
    };

    $scope.searchChanged = function (text) {
        if (!text || text == ''){
            $scope.filteredNutrients = $scope.nutrients;
            return;
        }
        $scope.filteredNutrients = {};
        for (var nut_id in $scope.nutrients){
            var nutrient = $scope.nutrients[nut_id];
            if (nutrient.name.toLowerCase().indexOf(text.toLowerCase()) != -1){
                $scope.filteredNutrients[nut_id] = nutrient;
            }
        }
    };

    $scope.getDRVText = function (nutrient) {
        if ($scope.recommended[nutrient.id]){
            return $scope.recommended[nutrient.id] + " " + nutrient.unit;
        }else{
            return "n/a";
        }
    };

    $scope.getNutrientPercent = function (nutrient) {
        if ($scope.recommended[nutrient.id]){
            return 100 * nutrient.totalConsumption / nutrient.numberOfEntries / $scope.recommended[nutrient.id];
        }else{
            return "n/a";
        }
    }


});









