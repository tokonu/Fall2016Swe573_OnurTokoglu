'use strict';

var app = angular.module('foodApp',['ui.router','720kb.datepicker']);

app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/eat')
    .when("/eat", "/eat/myfoods");

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
            templateUrl: '../static/partials/food/my-foods.html'
        })
        .state('eat.mymeals',{
            url: '/mymeals',
            templateUrl: '../static/partials/food/my-meals.html'
        })


    ;
});
