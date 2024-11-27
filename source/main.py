from time import sleep
import RPi.GPIO as GPIO

from requests import Response, post

from settings import CommonSettings
from logs import logger

from services import CameraService, FaceRecognizerService, LockService
from services import CameraSettings, FaceRecognizerSettings, LockSettings
from services import camera_exceptions, face_recognizer_exceptions, lock_exceptions


settings = CommonSettings()

camera = CameraService(CameraSettings())
lock = LockService(LockSettings())
face_recognizer = FaceRecognizerService(FaceRecognizerSettings())


def main(
    camera: CameraService,
    lock: LockService,
    face_recognizer: FaceRecognizerService,
):
    camera.connect()
    lock.connect()
    face_recognizer.connect()

    frame = camera.get_frame()
    is_contains_face = face_recognizer.contains_face(frame)

    if not is_contains_face:
        return

    image_path = camera.convert_frame_to_png(frame)

    if request_identify(image_path, settings.BACKEND_ENDPOINT_URI):
        lock.unlock()
        sleep(settings.COOLDOWN)
        lock.lock()


def request_identify(path_to_img: str, url: str) -> bool:
    try:
        with open(path_to_img, "rb") as image:
            request: Response = post(
                url, files={"file": ("image.png", image, "image/png")}
            )

    except Exception as e:
        logger.error(str(e))
        return False

    return request.status_code == 200


def reset_rasberry_state():
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()


if __name__ == "__main__":
    camera = CameraService(CameraSettings())
    face_recognizer = FaceRecognizerService(FaceRecognizerSettings())
    lock = LockService(LockSettings())

    while True:
        try:
            main(camera, lock, face_recognizer)

        except (
            camera_exceptions.ConnectionError,
            face_recognizer_exceptions.ConnectionError,
            lock_exceptions.ConnectionError,
        ) as connection_exception:
            logger.critical(str(connection_exception))

        except (
            camera_exceptions.FrameConversionError,
            camera_exceptions.FrameError,
            face_recognizer_exceptions.RecognizeError,
            lock_exceptions.PinSetupError,
        ) as runtime_error:
            logger.critical(str(runtime_error))

        reset_rasberry_state()
        sleep(settings.COOLDOWN)
