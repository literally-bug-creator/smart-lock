from camera import get_camera, camera_exceptions
from lock import get_lock, lock_exceptions
from frame_processor import get_frame_processor, frame_processor_exceptions


if __name__ == "__main__":
    camera = get_camera()
    lock = get_lock()
    frame_processor = get_frame_processor()

    while True:
        ...  # TODO: Implement logic
