<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);

    // Match JS variable names
    $userEmail = $data['username'] ?? null;
    $spotId = $data['spot_id'] ?? null;

    // Campus is no longer required
    if (!$userEmail || !$spotId) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing required fields']);
        exit;
    }

    $conn = new mysqli('localhost', 'root', '', 'parking_app');

    if ($conn->connect_error) {
        http_response_code(500);
        echo json_encode(['error' => 'Database connection failed']);
        exit;
    }

    // You can adjust the query if "campus" is no longer needed in the table
    $stmt = $conn->prepare("INSERT INTO reservations (user_email, spot_id) VALUES (?, ?)");
    $stmt->bind_param('si', $userEmail, $spotId);

    if ($stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'Reservation added successfully']);
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to add reservation']);
    }

    $stmt->close();
    $conn->close();
}
?>
