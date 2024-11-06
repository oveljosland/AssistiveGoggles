import time
import numpy as np
import subprocess
#from ultrasonic_sensor2 import UltrasonicSensor
import random

#left_sensor = UltrasonicSensor(trig_pin=0, echo_pin=0)
#right_sensor = UltrasonicSensor(trig_pin=0, echo_pin=0)

def main():
    #setup
    #left_sensor.setup(), right_sensor.setup()
    subprocess.run(["python", "self_calibrate.py"])

    try:
        while True:
            #headspace = np.mean([left_sensor.get_distance(), right_sensor.get_distance()])

            # test headspace measurements
            #headspace = np.array([random.randint(0, 100), random.randint(0, 100)])
            #avg_headspace = np.mean(headspace)
            #print(f"[{headspace[0]}, {headspace[1]}] -> {avg_headspace} cm")
            #time.sleep(0.5)
            
            
            subprocess.run(["python", "capture.py"])

    except KeyboardInterrupt:
        #left_sensor.cleanup()
        #right_sensor.cleanup()
        print("Exiting...")
    
    #finally:
        #left_sensor.cleanup()
        #right_sensor.cleanup()

if __name__ == "__main__":
    main()