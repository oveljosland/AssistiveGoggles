import serial
import time
import RPi.GPIO as GPIO
import socket
import sendmail

# Set up the serial connection
serial_port = "/dev/serial0"  # The serial port for Raspberry Pi
baud_rate = 9600  # The GPS breakout communicates at 9600 baud
ser = serial.Serial(serial_port, baud_rate, timeout=1)
sendt = False

# Set up the GPIO for the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Use internal pull-up resistor

def getlocation():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
    
        if line.startswith("$GPRMC"):
            fields = line.split(',')
            breddegrader = fields[3]
            lengdegrader = fields[5]
            print(f"Breddegrader: {breddegrader}, Lengdegrader: {lengdegrader}")
            return breddegrader, lengdegrader
def sjekkknapp():
    global sendt
    # Sjekker om knappen har blitt trukket
    if GPIO.input(button_pin) == GPIO.LOW:
        if not sendt:
            breddegrader, lengdegrader = getlocation()
            sendmail.send(f"Posisjon: Breddegrader {breddegrader}, Lengdegrader {lengdegrader}")
            sendt = True
          


