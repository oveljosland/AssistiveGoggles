import RPi.GPIO as GPIO
import time
import random

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.measurement_interval = 0.06  # 60 ms
        self.previous_time = 0
        self.distance = 0

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        current_time = time.time()

        if current_time - self.previous_time >= self.measurement_interval:
            self.previous_time = current_time

            # Trigger the sensor pulse
            self.trigger_pulse()

            # Read the duration of the response pulse
            duration = self.pulse_duration()

            # Convert time into distance in cm
            self.distance = duration * 17150  # Speed of sound: 343 m/s, hence 17150 cm/s for round trip

            return self.distance
        else:
            # No new measurement; return the last distance
            return self.distance

    def trigger_pulse(self):
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.000002)  # Wait for 2 microseconds
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)  # Wait for 10 microseconds
        GPIO.output(self.trig_pin, GPIO.LOW)

    def pulse_duration(self):
        # Wait for the echo to go high (start of pulse)
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        # Wait for the echo to go low (end of pulse)
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        return stop_time - start_time

    def cleanup(self):
        GPIO.cleanup([self.trig_pin, self.echo_pin])

