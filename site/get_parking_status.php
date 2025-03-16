<?php
header("Content-Type: application/json");
include 'dbconfig.php';

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    die(json_encode(["error" => "fail to connect to database: " . $conn->connect_error]));
}

// read ParkingLots list status
$sql = "SELECT Spotid, IsOccupied FROM ParkingLots";
$result = $conn->query($sql);

$parking_spots = [];
while ($row = $result->fetch_assoc()) {
    $parking_spots[] = [
        "id" => $row["Spotid"],
        "status" => $row["IsOccupied"] == 1 ? "occupied" : "available"
    ];
}

// echo status of parking lots
echo json_encode(["parking_spots" => $parking_spots]);

$conn->close();
?>