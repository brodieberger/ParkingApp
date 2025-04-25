<?php
header('Content-Type: application/json');

// Database connection (adjust these as needed)
include 'dbconfig.php';

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

$sql = "SELECT id, username, spot_id, created_at FROM reservations ORDER BY created_at DESC";
$result = $conn->query($sql);

$reservations = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $reservations[] = $row;
    }
}

echo json_encode($reservations);

$conn->close();
?>
