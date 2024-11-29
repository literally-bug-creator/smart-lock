from camera import get_camera, camera_exceptions
from frame_processor import get_frame_processor, frame_processor_exceptions


if __name__ == "__main__":
    camera = get_camera()
    frame_processor = get_frame_processor()
