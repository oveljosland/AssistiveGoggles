import RPi.GPIO as GPIO
import time

# Measuring distance with the HC-SR04 Ultrasonic Sensor

#trig_pin = 6  # Pin to send the ping from
#echo_pin = 5  # Pin to read the ping from
#led_pin = 18  # Pin for LED (adjust as per your board setup)
#measurement_interval = 0.06  # Datasheet recommends waiting at least 60ms between measurements
#previous_time = 0
#previous_micros = 0
#led_state = False  # Initialise LED to off
#distance = 0

GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def uss_setup():
    trig_pin = 6
    echo_pin = 5
    measurement_interval = 0.06
    previous_time = 0
    previous_micros = 0
    distance = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    

def uss_get_distance():
    global previous_time, led_state, distance
    current_time = time.time()

    if current_time - previous_time >= measurement_interval:
        previous_time = current_time

        # Toggle LED state
        led_state = not led_state
        GPIO.output(led_pin, led_state)

        trigger_pulse()

        # Read the duration of the response pulse
        duration = pulse_duration()

        # Convert time into distance in cm
        distance = duration / 58.0

        # Print the distance
        print(f"Distance: {distance:.2f} cm")


def trigger_pulse():
    global previous_micros
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(0.000002)  # Wait for 2 microseconds
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # Wait for 10 microseconds
    GPIO.output(trig_pin, GPIO.LOW)

def pulse_duration():
    start_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    return (stop_time - start_time) * 1000000  # Convert to microseconds

def setup():
    print("Starting setup...")
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(2)  # Allow sensor to settle

def loop():
    try:
        while True:
            uss_get_distance()
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()  # Reset GPIO settings on exit

if __name__ == '__main__':
    setup()
    loop()
