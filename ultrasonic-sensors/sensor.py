import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for Sensor 1
TRIG_1 = 23         # GPIO 23 (Pin 16)
ECHO_1 = 24         # GPIO 24 (Pin 18)
MOTOR_PIN_1 = 18    # GPIO pin for the motor control of Sensor 1

# Define GPIO pins for Sensor 2
TRIG_2 = 27         # GPIO 27 (Pin 13)
ECHO_2 = 22         # GPIO 22 (Pin 15)
MOTOR_PIN_2 = 25    # GPIO pin for the motor control of Sensor 2

# Set up the pins as input and output
GPIO.setup(TRIG_1, GPIO.OUT)
GPIO.setup(ECHO_1, GPIO.IN)
GPIO.setup(MOTOR_PIN_1, GPIO.OUT)

GPIO.setup(TRIG_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)
GPIO.setup(MOTOR_PIN_2, GPIO.OUT)

# Constants for vibration delay control
MAX_DISTANCE = 25  # Maximum distance to start vibrating in cm
MAX_DELAY = 1000   # Maximum delay in ms (when at max distance)
MIN_DELAY = 100    # Minimum delay in ms (when very close)

def measure_distance(TRIG, ECHO):
    """Measure distance using the ultrasonic sensor."""
    GPIO.output(TRIG, False)
    time.sleep(0.05)  # Allow the sensor to settle

    # Send a 10us pulse to the trigger pin
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Measure the duration of the echo pulse
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Convert time to distance
    return round(distance, 2)

def get_vibration_delay(distance):
    """Calculate the vibration delay inversely proportional to distance."""
    if distance > MAX_DISTANCE:
        return MAX_DELAY
    else:
        scale = (MAX_DISTANCE - distance) / MAX_DISTANCE
        delay = MAX_DELAY - (scale * (MAX_DELAY - MIN_DELAY))
        return max(MIN_DELAY, delay)

def activate_motor(motor_pin, duration=0.1):
    """Activate the motor for a short pulse duration."""
    GPIO.output(motor_pin, GPIO.HIGH)  # Turn on the motor
    time.sleep(duration)               # Keep it on for the duration
    GPIO.output(motor_pin, GPIO.LOW)   # Turn off the motor

try:
    while True:
        # Measure distance for Sensor 1
        dist_1 = measure_distance(TRIG_1, ECHO_1)
        print(f"Sensor 1 Distance: {dist_1} cm")

        # Check and activate motor for Sensor 1 if within range
        if dist_1 <= MAX_DISTANCE:
            delay_1 = get_vibration_delay(dist_1)
            print(f"Sensor 1 Vibration Delay: {delay_1} ms")
            activate_motor(MOTOR_PIN_1, duration=0.1)
            time.sleep(delay_1 / 1000)  # Wait for calculated delay

        # Measure distance for Sensor 2
        dist_2 = measure_distance(TRIG_2, ECHO_2)
        print(f"Sensor 2 Distance: {dist_2} cm")

        # Check and activate motor for Sensor 2 if within range
        if dist_2 <= MAX_DISTANCE:
            delay_2 = get_vibration_delay(dist_2)
            print(f"Sensor 2 Vibration Delay: {delay_2} ms")
            activate_motor(MOTOR_PIN_2, duration=0.1)
            time.sleep(delay_2 / 1000)  # Wait for calculated delay

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()  # Clean up the GPIO pins on exit
