import pyrealsense2


class PyRealSenseCamera:
    """Wrapper for the Intel RealSense camera."""
    def __init__(self):
        self.frame: pyrealsense2.composite_frame | None = None
        self.color_image: pyrealsense2.depth_frame | None = None
        self.depth_image: pyrealsense2.video_frame | None = None

        self.pipeline = pyrealsense2.pipeline()
        self.config = pyrealsense2.config()

        self.pipeline_wrapper = pyrealsense2.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(self.device.get_info(pyrealsense2.camera_info.product_line))

        if not any(sensor.get_info(pyrealsense2.camera_info.name) == 'RGB Camera' for sensor in self.device.sensors):
            print("The program requires depth camera with color sensor")
            exit(1)

        self.config.enable_stream(pyrealsense2.stream.depth, 640, 480, pyrealsense2.format.z16, 30)
        self.config.enable_stream(pyrealsense2.stream.color, 640, 480, pyrealsense2.format.bgr8, 30)

        self.pipeline.start(self.config)

    def __del__(self):
        self.pipeline.stop()

    def wait_for_next_frame(self):
        """Waits for the next frame from the camera."""
        self.frame: pyrealsense2.composite_frame = self.pipeline.wait_for_frames()
        self.color_image = self.frame.get_color_frame()
        self.depth_image = self.frame.get_depth_frame()

    def try_get_next_frame(self):
        """Gets the next frame from the camera if it is available."""
        frame: pyrealsense2.composite_frame = self.pipeline.poll_for_frames()

        if frame:
            self.frame = frame
            self.depth_image = frame.get_depth_frame()
            self.color_image = frame.get_color_frame()

    def get_frame(self) -> pyrealsense2.composite_frame:
        """Gets the most recent combined frame from the camera."""
        self.try_get_next_frame()

        return self.frame

    def get_color_image(self) -> pyrealsense2.depth_frame:
        """Gets the most recent color image from the camera."""
        self.try_get_next_frame()

        return self.color_image

    def get_depth_image(self) -> pyrealsense2.video_frame:
        """Gets the most recent depth image from the camera."""
        self.try_get_next_frame()

        return self.depth_image
