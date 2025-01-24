from camera import get_camera
from lock import get_lock
from server_api import get_server_api
from time import sleep
from logs import logger
import cv2


def main():
    frame = camera.get_frame()

    if frame is None:
        logger.debug("Get 'None' frame!")
        return
    
    success, encoded_image = cv2.imencode(".png", frame)
    if not success:
        raise ValueError("Failed to encode frame")
    
    is_identified = server_api.request_identify(encoded_image)
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
    server_api = get_server_api()

    while True:
        try:
            main()

        except Exception as e:
            logger.critical(str(e))
