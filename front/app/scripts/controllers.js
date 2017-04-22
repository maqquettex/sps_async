'use strict';

angular.module('sps')

.controller('ShowsongController', ['$scope', '$routeParams', 'songFactory', function($scope, $routeParams, songFactory) {
    $scope.message = 'Loading...';
    $scope.showMessage = true;
    $scope.inGroup = songFactory.getInGroup();
    $scope.proposed = songFactory.getProposed();
    if ($scope.inGroup) {
        $('#propButton').show(100);
    }
    $scope.isProposed = function(id) {
        if (!$scope.inGroup)
            return false;
        for (var i = 0; i < $scope.proposed.length; i++) {
            if ($scope.proposed[i].id === id) {
                console.log(true);
                return true;
            }
            return false;
        }
    };
    $scope.song = songFactory.getSong(parseInt($routeParams.id,10)).then(
        function(response) {
            $scope.song = response.data;
            $scope.showMessage = false;
        },
        function(response) {
            $scope.message = "Something went wrong: "+response.status + " " + response.statusText;
            $scope.showMessage = true;
        }
    );
}])
.controller('GroupController', ['$scope', 'groupFactory', 'songFactory', '$websocket', '$location', function($scope, groupFactory, songFactory, $websocket, $location) {
    var newSong = {};
    $scope.addSongArtist = '';
    $scope.addSongTitle = '';
    $scope.addSongText = '';
    $scope.showAddSongNew = false;
    $scope.showAddSongNotFound = false;
    $scope.showAddSongInputProblem = false;
    $scope.showAddSongLoading = false;
    $scope.firstinit = true;
    $scope.inGroup = false;
    $scope.isLeader = false;
    $scope.token = '0';
    $scope.socket = {};
    $scope.isInGroup = function() {
        return $scope.inGroup;
    };
    $scope.$watch('inGroup', function(newValue, oldValue) { //triggers animation when state changes
        console.log(oldValue + ' ' + newValue);
        if (newValue != oldValue && newValue) {
            songFactory.setInGroup(newValue);
            $('#notInGroup').hide(200);
            $('#nowInGroup').show(200);
            console.log('show');
            if (!$scope.isLeader) {
                $('#userPanel').show(200);
            }
        } else if (newValue != oldValue && !newValue) {
            songFactory.setInGroup(newValue);
            $('#nowInGroup').hide(200);
            $('#notInGroup').show(200);
            console.log('hide');
            if (!$scope.isLeader) {
                $('#userPanel').hide(200);
            }
        }
    });
    $scope.$watch('isLeader', function(newValue, oldValue) { // as higher
        if (newValue != oldValue && newValue) {
            $('#leaderPanel').show(200);
        } else if (newValue != oldValue && !newValue) {
            $('#leaderPanel').hide(200);
        } 
    });
    $scope.nowplaying = 0;
    $scope.proposed = [];
    var proposedToggle = [];
    $scope.joinGroupName = "";
    $scope.createGroupName = "";
    $scope.showGroupNameReq = false;
    $scope.showGroupServerProblem = false;
    $scope.showGroupNameProblem = false;
    $scope.createGroup = function() {
        if ($scope.createGroupName == "") {
            $scope.showGroupNameReq = true;
            return;
        }
        var res = groupFactory.createGroup($scope.createGroupName);
        if (res == 1) {
            $scope.showGroupServerProblem = true;
            return;
        }
        if (res == 2) {
            $scope.showGroupNameProblem = true;
            return;
        }
        $scope.socketer(groupFactory.connect());
        console.log($scope.socket);
        $scope.showGroupNameReq = false;
        $scope.showGroupServerProblem = false;
        $scope.showGroupNameProblem = false;
        $scope.inGroup = true;
        $scope.isLeader = true;
        $('#createGroupModal').modal('hide');
        $('#propButton').show(100);
        $scope.token = groupFactory.getToken();
    };
    $scope.joinGroup = function() {
        if ($scope.joinGroupName == "") {
            $scope.showGroupNameReq = true;
            return;
        }
        var res = groupFactory.joinGroup($scope.joinGroupName);
        if (res == 1) {
            $scope.showGroupServerProblem = true;
            return;
        }
        if (res == 2) {
            $scope.showGroupNameProblem = true;
            return;
        }
        $scope.socketer(groupFactory.connect());
        $scope.showGroupServerProblem = false;
        $scope.showGroupNameProblem = false;
        $scope.showGroupNameReq = false;
        $scope.inGroup = true;
        console.log($scope.socket);
        $('#joinGroupModal').modal('hide');
        $('#propButton').show(100);
        $scope.token = groupFactory.getToken();
    };
    $scope.socketer = function(link) {
        $scope.socket = new WebSocket(link);
        console.log($scope.socket);
        $scope.socket.onmessage = function(event) {
            var jsonmes = JSON.parse(event.data);
            console.log(jsonmes);
            console.log(jsonmes.action)
            if (typeof jsonmes.action == 'undefined') {
                var jsonmes = JSON.parse(event.data);
                $scope.proposed = [];
                $scope.nowplaying = jsonmes.current;
                if (jsonmes.current != 0) {
                    songFactory.getSongInfo(jsonmes.current).then(
                        function(response) {
                            var song = {};
                            song = response.data;
                            $scope.proposed.push(song);
                            songFactory.setProposed($scope.proposed);

                            $scope.proposed.forEach(function(element, index, array) {
                                var x = {};
                                x.id = element;
                                x.state = false;
                                proposedToggle.push(x);
                            });
                        }, 
                        function(response) {
                            var song = {};
                            song.artist = response.status;
                            song.title = response.statusText;
                            $scope.proposed.push(song);
                        }
                    );
                }
                jsonmes.proposed.forEach(function(element, index, array) {
                    var song = {};
                    if (element != jsonmes.current) {
                        songFactory.getSongInfo(element).then(
                            function(response) {
                                song = response.data;
                                $scope.proposed.push(song);
                                songFactory.setProposed($scope.proposed);

                                $scope.proposed.forEach(function(element, index, array) {
                                    var x = {};
                                    x.id = element.id;
                                    x.state = false;
                                    proposedToggle.push(x);
                                });
                            }, 
                            function(response) {
                                song.artist = response.status;
                                song.title = response.statusText;
                                $scope.proposed.push(song);
                        });
                    }
                });
            }
            if (jsonmes.action == 'propose') {
                var dup = false;
                $scope.proposed.forEach(function(element, index, array) {
                    if (jsonmes.song === element.id)
                        dup = true;
                });
                if (!dup) {
                    var song = {};
                    songFactory.getSongInfo(jsonmes.song).then(
                        function(response) {
                            song = response.data;
                            $scope.proposed.push(song);
                            songFactory.setProposed($scope.proposed);
                            var toggledata = {};
                            toggledata.id = jsonmes.song;
                            toggledata.state = false;
                            proposedToggle.push(toggledata);
                            $scope.$apply();
                        }, 
                        function(response) {
                            song.artist = response.status;
                            song.title = response.statusText;
                            $scope.proposed.push(song);
                    });
                }
            }
            if (jsonmes.action == 'ignore') {
                if (jsonmes.song == $scope.nowplaying && $scope.isLeader)
                    return;
                $scope.proposed.forEach(function(element, index, array) {
                    if (element.id === jsonmes.song) {
                        $scope.proposed.splice(index, 1);
                        proposedToggle.splice(index, 1);
                        songFactory.setProposed($scope.proposed);
                    }
                });
            }
            if (jsonmes.action == 'choose') {
                if ($scope.nowplaying == jsonmes.song)
                    return;
                $scope.deleteProposed($scope.nowplaying);
                console.log($scope.socket);
                var dup = false;
                $scope.proposed.forEach(function(element, index, array) {
                    if (jsonmes.song === element.id)
                        dup = true;
                });
                if (!dup) {
                    var song = {};
                    songFactory.getSongInfo(jsonmes.song).then(
                        function(response) {
                            song = response.data;
                            $scope.proposed.push(song);
                            songFactory.setProposed($scope.proposed);
                            var toggledata = {};
                            toggledata.id = jsonmes.song.id;
                            toggledata.state = false;
                            proposedToggle.push(toggledata);
                            $scope.$apply();
                        }, 
                        function(response) {
                            song.artist = response.status;
                            song.title = response.statusText;
                            $scope.proposed.push(song);
                    });
                }
                $scope.nowplaying = jsonmes.song;
            }
            if (jsonmes.action == 'delete') {
                proposedToggle = [];
                $scope.proposed = [];
                $scope.nowplaying = 0;
                $scope.leave();
                $scope.socket.close();
            }
            $scope.$apply();
        };
    };
    $scope.toggleMenu = function(id) {
        var state = false;
        proposedToggle.forEach(function(element, index, array) {
            if (element.id === id) {
                array[index].state = !array[index].state;
                state = array[index].state;
            }
        });
        console.log('State of ' + id + ' ' + state);
        console.log(proposedToggle);
        if (state) {
            $('#songDisp' + id).hide(200);
            $('#songMenu' + id).show(200);
        } else {
            $('#songMenu' + id).hide(200);
            $('#songDisp' + id).show(200);
        };
    };
    $scope.propose = function(song) {
        console.log($scope.socket);
        var dup = false;
        $scope.proposed.forEach(function(element, index, array) {
            if (song.id === element.id && !$scope.isLeader)
                dup = true;
            else if ($scope.isLeader) {
                $scope.play(song.id);
                dup = true;
            }
        });
        if (!dup) {
            $scope.proposed.push(song);
            songFactory.setProposed($scope.proposed);
            var toggledata = {};
            toggledata.id = song.id;
            toggledata.state = false;
            proposedToggle.push(toggledata);
            if (!$scope.isLeader) {
                var senddata = {};
                senddata.song = song.id;
                $scope.socket.send(JSON.stringify(senddata));
            } else {
                $scope.play(song.id);
            }
        }
    };
    $scope.play = function (id) {
        $scope.deleteProposed($scope.nowplaying);
        $scope.nowplaying = id;
        var isProposed = false;
        for (var i = 0; i < $scope.proposed.length; i++) {
            if ($scope.proposed[i].id === id) {
                isProposed = true;
            }
        }
        if (isProposed = false) {
            songFactory.getSongInfo(id).then(
                function(response) {
                    var song = {};
                    song = response.data;
                    $scope.proposed.push(song);
                    songFactory.setProposed($scope.proposed);
                    var x = {};
                    x.id = id;
                    x.state = false;
                    proposedToggle.push(x);
                },
                function(response) {
                    var song = {};
                    song.artist = response.status;
                    song.title = response.statusText;
                    $scope.proposed.push(song);
                }
            );
        }
        var senddata = {};
        senddata.action = 'choose';
        senddata.song = id;
        $scope.socket.send(JSON.stringify(senddata));
    };
    $scope.leave = function() {

        proposedToggle = [];
        $scope.proposed = [];
        $scope.nowplaying = 0;
        $scope.inGroup = false;
        $('#nowInGroup').hide(200);
        $('#notInGroup').show(200);
        console.log('hide');
        $('#userPanel').hide(200);
        $('#propButton').hide(100);
        $scope.socket.close();
    }
    $scope.delete = function() {
        $('#propButton').hide(100);
        proposedToggle = [];
        $scope.proposed = [];
        $scope.nowplaying = 0;
        $scope.inGroup = false;
        $scope.isLeader = false;
        $('#nowInGroup').hide(200);
        $('#notInGroup').show(200);
        console.log('hide');
        $('#leaderPanel').hide(200);
        var senddata = {};
        senddata.action = 'delete';
        $scope.socket.send(JSON.stringify(senddata));
        $scope.socket.close();
    };
    $scope.deleteProposed = function(id) {
        $scope.proposed.forEach(function(element, index, array) {
            if (element.id === id) {
                $scope.proposed.splice(index, 1);
                proposedToggle.splice(index, 1);
                songFactory.setProposed($scope.proposed);
                var senddata = {};
                senddata.action = 'ignore';
                senddata.song = id;
                $scope.socket.send(JSON.stringify(senddata));
            }
        });
    };
    $scope.addSong = function() {
        songFactory.addSong(newSong.id).then(
            function(response) {
                if (isInGroup && isLeader) {
                    $location.path("/"+response.data.id+"/");
                    return;
                }
                if (isInGroup && !isLeader) {
                    $location.path("/"+response.data.id+"/");
                    return;
                }
                $location.path("/"+response.data.id+"/");
            },
            function(response) {
                $scope.showMessage = true;
                $scope.message = "Something went wrong: "+response.status + " " + response.statusText;
            }
        );
    }
    $scope.askSong = function() {
        $scope.showAddSongLoading = true;
        $scope.showAddSongNew = false;
        $scope.showAddSongNotFound = false;
        $scope.showAddSongInputProblem = false;
        if ($scope.addSongArtist == "" || $scope.addSongTitle == "") {
            $scope.showAddSongInputProblem = true;
            return;
        }
        songFactory.askSong($scope.addSongArtist, $scope.addSongTitle).then(
            function(response) {
                console.log(response);
                newSong = response.data;
                $scope.showAddSongLoading = false;
                //if ($scope.addSongArtist != newSong.artist || $scope.addSongTitle != newSong.title || jQuery.isEmptyObject(newSong)) {
                if (jQuery.isEmptyObject(newSong)) {
                    $scope.showAddSongNotFound = true;
                    return;
                }
                $scope.addSongText = newSong.text;
                $scope.showAddSongNew = true;
                //$scope.showAddSongNew = false; ?????????????????
                $scope.showAddSongNotFound = false;
                $scope.showAddSongInputProblem = false;
            },
            function(response) {
                $scope.showAddSongLoading = false;
                console.log(response);
                $scope.showGroupServerProblem = true;
            }
        );

    }
}])
.controller('SearchController', ['$scope', 'songFactory', function($scope, songFactory) {
    $scope.message = 'Loading...';
    $scope.showMessage = true;
    $scope.searchText = "";
    /*$scope.artists = songFactory.getArtists().then(
        function(response) {
            $scope.artists = response.data;
            $scope.showMessage = false;
        },
        function(response) {
            $scope.message = "Something went wrong: "+response.status + " " + response.statusText;
            $scope.showMessage = true;
        }
    );*/
    $scope.songsInfo = songFactory.getSongsInfo().then(
        function(response) {
            $scope.songsInfo = response.data;
            $scope.showMessage = false;
        },
        function(response) {
            $scope.message = "Something went wrong: "+response.status + " " + response.statusText;
            $scope.showMessage = true;
        }
    );
}]);