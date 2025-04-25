<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - Reservations</title>
    <link rel="stylesheet" href="styles.css"> <!-- Include your shared stylesheet if needed -->
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }

        .top-bar {
            background-color: #2c3e50;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }

        .main-content {
            padding: 30px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ccc;
            text-align: left;
        }

        th {
            background-color: #2c3e50;
            color: white;
        }

        .form-group {
            max-width: 300px;
            margin: 40px auto;
        }

        .form-group input {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        .form-group button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }

        .form-group button:hover {
            background-color: #45a049;
        }

        .delete-btn {
            background-color: #e74c3c;
            border: none;
            color: white;
            padding: 6px 10px;
            cursor: pointer;
        }

        .delete-btn:hover {
            background-color: #c0392b;
        }
    </style>
</head>

<body>
    <div class="top-bar">
        <div class="logo-section">
            <img src="https://static.wixstatic.com/media/7383ad_c9a2ed5d32704d6b81504a4175fa440c~mv2.png/v1/fill/w_400,h_400,al_c,q_85,usm_1.20_1.00_0.01,enc_avif,quality_auto/CBH%20Logo.png"
                alt="Kean Logo" class="logo" width="40" height="40">
            <span class="brand-name">Kean Parking - Admin</span>
        </div>
    </div>

    <div class="main-content" id="mainContent">
        <div class="form-group" id="pinForm">
            <h2>Enter Admin PIN</h2>
            <input type="password" id="adminPin" placeholder="Enter PIN">
            <button onclick="verifyPin()">Submit</button>
        </div>

        <div id="adminPanel" style="display: none;">
            <h2>Reservations Table</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User Email</th>
                        <th>Spot ID</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="reservationTableBody">
                    <!-- Fetched reservations will go here -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function verifyPin() {
            const enteredPin = document.getElementById('adminPin').value;
            if (enteredPin === '1234') {
                document.getElementById('pinForm').style.display = 'none';
                document.getElementById('adminPanel').style.display = 'block';
                fetchReservations();
            } else {
                alert('Incorrect PIN');
            }
        }

        function fetchReservations() {
    fetch('get_reservations.php')
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('reservationTableBody');
            tbody.innerHTML = '';
            data.forEach(res => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${res.id}</td>
                    <td>${res.user_email}</td>
                    <td>${res.spot_id}</td>
                    <td><button class="delete-btn" onclick="deleteReservation(${res.id})">Delete</button></td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching reservations:', error);
            alert('Failed to load reservations.');
        });
}


        function deleteReservation(id) {
            if (confirm('Are you sure you want to delete this reservation?')) {
                fetch('api/delete_reservation.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        fetchReservations();
                    } else {
                        alert('Failed to delete reservation.');
                    }
                });
            }
        }
    </script>
</body>

</html>
