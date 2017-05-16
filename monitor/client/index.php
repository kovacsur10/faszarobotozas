<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Robot monitoring</title>
	<script type="text/javascript" src="jquery.js"></script>
	<script type="text/javascript" src="stringify.js"></script>
</head>
<body>
	<h1>Hello!</h1>
	<div id="alma"></div>
	
	<p>Latitude: </p>
	<input id="latitudeInput" type="text" />
	
	<p>Longitude: </p>
	<input id="longitudeInput" type="text" />
	
	<p>Checkpoint id: </p>
	<input id="idInput" type="text" /><br>
	
	<button id="startButton">START!</button>
	<button id="stopButton">STOP!</button>
	<button id="addCheckpointButton">ADD!</button>
	<button id="removeCheckpointButton">REMOVE!</button>
	
	<script type="text/javascript" src="client.js"></script>
	<script type="text/javascript">		
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
	</script>
</body>
</html>