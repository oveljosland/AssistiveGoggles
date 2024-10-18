import subprocess


def main():
    subprocess.run(["python", "self_calibrate.py"])
    subprocess.run(["python", "capture.py"])

if __name__ == "__main__":
    main()