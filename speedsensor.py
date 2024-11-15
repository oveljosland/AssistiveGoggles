import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins
TRIG = 23          # GPIO 23 (Pin 16)
ECHO = 24          # GPIO 24 (Pin 18)
MOTOR_PIN = 18     # GPIO pin for the motor control (choose an available pin)

# Set up the pins as input and output
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Constants for vibration delay control
MAX_DISTANCE = 25  # Maximum distance to start vibrating in cm
MAX_DELAY = 1000   # Maximum delay in ms (when at max distance)
MIN_DELAY = 100    # Minimum delay in ms (when very close)

def measure_distance():
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
    # Map the distance to a delay between MAX_DELAY and MIN_DELAY
    if distance > MAX_DISTANCE:
        return MAX_DELAY
    else:
        # Invert the mapping so closer distances give shorter delays
        scale = (MAX_DISTANCE - distance) / MAX_DISTANCE
        delay = MAX_DELAY - (scale * (MAX_DELAY - MIN_DELAY))
        return max(MIN_DELAY, delay)

def activate_motor(duration=0.1):
    """Activate the motor for a short pulse duration."""
    GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Turn on the motor
    time.sleep(duration)               # Keep it on for the duration
    GPIO.output(MOTOR_PIN, GPIO.LOW)   # Turn off the motor

try:
    while True:
        dist = measure_distance()
        print(f"Distance: {dist} cm")

        if dist <= MAX_DISTANCE:
            # Calculate delay based on distance
            delay = get_vibration_delay(dist)
            print(f"Vibration Delay: {delay} ms")
            
            activate_motor(duration=0.1)  # Short motor pulse
            time.sleep(delay / 1000)      # Wait for calculated delay

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()  # Clean up the GPIO pins on exit
