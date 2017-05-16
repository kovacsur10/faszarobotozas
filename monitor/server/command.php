<?php
	$DEBUG = 0;

	$servername = "localhost";
	$username = "robot";
	$password = "robot";
	$dbName = "robotics";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbName);

	// check connection
	if(mysqli_connect_errno()) {
		if($DEBUG)
			printf("Connect failed: %s\n", mysqli_connect_error());
		echo "ERROR";
		exit();
	}
	if($DEBUG)
		echo "Connected successfully";
	
	if(!isset($_POST['action'])){
		if($DEBUG)
			printf("No posted value!\n");
		echo "ERROR";
		exit();
	}
	$action = $_POST['action'];
	
	switch($action){
		case "start":
		case "stop":
		case "add":
		case "remove":
		break;
		default:
			if($DEBUG)
				printf("Invalid action!\n");
			echo "ERROR";
			exit();
	}
	
	if(!isset($_POST['params'])){
		if($DEBUG)
			printf("No posted value!\n");
		echo "ERROR";
		exit();
	}
	$params = $_POST['params'];
	
	if($getActionId = $conn->prepare("SELECT id FROM actions WHERE name=?")){
		$getActionId->bind_param("s", $action);
		$getActionId->execute();
		$getActionId->bind_result($actionId);
		$getActionId->fetch();
		$getActionId->close();
		
		if($insertAction = $conn->prepare("INSERT INTO useractions (action, params) VALUES (?, ?)")){
			$insertAction->bind_param("is", $actionId, $params);
			$insertAction->execute();
			$insertAction->close();
		}else{
			if($DEBUG)
				printf("Prepare error! ".$conn->error."\n");
			echo "ERROR";
			exit();
		}
	}else{
		if($DEBUG)
			printf("Prepare error! ".$conn->error."\n");
		echo "ERROR";
		exit();
	}
	
	
	
	//cleanup
	$conn->close();
	echo "OK";
?>