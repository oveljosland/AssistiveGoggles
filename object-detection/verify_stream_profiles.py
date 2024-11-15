import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
try:
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)

    print("Supported Stream Modes:")
    for s in pipeline_profile.get_streams():
        print("Stream: {}, Format: {}, Resolution: {}x{}, FPS: {}".format(
            s.stream_type(), s.format(), s.as_video_stream_profile().width(),
            s.as_video_stream_profile().height(), s.fps()))
except Exception as e:
    print("Error: ", e)
finally:
    pipeline.stop()
