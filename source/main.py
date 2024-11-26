from time import sleep

from entities import Camera, Lock
from requests import Response, post

from services import FaceRecognition
from settings import (
    CommonSettings,
    LockSettings,
    CameraSettings,
    FaceRecognizerSettings,
)


common_settings = CommonSettings()
lock_settings = LockSettings()
camera_settings = CameraSettings()
face_recognizer_settings = FaceRecognizerSettings()


def main():
    camera = Camera(camera_settings.CAMERA_INDEX, camera_settings.IMG_HEIGHT, camera_settings.IMG_WIDTH)
    lock = Lock(lock_settings.PIN)
    face_recog = FaceRecognition(face_recognizer_settings.CLASSIFIER, face_recognizer_settings.SCALE_FACTOR, face_recognizer_settings.MIN_NEIGHBORS, face_recognizer_settings.MIN_SIZE_X, face_recognizer_settings.MIN_SIZE_Y)

    while True:
        sleep(common_settings.COOLDOWN)
        img = camera.get_frame()

        if img is None:
            continue

        is_contains_face = face_recog.contains_face(img)

        if not is_contains_face:
            continue

        if request_identify(img):
            lock.unlock()
            sleep(common_settings.COOLDOWN)
            lock.lock()


def request_identify(img) -> bool:
    if common_settings.BACKEND_ENDPOINT_URI is None:
        return False

    request: Response = post(common_settings.BACKEND_ENDPOINT_URI, files=img)

    return request.status_code == 200


if __name__ == "__main__":
    main()
