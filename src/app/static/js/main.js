'use strict';

var app = angular.module('foodApp',['ui.router','720kb.datepicker','chart.js']);

app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/eat')
    .when("/eat", "/eat/myfoods")
    .when("/reports", "/reports/weight");

    $stateProvider

        .state('eat',{
            url: '/eat',
            views: {
                '' : {
                    templateUrl : '../static/partials/food/food.html'
                },
                'mealbox@eat' : {
                    templateUrl : '../static/partials/food/mealbox.html'
                }
            }
        })
        .state('eat.search',{
            url: '/search',
            templateUrl: '../static/partials/food/food-search.html',
            controller: 'FoodSearchCtrl'
        })
        .state('eat.myfoods',{
            url: '/myfoods',
            templateUrl: '../static/partials/food/my-foods.html',
            controller: 'MyFoodsCntr'
        })
        .state('eat.mymeals',{
            url: '/mymeals',
            templateUrl: '../static/partials/food/my-meals.html',
            controller: 'MyMealsCntr'
        })


        .state('activity',{
            url: '/activity',
            views: {
                '' : {
                    templateUrl : '../static/partials/activity/activity.html',
                    controller: 'ActivityCtrl'
                }
            }
        })

        .state('reports',{
            url: '/reports',
            templateUrl: '../static/partials/report/reports.html',
            controller: 'ReportsCtrl'
        })
        .state('reports.weight',{
            url: '/weight',
            templateUrl: '../static/partials/report/reports-weight.html',
            controller: 'ReportsWeightCtrl'
        })
        .state('reports.myfoods',{
            url: '/myfoods',
            templateUrl: '../static/partials/report/myfoods.html',
            controller: 'ReportsMyFoodsCtrl'
        })
        .state('reports.balance',{
            url: '/balance',
            templateUrl: '../static/partials/report/balance.html',
            controller: 'ReportsBalanceCtrl'
        })
        .state('reports.nutrition',{
            url: '/nutrition',
            templateUrl: '../static/partials/report/nutrition.html',
            controller: 'ReportsNutrientCtrl'
        })
    ;


});
