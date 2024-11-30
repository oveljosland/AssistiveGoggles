import subprocess

import realsense_camera
import texttospeech
import gypsy
import fall
import ultrasonic_sensors.Ultrasonic_final as ultrasonicSensors


def main():
    try:
        camera = realsense_camera.PyRealSenseCamera()

        texttospeech.run(camera) # Start the continuous text-to-speech thread

        while True:
            gypsy.sjekkknapp()
            fall.detect_impact()

            ultrasonicSensors.monitor_sensors()

            
    except KeyboardInterrupt:
        print("Exiting...")
    
    finally:
        print("Cleaning up...")

if __name__ == "__main__":
    main()