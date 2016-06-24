'use strict';

var Devourer = angular.module('Devourer', [
    'ngFileUpload'
])
.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}])
;
