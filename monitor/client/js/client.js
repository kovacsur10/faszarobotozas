var counter = 0;
var urlTag = "http://localhost/server/";

var leftTop = {
  lat: 47.475236,
  lon: 19.054363
};

var rightBottom = {
  lat: 47.471142,
  lon: 19.064553
};

var dimensions = {
  width: 1127 / (rightBottom.lon - leftTop.lon),
  height: 677 / (leftTop.lat - rightBottom.lat) 
};

var dimensionsInv = {
  width: (rightBottom.lon - leftTop.lon) / 1127,
  height: (leftTop.lat - rightBottom.lat) / 677 
};

class Robot {
  constructor(){
    this.setPosition(leftTop.lat, leftTop.lon);
  }
  
  setPosition(lat, lon){
    this.lat = lat;
    this.lon = lon;
    $("#robot").css({left: Math.round((1127 - ((rightBottom.lon - this.lon) * dimensions.width))-20), top: Math.round(((leftTop.lat - this.lat) * dimensions.height)-20)});
  }
  
  setPositionT(lat, lon){
    var tmp = transformPosition(lat, lon);
    this.setPosition(tmp.lat, tmp.lon);
  }
  
  setRotation(angle){
    this.angle = angle;
    $("#robot").css({'transform': "rotate("+(-angle-90.0)+"deg)"});
  }
}

let robot = new Robot();
var checkpoints = [];


function transformPosition(latIn, lonIn){
  return {
    lat: Math.trunc(latIn) +  (latIn - Math.trunc(latIn)) * (10.0 / 6),
    lon: Math.trunc(lonIn) +  (lonIn - Math.trunc(lonIn)) * (10.0 / 6)
  };
}

function transformPositionBack(latIn, lonIn){
  return {
    lat: Math.trunc(latIn) +  (latIn - Math.trunc(latIn)) * (6.0 / 10),
    lon: Math.trunc(lonIn) +  (lonIn - Math.trunc(lonIn)) * (6.0 / 10)
  };
}

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

$(function(){
	setInterval(function() {
		$.getJSON({
			url: urlTag+"getdata.php",
			success: function(value){
        if(value.length != 0){
          value = value[0]
          console.log(value);
          
          $("#time").html(value.timestamp);
          $("#distance").html(value.distance);
          $("#faceAngle").html(value.faceAngle);
          $("#cpAngle").html(value.cpAngle);
          $("#turning").html(value.turning == "1" ? "Igen" : "Nem");
          $("#moving").html(value.moving == "1" ? "Igen" : "Nem");
          checkpoints = value.checkpoints;
          
          robot.setPositionT(value.latitude, value.longitude);
          robot.setRotation(value.faceAngle);
        }
        drawCheckpoints();
			}
		});
	}, 100000000);
});

function drawCheckpoints(){
  $(".cp").remove();
  for(var i = 0; i < checkpoints.length; i++){
    var pos = transformPosition(checkpoints[i].lat, checkpoints[i].lon);   
    $("#map").append("<div id='"+checkpoints[i].id+"' class='cp' style='left:"+Math.round((1127 - ((rightBottom.lon - pos.lon) * dimensions.width)) - 5)+"px;top:"+Math.round(((leftTop.lat - pos.lat) * dimensions.height) - 5)+"px;'></div>");
  }
}

$("#startButton").click(startRobot);
$("#stopButton").click(stopRobot);
$("#addCheckpointButton").click(function(){
  latval = parseFloat($("#latitudeInput").val());
  lonval = parseFloat($("#longitudeInput").val());
  identifier = parseInt($("#idInput").val());
  if(!isNaN(latval) && !isNaN(lonval) && !isNaN(identifier)){
    addCheckpoint(latval, lonval);
  }else{
    alert("Valós/egész értékek legyenek!");
  }		
});
$("#removeCheckpointButton").click(function(){
  identifier = parseInt($("#idInput").val());
  if(!isNaN(identifier)){
    removeCheckpoint(identifier);
  }else{
    alert("Egész érték legyen!");
  }		
});

$("#map").click(function(e){
  var posX = $(this).position().left;
  var posY = $(this).position().top;
  var lat = rightBottom.lat + dimensionsInv.height / (677 - (e.pageY - posY));
  var lon = leftTop.lon + dimensionsInv.width * (e.pageX - posX);
  var pos = transformPositionBack(lat, lon);
  
  $("#latitudeInput").val(pos.lat);
  $("#longitudeInput").val(pos.lon);
});

//robot.setPosition(47.47402, 19.05793);
robot.setPositionT(47.284429, 19.034813);
robot.setRotation(0.0);
checkpoints = [{
  id: "alma",
  lat: 47.284429,
  lon: 19.034813
},
{
  id: "korte",
  lat: 47.28268,
  lon: 19.0349
}];
drawCheckpoints();