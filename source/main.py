from time import sleep
import RPi.GPIO as GPIO

from requests import Response, post

from settings import CommonSettings

from services import CameraService, FaceRecognizerService, LockService
from services import CameraSettings, FaceRecognizerSettings, LockSettings
from services import camera_exceptions, face_recognizer_exceptions, lock_exceptions


settings = CommonSettings()

camera = CameraService(CameraSettings())
lock = LockService(LockSettings())
face_recognizer = FaceRecognizerService(FaceRecognizerSettings())


def main(
    camera: CameraService, lock: LockService, face_recognizer: FaceRecognizerService
):
    camera.connect()
    lock.connect()
    face_recognizer.connect()

    frame = camera.get_frame()

    is_contains_face = face_recognizer.contains_face(frame)

    if not is_contains_face:
        return

    image_path = camera.convert_frame_to_png(settings.IMAGE_PATH, frame)

    if request_identify(image_path):
        lock.unlock()
        sleep(settings.COOLDOWN)
        lock.lock()


def request_identify(path_to_img: str, url: str) -> bool:
    try:
        with open(path_to_img, "rb") as image:
            request: Response = post(
                url, files={"file": ("image.png", image, "image/png")}
            )

    except ... as e:
        # TODO: Add log of exception
        return False

    return request.status_code == 200


def reset_rasberry_state():
    GPIO.setup(GPIO.BOARD)
    GPIO.cleanup()


if __name__ == "__main__":
    camera = CameraService(CameraSettings())
    face_recognizer = FaceRecognizerService(FaceRecognizerSettings())
    lock = LockService(LockSettings())

    while True:
        try:
            main(camera, face_recognizer, lock)

        except (
            camera_exceptions.ConnectionError,
            face_recognizer_exceptions.ConnectionError,
            lock_exceptions.ConnectionError,
        ) as connection_exception:
            ...  # TODO: Log exception

        except ... as runtime_error:
            ...  # TODO: Log exception

        reset_rasberry_state()
        sleep(settings.COOLDOWN)
