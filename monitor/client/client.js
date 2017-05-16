var counter = 0;
var urlTag = "http://localhost/server/";

function startRobot(){
  ajaxRequest("start", {}, function(value){
    $("#alma").html(value);
  });
}

function stopRobot(){
  ajaxRequest("stop", {}, function(value){
    $("#alma").html(value);
  });
}

function addCheckpoint(latitude, longitude){
  counter++;
  ajaxRequest("add", {id: counter, lat: latitude, lon: longitude}, function(value){
    $("#alma").html(value);
  });
}

function removeCheckpoint(id_val){
  ajaxRequest("remove", {id: id_val}, function(value){
    $("#alma").html(value);
  });
}

function ajaxRequest(mode, param_values, fun){
  var jsonParam = JSON.stringify(param_values, null, 2);
  $.ajax({
    url: urlTag+"command.php", 
    type: "POST",
    xhrFields: {
      withCredentials: false
    },
    crossDomain: true,
    data: {
      action: mode,
      params: jsonParam
    },
    success: fun
  });
}