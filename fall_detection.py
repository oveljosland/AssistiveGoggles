import time
import board
import busio
import adafruit_lsm303_accel

# Initialize I2C bus and accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

# Impact detection parameter
IMPACT_THRESHOLD = 25  # m/s^2, adjust based on testing

def detect_impact():
    # Read accelerometer data
    accel_x, accel_y, accel_z = accel.acceleration
    accel_magnitude = (accel_x**2 + accel_y**2 + accel_z**2)**0.5

    # Check if acceleration exceeds the impact threshold
    if accel_magnitude > IMPACT_THRESHOLD:
        print("Impact detected! Possible fall on the ground.")
        # Add any alert/response code here

while True:
    detect_impact()
    time.sleep(0.1)
