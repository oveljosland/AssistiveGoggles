import pyrealsense2 as rs
import numpy as np
import cv2
import open3d as o3d


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        # Create Open3D image
        depth_o3d = o3d.geometry.Image(depth_image)

        # Create point cloud from depth image
        intrinsic = o3d.camera.PinholeCameraIntrinsic(640, 480, 385, 385, 320, 240)
        pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_o3d, intrinsic)

        # Segment plane
        plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)

        # Extract ground plane
        ground_plane = pcd.select_by_index(inliers)

        downsampled_pcd = pcd.voxel_down_sample(voxel_size=0.05)

        cleaned_pcd, _ = downsampled_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

        # Visualize the ground plane
        ground_plane.paint_uniform_color([1.0, 0, 0])  # Red color for ground plane
        o3d.visualization.draw_geometries([pcd, ground_plane])
        o3d.visualization.Visualizer().run()


finally:

    # Stop streaming
    pipeline.stop()