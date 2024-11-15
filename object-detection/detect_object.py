import cv2 as cv
import time
import argparse
import numpy as np
import pyrealsense2 as rs

# kjøres ved: python detect_object.py -p caffe/MobileNetSSD_deploy.prototxt -m caffe/MobileNetSSD_deploy.caffemodel

# sett opp argumenter for scriptet
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="Path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="Path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.7, help="Minimum probability to filter weak detections")
args = vars(ap.parse_args())

# merkelapper for hva som kan detekteres av modellen
labels = ["background", "aeroplane", "bicycle", "bird", "boat",
          "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
          "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
          "sofa", "train", "tvmonitor"]

# unike farger for hvert unikt objekt
colors = np.random.uniform(0, 255, size=(len(labels), 3))

print("Laster inn modell...")
nn = cv.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("Starter videostrøm...")
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)
time.sleep(2)  # la kamera 'varme opp'

try:
    while True:
        # hent frames
        frames = pipeline.wait_for_frames()
        #frames = pipeline.wait_for_frames(timeout_ms=10000)
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        
        # konverterer frames til et numpy array
        frame = np.asanyarray(color_frame.get_data())

        # dimensjoner for frame
        (h, w) = frame.shape[:2]

        # beskjær frame til 400x400
        resized_frame = cv.resize(frame, (400, int(400 * h / w)))

        # konverterer frame til blob
        blob = cv.dnn.blobFromImage(cv.resize(resized_frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # gi blob til nettverket og få prediksjoner
        nn.setInput(blob)
        detections = nn.forward()

        # loop gjennom prediksjoner
        for i in range(0, detections.shape[2]):
            # sannsynlinghet for at prediksjon er riktig
            confidence = detections[0, 0, i, 2]

            # filtrere ut svake prediksjoner
            if confidence > args["confidence"]:
                # lagre indekser for hvert objekt
                idx = int(detections[0, 0, i, 1])

                # lage boks rund objekt
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # tegne boks og label
                label = "{}: {:.2f}%".format(labels[idx], confidence * 100)
                cv.rectangle(frame, (startX, startY), (endX, endY), colors[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv.putText(frame, label, (startX, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)

        cv.imshow("Frame", frame)

        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    print("Avslutter...")
    cv.destroyAllWindows()
    pipeline.stop()
