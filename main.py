import subprocess
from viewer import show
from self_calibrate import main as camera_calibrate

def main():
    try:
        camera_calibrate()
        while True:
            show()
            dnn_response = subprocess.run(["dnn/rs_dnn"], capture_output=True, text=True)
            print(dnn_response.stdout)
            print(dnn_response.stderr)
    except KeyboardInterrupt:
        print("Exiting...")
    
    finally:
        print("Cleaning up...")

if __name__ == "__main__":
    main()