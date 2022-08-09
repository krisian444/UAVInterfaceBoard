# Module: Interface Board Data Readout
# Description: This script is to read data from I2C interface board and display the readings using OpenCV
# Name: Krisian Bargas
#       ECE 491 Group 9
# Copyright: yes
# Rev Number: V1
# Rev Notes: n/a

import cv2
import numpy as np
import time
import board
import busio

import adafruit_gps
import adafruit_icm20x
from TFmini_I2C import TFminiI2C as tf

# initialize window size for viewing and text locations in image
height = 480
width = 640

gpsXloc = 35
gpsYloc = 50

imuXloc = 35
imuYloc = 180

lidXloc = 35
lidYloc = 375


# I2C interface to read the pins
i2c = board.I2C()

# Instance for IMU
icm = adafruit_icm20x.ICM20649(i2c)

# create a GPS module instance.
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# create instance for LIDAR
lidar = tf(1, 0x11)

# Turn on the basic GGA and RMC info (what you typically want), refer to NMEA for
# more information
# sends command to GPS to read 
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# update polling data from GPS by 1 per second (1Hz) - get info every second
# in milliseconds
gps.send_command(b"PMTK220,1000")

# Main loop runs forever printing the location, etc.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data
    frame = np.zeros((height, width, 3), np.uint8)
    
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            #continue
            lat = str("No fix yet...")
            long = str("No fix yet...")
        else:
            lat = gps.latitude
            long = format(gps.longitude)
        # Print out location: longitude and latitude
        print("=" * 40)  # Print a separator line.
        

        gyroX, gyroY, gyroZ = icm.gyro
        accX, accY, accZ = icm.acceleration
        lidDist = lidar.readDistance() / 100 # reading is in cm, changing to meters

       # print out values  
       # print("Latitude: {0:.6f} degrees".format(gps.latitude))
       # print("Longitude: {0:.6f} degrees".format(gps.longitude))
       # print("Gyro readings: X:%.2f, Y: %.2f, Z: %.2f rad/s" % (icm.gyro))
        #print("Acceleromter readings: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
        
        # print values on display
        cv2.putText(frame, "GPS Adafruit 1010D Module", (gpsXloc, gpsYloc), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, "Latitude: " + str(lat) +" deg", (gpsXloc, gpsYloc + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "Longitude: " + str(long) +" deg", (gpsXloc, gpsYloc + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        # the functions icm.gyro and icm.acceleration get you the readings from the IMU
        
        cv2.putText(frame, "IMU Adafruit ICM Module", (imuXloc, imuYloc), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, "Gyro readings:", (imuXloc, imuYloc + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "X: " + f"{gyroX:.2f},", (imuXloc, imuYloc + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "Y: " + f"{gyroY:.2f},", (imuXloc + 200, imuYloc + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "Z: " + f"{gyroZ:.2f} rad/s", (imuXloc + 370,imuYloc + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        
        cv2.putText(frame, "Accelerometer readings:", (imuXloc, imuYloc + 115), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "X: " + f"{accX:.2f},", (imuXloc, imuYloc + 145), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "Y: " + f"{accY:.2f},", (imuXloc + 200, imuYloc + 145), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        cv2.putText(frame, "Z: " + f"{accZ:.2f} m/s^s", (imuXloc + 370, imuYloc + 145), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        
        cv2.putText(frame, "TF02-Pro LIDAR:", (lidXloc, lidYloc), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, str(lidDist) + " meters", (lidXloc, lidYloc + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        #time.sleep(0.5)
        
        
        cv2.imshow("Sensor Readings", frame)
        k = cv2.waitKey(20)
        if k == ord("s"):
            # output last frame shown from webcam / was only used for testing purposes
            cv2.destroyAllWindows()
            break
