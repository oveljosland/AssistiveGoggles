import cv2 as cv
import time
import argparse
import numpy as np
import pyrealsense2 as rs

framerate = 30

# Argument setup
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="Path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="Path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.7, help="Minimum probability to filter weak detections")
args = vars(ap.parse_args())

# Object labels and random colors
labels = ["background", "aeroplane", "bicycle", "bird", "boat",
          "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
          "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
          "sofa", "train", "tvmonitor"]
colors = np.random.uniform(0, 255, size=(len(labels), 3))

print("Loading model...")
nn = cv.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("Starting video stream...")
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, framerate)  # Enable color stream
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, framerate)  # Enable depth stream
pipeline.start(config)
time.sleep(2)  # Let the camera warm up

def determine_position(centerX, frame_width):
    """Determine the position of the object based on its X-coordinate."""
    segment_width = frame_width // 5
    positions = {
        0: "far left",
        1: "left",
        2: "center",
        3: "right",
        4: "far right"
    }
    segment = centerX // segment_width
    return positions.get(min(segment, 4))  # Cap to the last position if out of bounds

try:
    while True:
        # Get frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()  # Get depth frame
        if not color_frame or not depth_frame:
            continue

        # Convert frames to numpy arrays
        frame = np.asanyarray(color_frame.get_data())
        depth = np.asanyarray(depth_frame.get_data())

        # Dimensions for frame
        (h, w) = frame.shape[:2]

        # Convert frame to blob
        blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # Get predictions
        nn.setInput(blob)
        detections = nn.forward()

        # Process detections efficiently
        valid_detections = [
            i for i in range(0, detections.shape[2])
            if detections[0, 0, i, 2] > args["confidence"]
        ]

        for i in valid_detections:
            # Extract object information
            confidence = detections[0, 0, i, 2]
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Calculate center of the bounding box
            centerX = (startX + endX) // 2
            centerY = (startY + endY) // 2

            # Retrieve depth at the center
            depth_distance = depth_frame.get_distance(centerX, centerY)

            # Determine position
            position = determine_position(centerX, w)

            # Create label
            label = f"{labels[idx]}: {depth_distance:.2f} meters away on the {position}"

            # Draw bounding box and label
            cv.rectangle(frame, (startX, startY), (endX, endY), colors[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv.putText(frame, label, (startX, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)

            # Print details
            print(label)

        # Show frame
        cv.imshow("Frame", frame)

        # Exit on 'q' key
        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break

finally:
    print("Exiting...")
    cv.destroyAllWindows()
    pipeline.stop()
