from multiprocessing import Process

import pyrealsense2
import numpy as np #gjør bilde til narray
import cv2 #bildbehandling + vise bilder
from google.cloud import vision #google vision api
import pyttsx3 #snakking

import realsense_camera


class TextToSpeech(Process):
    def __init__(self, camera: realsense_camera.PyRealSenseCamera, rate: int = 150, volume: float = 0.9):
        # Initialize the pyttsx3 engine
        super().__init__()
        self.camera: realsense_camera.PyRealSenseCamera = camera

        self.engine = pyttsx3.init()

        # Set the rate of speech
        self.engine.setProperty('rate', rate)

        # Set the volume
        self.engine.setProperty('volume', volume)

        self.texts = []

    def run(self):
        while True:
            # listen for key press
            key = cv2.waitKey(0)
            if key == ord('r'):
                self.get_text(self.camera.get_color_image())
                self.speak()

    def get_text(self, frame: pyrealsense2.video_frame):
        """Gets the text from the frame using the Google Vision API."""
        client = vision.ImageAnnotatorClient()

        # Convert the frame to a byte array
        _, encoded_image = cv2.imencode('.jpg', np.asanyarray(frame.get_data()))
        content = encoded_image.tobytes()

        # Create an Image object
        image = vision.Image(content=content)

        # Perform text detection
        response = client.text_detection(image=image)

        # Check for errors in the response
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        self.texts = response.text_annotations[1:]  # Skipping the first result as it's the full text

    def speak(self, texts = None):
        """Reads the texts out loud, defaulting to the stored texts if none are provided."""
        print("Texts:")
        texts = texts if texts else self.texts

        # If the input is not a list of texts
        if isinstance(texts, str):
            print(f'\t"{texts}"')
            self.engine.say(texts)
            self.engine.runAndWait()
            return

        # read out loud
        for text in texts:
            if isinstance(text, vision.TextAnnotation):
                print(f'\t"{text.description}"')
            else:
                print(f'\t"{text}"')

            self.engine.say(text)
            self.engine.runAndWait()


def run(camera: realsense_camera.PyRealSenseCamera):
    tts = TextToSpeech(camera)
    tts.start()


def main():
    camera = realsense_camera.PyRealSenseCamera()
    run(camera)


if __name__ == "__main__":
    main()
