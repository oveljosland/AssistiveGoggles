import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the first sensor
TRIG1 = 23         # GPIO 23 (Pin 16)
ECHO1 = 24         # GPIO 24 (Pin 18)

# Define the GPIO pins for the second sensor
TRIG2 = 27         # GPIO 27 (Pin 13)
ECHO2 = 22         # GPIO 22 (Pin 15)

# Define the motor pin
MOTOR_PIN = 18     # GPIO pin for the motor control

# Set up the pins as input and output
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def measure_distance(trig, echo):
    # Ensure the trigger pin is low
    GPIO.output(trig, False)
    time.sleep(0.1)  # Short delay to allow for separation between triggers

    # Send a 10us pulse to the trigger pin
    GPIO.output(trig, True)
    time.sleep(0.00001)  # 10us pulse
    GPIO.output(trig, False)

    # Wait for the echo pin to go high (start of the echo pulse)
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    # Wait for the echo pin to go low (end of the echo pulse)
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # Calculate the duration of the pulse
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance (sound speed in air is 34300 cm/s)
    distance = pulse_duration * 17150  # 17150 is half of 34300 (round trip time)

    # Limit the distance to two decimal places
    distance = round(distance, 2)

    return distance

def activate_motor(duration=3.5):
    """Activate the motor for a given duration in seconds."""
    GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Turn on the motor
    time.sleep(duration)               # Keep it on for the duration
    GPIO.output(MOTOR_PIN, GPIO.LOW)   # Turn off the motor

try:
    while True:
        # Measure distance from Sensor 1
        dist1 = measure_distance(TRIG1, ECHO1)
        print(f"Distance from Sensor 1: {dist1} cm")

        # Measure distance from Sensor 2
        dist2 = measure_distance(TRIG2, ECHO2)
        print(f"Distance from Sensor 2: {dist2} cm")

        # Check if either distance is less than 10 cm and activate motor
        if dist1 < 10 or dist2 < 10:
            print("DANGER!")
            activate_motor()  # Activate motor vibration

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()  # Clean up the GPIO pins on exit
