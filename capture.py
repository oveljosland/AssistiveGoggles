import numpy as np
import cv2
import threading
import realsense_camera


def display_color_and_depth_image(camera: realsense_camera.PyRealSenseCamera):
    """Displays the color and depth images from the camera."""
    camera.wait_for_next_frame()

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(np.asanyarray(camera.depth_image.get_data()), alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = camera.color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(camera.color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((camera.color_image, depth_colormap))

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    cv2.waitKey(1)


def display_color_and_depth_image_continuous(camera: realsense_camera.PyRealSenseCamera):
    """Displays the color and depth images from the camera continuously."""
    def run_continuous(rs_camera: realsense_camera.PyRealSenseCamera):
        while True:
            display_color_and_depth_image(rs_camera)

    display_thread = threading.Thread(target=run_continuous, args=(camera,))
    display_thread.start()


if __name__ == "__main__":
    real_sense_camera = realsense_camera.PyRealSenseCamera()
    display_color_and_depth_image_continuous(real_sense_camera)