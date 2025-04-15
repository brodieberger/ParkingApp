import cv2
import json
import numpy as np
import mysql.connector
import dbconnect
import random
import time
from mysql.connector import Error

# Define parking spot coordinates
PARKING_SPOTS = {
    "Spot 1": (35, 70, 130, 263),
    "Spot 2": (155, 70, 240, 263),
    "Spot 3": (263, 70, 355, 263),
    "Spot 4": (373, 70, 460, 263),
    "Spot 5": (490, 70, 580, 263),
    "Spot 6": (35, 350, 130, 530),
    "Spot 7": (150, 350, 240, 530),
    "Spot 8": (263, 350, 355, 530),
    "Spot 9": (373, 350, 460, 530),
    "Spot 10": (483, 350, 580, 530),
}

# Function to check if contour is inside a parking spot
def is_car_inside_spot(contour, spot_coords):
    x, y, w, h = cv2.boundingRect(contour)
    sx1, sy1, sx2, sy2 = spot_coords
    return not (x > sx2 or x + w < sx1 or y > sy2 or y + h < sy1)

while True:
    # Load random image
    image_path = "images/parking_lot_" + str(random.randint(1, 8)) + ".jpg"
    image = cv2.imread(image_path)

    # Preprocess image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Process contours
    occupied_spots = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 1700 < area < 10000:
            for spot, coords in PARKING_SPOTS.items():
                if is_car_inside_spot(contour, coords):
                    occupied_spots.append(spot)

    # Generate parking status
    parking_status = {spot: "Occupied" if spot in occupied_spots else "Vacant" for spot in PARKING_SPOTS}

    # Save to JSON
    with open('output/parking_status.json', 'w') as f:
        json.dump(parking_status, f, indent=4)

    # Update database
    try:
        mydb = mysql.connector.connect(
            host=dbconnect.host,
            user=dbconnect.user,
            password=dbconnect.password,
            database=dbconnect.database
        )
        if mydb.is_connected():
            mycursor = mydb.cursor(dictionary=True)
            for spot, status in parking_status.items():
                spot_id = int(spot.split()[1])
                is_occupied = 1 if status == "Occupied" else 0
                mycursor.execute("UPDATE ParkingLots SET IsOccupied = %s WHERE Spotid = %s", (is_occupied, spot_id))
            mydb.commit()
            mycursor.close()
            print("Spots Updated!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if mydb.is_connected():
            mydb.close()

    # Draw result image
    for spot, (sx1, sy1, sx2, sy2) in PARKING_SPOTS.items():
        color = (0, 0, 255) if parking_status[spot] == "Occupied" else (0, 255, 0)
        cv2.rectangle(image, (sx1, sy1), (sx2, sy2), color, 2)
        cv2.putText(image, spot, (sx1, sy1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imwrite("output/output_parking_lot.jpg", image)
    print("Output stuff saved to output folder")

    # Wait for 10 seconds before repeating
    time.sleep(10)
