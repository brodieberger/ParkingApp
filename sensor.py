#This is an old implementation when we were going with a sensor idea. Keeping this in here anyway

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="parking_app"
)
mycursor = mydb.cursor(dictionary=True)

def check(spots):
    for spot in spots:
        if spot['is_occupied'] == 0:
            print("Spot open!")
        else:
            print("Spot full")

while(True):
    mycursor.execute("SELECT is_occupied FROM parking_spots")
    spots = mycursor.fetchall()
    check(spots)

    input("")
    mycursor.execute("UPDATE `parking_spots` SET `is_occupied` = '1' WHERE `parking_spots`.`id` = 1")
    mydb.commit()

    mycursor.execute("SELECT is_occupied FROM parking_spots")
    spots = mycursor.fetchall()
    check(spots)

    input("")
    mycursor.execute("UPDATE `parking_spots` SET `is_occupied` = '0' WHERE `parking_spots`.`id` = 1")
    mydb.commit()