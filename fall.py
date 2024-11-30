import time
import board
import busio
import adafruit_lsm303_accel
import sendmail
import gypsy

# Initialize I2C bus and accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
accel_max = 0
# Impact detection parameter
IMPACT_THRESHOLD = 19  # m/s^2, adjust based on testing
MESSAGE_MAX_RATE = 10  # seconds, adjust based on testing
sendt = False
time_since_last_impact = time.time()

def detect_impact():
    global accel_max
    global sendt
    global time_since_last_impact
    # Read accelerometer data
    accel_x, accel_y, accel_z = accel.acceleration
    accel_magnitude = (accel_x**2 + accel_y**2 + accel_z**2)**0.5
    # Check if acceleration exceeds the impact threshold
    if accel_magnitude > IMPACT_THRESHOLD:
        accel_max = max(accel_magnitude, accel_max)
        print("Impact detected! Possible fall on the ground.", accel_magnitude)
        if not sendt or time.time() - time_since_last_impact > MESSAGE_MAX_RATE:
            breddegrader, lengdegrader = gypsy.getlocation()
            sendmail.send('Det har blitt opfattet ett fall på  ' + str(accel_max) + 'm/s^2 Posisjon: Breddegrader ' + breddegrader + 'Lengdegrader ' + lengdegrader)
            sendt = True
            time_since_last_impact = time.time()
