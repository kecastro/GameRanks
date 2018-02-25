/**
 * Created by kevincastro on 2/5/18.
 */
var app = angular.module("Trade", []);



app.controller("trade", function($scope, $http, $location) {

    $scope.myquery = "";
    $scope.game_not_exist = false;

    $scope.games_list = [];

    $scope.consoles = ["Xbox One", "Xbox 360", "PlayStation 3", "PlayStation 4", "PlayStation Vita", "Wii U", "Nintendo 3DS"];

    $scope.search = function(){

        $scope.searchResult = null;

        if($scope.myquery.length > 2 ){
        $http.get("/tradesearch/" + $scope.myquery)
            .then(function (response) {
                $scope.searchResult = response.data;
                if($scope.searchResult.length > 0)
                    $scope.game_not_exist = false;
                else
                    $scope.game_not_exist = true;
            });
        }
        else
            $scope.game_not_exist = false;
    };

    $scope.add_trade = function(game_id, game_name, game_cover, game_platforms){
        $scope.myquery="";
        $scope.search();
        $scope.exist = false;
        $scope.malert = false;

        for (var i = 0; i < $scope.games_list.length; i++){
            if ($scope.games_list[i]["id"] == game_id) {
                $scope.alert_message = 'El juego ya ha sido agregado'
                $scope.exist = true;
                $scope.malert = true;
            }
        }

        if(!$scope.exist){
            $scope.games_list.push({id: game_id, name: game_name, opt: game_platforms , type: false ,platform: null});
        }
    };

    $scope.remove_game = function(game_id){
        for (var i = 0; i < $scope.games_list.length; i++){
            if ($scope.games_list[i]["id"] == game_id) {
                $scope.games_list.splice(i);
            }
        }
    };

    $scope.update_platform = function(platform){
        var sel = platform.split(',');
        for (var i = 0; i < $scope.games_list.length; i++){
            if ($scope.games_list[i]["id"] == sel[0]) {
                $scope.games_list[i]["platform"] = sel[1];
            }
        }
    };

      $scope.type_select = function(game_id, type){
       for (var i = 0; i < $scope.games_list.length; i++){
           if ($scope.games_list[i]["id"] == game_id) {
               $scope.games_list[i]["type"] = type;
           }
       }
    };

    $scope.exchange = function(){

        $http.defaults.xsrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';

        $scope.send_django = []

        for (var i = 0; i < $scope.games_list.length; i++){
             $scope.send_django.push({id: $scope.games_list[i]["id"], platform: $scope.games_list[i]["platform"], type: $scope.games_list[i]["type"]})
        }

        $scope.can_send = true;

        for (var i = 0; i < $scope.games_list.length; i++){
            if ($scope.games_list[i]["platform"] == null){
                $scope.can_send = false;
            }
        }

        if($scope.can_send){
            $http.post("", $scope.games_list)
             .then(function (response) {
                if(response.status == 200){
                    window.location.replace('/user/current');
                }
                else{
                    console.log(response.status)
                    $scope.alert_message = "Hubo un problema generando el intercambio";
                    $scope.malert = true;
                }
             });
        }
        else{
            $scope.alert_message = "Debe seleccionar una consola para los juegos";
            $scope.malert = true;
        }



    };

});
