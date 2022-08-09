# Group 9 Capstone
# Adafruit IMU module reading the gyro and accelerometer

import time
import busio
import adafruit_icm20x
import board

i2c = board.I2C()
icm = adafruit_icm20x.ICM20649(i2c)
                               
while(1):
    print("=" * 40)
    print("Gyro readings: X:%.2f, Y: %.2f, Z: %.2f rad/s" % (icm.gyro))
    print("Acceleromter readings: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
    
    # the functions icm.gyro and icm.acceleration get you the readings from the IMU
    
    time.sleep(0.5)
