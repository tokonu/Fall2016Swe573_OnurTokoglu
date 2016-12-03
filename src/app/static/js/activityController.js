'use strict';

app.controller('ActivityCtrl',function ($scope, UserInfoService, $http) {

    $scope.activities = {};
    $scope.filteredActivities = {};
    $scope.today = (new Date()).toString();
    var user = $scope.user = UserInfoService.getUser();

    var getActivities = function() {

        $http.post('/userarea/getActivities')
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                }else if (data.activities) {
                    $scope.activities = data.activities;
                    $scope.filteredActivities = $scope.activities;
                }
                //alert(JSON.stringify(data, null, 4));
            })
            .error(function (err) {
                alert(err);
            });

    };

    $scope.activityClicked = function (activity) {
        if (activity.detailVisible){
            activity.detailVisible = false;
            return;
        }
        activity.detailVisible = !activity.detailVisible;
    };

    $scope.getCalories = function(activity){
        var kcal = Math.round(activity.kcal_ph_pkg * user.weight * activity.duration / 60);
        activity["kcal"] = kcal;
        return kcal
    };

    $scope.searchChanged = function (text) {
        if (!text || text == ''){
            $scope.filteredActivities = $scope.activities;
            return;
        }
        $scope.filteredActivities = {};
        for (var id in $scope.activities){
            var activity = $scope.activities[id];
            if (activity.name.toLowerCase().indexOf(text.toLowerCase()) != -1){
                $scope.filteredActivities[id] = activity;
            }
        }
    };

    $scope.saveActivity = function (activity) {
        activity.date = $scope.date;
        $http.post('/userarea/saveActivity', {activity:activity})
            .success(function (data) {
                if (data.error){
                    alert(data.error);
                }else {
                    alert(data);
                }
                //alert(JSON.stringify(data, null, 4));
            })
            .error(function (err) {
                alert(err);
            });
    }


    getActivities();

}); 