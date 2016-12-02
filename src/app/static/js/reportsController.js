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

    $scope.fromDate = "03-11-2016";
    $scope.toDate = "25-11-2016";

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

    //getWeightHist();

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
















