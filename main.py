import subprocess

import capture
import realsense_camera
import texttospeech

def main():
    camera = realsense_camera.PyRealSenseCamera()
    # self_calibrate.main()

    try:
        print("Starting text-to-speech...")
        print("Press r to read the text aloud")
        texttospeech.run(camera)

        print("Starting capture...")
        capture.display_color_and_depth_images(camera)

        while True:
            dnn_response = subprocess.run(["dnn/rs_dnn"], capture_output=True, text=True)
            print(dnn_response.stdout)
            print(dnn_response.stderr)

    except KeyboardInterrupt:
        print("Exiting...")
    
    finally:
        pass

if __name__ == "__main__":
    main()