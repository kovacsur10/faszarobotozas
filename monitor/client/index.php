<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Robot monitoring</title>
	<script type="text/javascript" src="js/jquery.js"></script>
	<script type="text/javascript" src="js/stringify.js"></script>
	<link href="css/main.css" rel="stylesheet" type="text/css">
</head>
<body>
	<div id="map">
		<div id="robot"></div>
	</div>
	<div style="z-index:3;">
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
	</div>
	
	<script type="text/javascript" src="js/client.js"></script>
</body>
</html>