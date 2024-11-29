from camera import get_camera, camera_exceptions
from lock import get_lock, lock_exceptions
from frame_processor import get_frame_processor, frame_processor_exceptions
from server_api import get_server_api, server_api_exceptions
from source.tests.request import request
from logs import logger


def main():
    frame = camera.get_frame()
    if not frame_processor.contains_face(frame):
        continue

    frame_path = frame_processor.save_frame(frame)
    is_identified = server_api.request_identify(frame_path)

    if not is_identified:
        continue

    lock.unlock()
    sleep(5)
    lock.lock()


if __name__ == "__main__":
    camera = get_camera()
    lock = get_lock()
    frame_processor = get_frame_processor()
    server_api = get_server_api()

    while True:
        try:
            main()

        except Exception as e:
            if not issubclass(e, server_api_exceptions.ServerAPIError, camera_exceptions.CameraException,
                              lock_exceptions.LockException, frame_processor_exceptions.FrameProcessorError):
                logger.critical(str(e))
                raise e

            logger.warning(str(e))






