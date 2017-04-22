'use strict';
angular.module('sps', ['ngRoute', 'ngWebSocket'])
.config(function ($httpProvider) {
  $httpProvider.defaults.headers.common = {};
  $httpProvider.defaults.headers.post = {};
  $httpProvider.defaults.headers.put = {};
  $httpProvider.defaults.headers.patch = {};
})
.config(function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl : 'nosong.html',
                controller  : ''
            })
            .when('', {
                templateUrl : 'nosong.html',
                controller  : ''
            })
            .when('/about', {
                templateUrl : 'about.html',
                controller  : ''
            })
            .when('/:id', {
                templateUrl : 'showsong.html',
                controller  : 'ShowsongController'
            })
            .otherwise('/');
    });

var hideit = function () {
    $('#nowInGroup').hide();
    $('#leaderPanel').hide();
    $('#userPanel').hide();
};

var groupWebSocket = {};