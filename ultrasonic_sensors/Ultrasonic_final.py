import RPi.GPIO as GPIO
import time

#Setter opp GPIO mode
GPIO.setmode(GPIO.BCM)

#Definerer GPIO pins for Sensor 1
TRIG_1 = 23 # GPIO 23 (Pin 16)
ECHO_1 = 24 # GPIO 24 (Pin 18)
MOTOR_PIN_1 = 18 # GPIO pin for å kontrollere motoren til sensor 1

#Definerer GPIO pins for Sensor 2
TRIG_2 = 27 #GPIO 27 (Pin 13)
ECHO_2 = 22 #GPIO 22 (Pin 15)
MOTOR_PIN_2 = 12 #GPIO pin for å kontrollere motoren til sensor 2

#Setter opp pinsa som input og output
GPIO.setup(TRIG_1, GPIO.OUT)
GPIO.setup(ECHO_1, GPIO.IN)
GPIO.setup(MOTOR_PIN_1, GPIO.OUT)

GPIO.setup(TRIG_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)
GPIO.setup(MOTOR_PIN_2, GPIO.OUT)

#Konstanter for vibrasjons-hyppighet-kontrollen
MAX_DISTANCE = 25 # Maksimum avstand for å starte å vibrere i cm
MAX_DELAY = 1000 # Maksimum delay i ms (ved størst avstand)
MIN_DELAY = 100 # Minimum delay i ms (Når faren er veldig nærme)

def measure_distance(TRIG, ECHO): 
    """Måler avstanden ved bruk av ultrasonisk sensor."""
    GPIO.output(TRIG, False)
    time.sleep(0.05) # Liten delay som lar sensoren til å forberede seg til neste måling

    # Sender en 10 mikrosekund puls til trigger pinnen
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Måler varigheten til echo pulsen
    while GPIO.input(ECHO) == 0: 
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # Konverterer tid til distanse - Formel = distance = (pulse_duration * lydens hastighet i luft) / 2 - Her jobber vi med cm/s
    return round(distance, 2)

def get_vibration_delay(distance):
    """Kalkulerer vibrasjons delay"""
    if distance > MAX_DISTANCE:
        return MAX_DELAY
    else: 
        scale = (MAX_DISTANCE - distance) / MAX_DISTANCE
        delay = MAX_DELAY - (scale * (MAX_DELAY - MIN_DELAY))
        return max(MIN_DELAY, delay)

def activate_motor(motor_pin, duration=0.1):
    """Aktiverer motoren i en kort puls varighet"""
    GPIO.output(motor_pin, GPIO.HIGH) # Skrur på motoren
    time.sleep(duration) # Holder den på for den gitte varigheten
    GPIO.output(motor_pin, GPIO.LOW) # Skrur av motoren

def monitor_sensors():
    # Måler avstanden for Sensor 1
    dist_1 = measure_distance(TRIG_1, ECHO_1)
    print(f"Sensor 1 Distance: {dist_1} cm")
    #Sjekker og aktiverer motor for sensor 1 hvis den er innenfor rangen
    if dist_1 <= MAX_DISTANCE:
        delay_1 = get_vibration_delay(dist_1)
        print(f"Sensor 1 Vibration Delay: {delay_1} ms")
        activate_motor(MOTOR_PIN_1, duation=0.1)
        time.sleep(delay_1 / 1000) # Venter på den kalkulerte delayen
    #Måler avstanden for Sensor 2
    dist_2 = measure_distance(TRIG_2, ECHO_2)
    print(f"Sensor 2 Distance: {dist_2} cm")
    #Sjekker og aktiverer motor for sensor 2 hvis den er innenfor rangen
    if dist_2 <= MAX_DISTANCE:
        delay_2 = get_vibration_delay(dist_2)
        print(f"Sensor 2 Vibration Delay {delay_2} ms")
        activate_motor(MOTOR_PIN_2, duration=0.1)
        time.sleep(delay_2 / 1000) # Venter på den kalkulerte delayen
    
