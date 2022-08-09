# Group 9 Capstone
# Adafruit GPS module reading longitude and latitued values

# Based off of sample code from Adafruit 


import time
import board
import busio

import adafruit_gps

# I2C interface to read the pins
# this part was previously a board.i2c function
i2c = busio.I2C(board.SCL, board.SDA)

# Create a GPS module instance.
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface


# Turn on the basic GGA and RMC info (what you typically want), refer to NMEA for
# more information
# sends command to GPS to read 
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# update polling data from GPS by 1 per second (1Hz) - get info every second
# in milliseconds
gps.send_command(b"PMTK220,1000")

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out location: longitude and latitude
        print("=" * 40)  # Print a separator line.
        
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        
        # BASICALLY, to get gps.latitude and gps.longitude to get coordinates
