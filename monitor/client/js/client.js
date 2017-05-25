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

class Robot {
  constructor(){
    this.setPosition(leftTop.lat, leftTop.lon);
  }
  
  setPosition(lat, lon){
    this.lat = lat;
    this.lon = lon;
    $("#robot").css({left: 1127 - ((rightBottom.lon - this.lon) * dimensions.width) - 20, top: (leftTop.lat - this.lat) * dimensions.height - 20});
  }
  
  setRotation(angle){
    this.angle = angle;
    $("#robot").css({transform: "rotate("+(-angle-90.0)+"deg)"});
  }
}

let robot = new Robot();




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

/*$(function(){
	setInterval(function() {
		$.getJSON({
			url: urlTag+"getdata.php",
			success: function(value){
				console.log(value);
			}
		});
	}, 1000);
});*/

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

robot.setPosition(47.47402, 19.05793);
robot.setRotation(20.0);