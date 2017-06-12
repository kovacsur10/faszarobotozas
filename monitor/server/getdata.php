<?php
	$servername = "localhost";
	$username = "robot";
	$password = "robot";
	$dbName = "robotics";
	
	$errorJson = '{"verdict": "error", "error_source": "';

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbName);

	// check connection
	if(mysqli_connect_errno()){
		$errorJson = $errorJson.'Connect failed: '.mysqli_connect_error().'"}';
		echo $errorJson;
		exit();
	}
	
	if($result = $conn->query("SELECT *  FROM state WHERE read_ = 0 ORDER BY id ASC LIMIT 1;")){
		$rows = [];
		$id = -1;
		while($r = $result->fetch_assoc()){
			$id = $r['id'];
			$rows[] = $r;
		}
		
		if(!$conn->query("UPDATE state SET read_ = 1 WHERE read_ = 0 AND id=".$id.";")){
			$errorJson = $errorJson.'UPDATE problem."}';
			echo $errorJson;
			exit();
		}
	}else{
		$errorJson = $errorJson.'SELECT problem."}';
		echo $errorJson;
		exit();
	}
	
	$conn->close();
	echo json_encode($rows);
?>