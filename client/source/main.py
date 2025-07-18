from camera import get_camera, camera_exceptions
from lock import get_lock, lock_exceptions
from frame_processor import get_frame_processor, frame_processor_exceptions
from server_api import get_server_api, server_api_exceptions
from time import sleep
from logs import logger


def main():
    frame = camera.get_frame()

    if frame is None:
        logger.debug("Get 'None' frame!")
        return

    if not frame_processor.contains_face(frame):
        logger.debug("Frame does not contain faces!")
        return

    frame_path = frame_processor.save_frame(frame)
    is_identified = server_api.request_identify(frame_path)

    if not is_identified:
        logger.debug("Face is unidentified!")
        return

    logger.debug("Face is successfully identified!")

    lock.unlock()
    logger.debug("Lock is opened!")
    sleep(3)
    lock.lock()
    logger.debug("Lock is closed!")


if __name__ == "__main__":
    camera = get_camera()
    lock = get_lock()
    frame_processor = get_frame_processor()
    server_api = get_server_api()

    while True:
        try:
            main()

        except Exception as e:
            if not issubclass(
                type(e),
                (
                    server_api_exceptions.ServerAPIError,
                    camera_exceptions.CameraException,
                    lock_exceptions.LockException,
                    frame_processor_exceptions.FrameProcessorError,
                ),
            ):
                logger.critical(str(e))
                raise e

            logger.warning(str(e))
