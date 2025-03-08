import cv2
import json
import numpy as np

# Define parking spot coordinates. You can use microsoft paint to get these. Should be (X1, Y1, X2, Y2).
# Must be hardcoded for each image.
PARKING_SPOTS = {
    "Spot 1": (30, 70, 130, 300),
    "Spot 2": (140, 70, 240, 300),
    "Spot 3": (260, 70, 360, 300),
    "Spot 4": (370, 70, 460, 300),
    "Spot 5": (480, 70, 580, 300),
    "Spot 6": (30, 320, 130, 530),
    "Spot 7": (140, 320, 240, 530),
    "Spot 8": (260, 320, 360, 530),
    "Spot 9": (370, 320, 460, 530),
    "Spot 10": (480, 320, 580, 530),
}

# Load image
image_path = 'images/parking_lot.jpg'
image = cv2.imread(image_path)

# Make image work better for image recognition. This was all copy pasted from stack overflow so not 100% sure how it all works.
# Currently it doesn't work 100% of the time. Probably only 8/10 times from what I tested.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Function to check if contour is inside a parking spot. Takes parameters for contour and spot coordinates.
def is_car_inside_spot(contour, spot_coords):
    x, y, w, h = cv2.boundingRect(contour)
    sx1, sy1, sx2, sy2 = spot_coords
    return not (x > sx2 or x + w < sx1 or y > sy2 or y + h < sy1)

# Process contours to determine occupancy
occupied_spots = []

# Sometimes theres more contours than there are parking spots. Shouldn't be a problem though since theres a limit of 10 spots.
for contour in contours:
    area = cv2.contourArea(contour)
    # Ignore small objects (noise) and very large objects (not cars)
    if 1000 < area < 10000:  
        for spot, coords in PARKING_SPOTS.items():
            if is_car_inside_spot(contour, coords):
                occupied_spots.append(spot)

# Generate final parking status
parking_status = {spot: "Occupied" if spot in occupied_spots else "Vacant" for spot in PARKING_SPOTS}

# Save results to JSON file. TODO this should go into a database. Currently not at Kean so I dont feel like setting up the firewall
with open('output/parking_status.json', 'w') as f:
    json.dump(parking_status, f, indent=4)

# Draw results on image. Would be cool for the showcase but we don't really need this cause of the whole privacy issue.
for spot, (sx1, sy1, sx2, sy2) in PARKING_SPOTS.items():
    color = (0, 0, 255) if parking_status[spot] == "Occupied" else (0, 255, 0)
    cv2.rectangle(image, (sx1, sy1), (sx2, sy2), color, 2)
    cv2.putText(image, spot, (sx1, sy1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imwrite("output/output_parking_lot.jpg", image)
print("Output stuff saved to output folder")
