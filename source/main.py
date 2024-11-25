from time import sleep

from entities import Camera, Lock
from requests import Response, post

from services import FaceRecognition
from settings import Settings, LockSettings, CameraSettings


settings = Settings()
lock_settings = LockSettings()
camera_settings = CameraSettings()


def main():
    camera = Camera()
    lock = Lock(lock_settings.PIN)
    face_recog = FaceRecognition()

    while True:
        sleep(settings.COOLDOWN)
        img: ... = camera.get_image()

        if img is None:
            continue

        opt_img = face_recog.optimize_img(img)
        is_contains_face = face_recog.contains_face(img)

        if not is_contains_face:
            continue

        if request_identify(opt_img):
            lock.unlock()
            sleep(settings.COOLDOWN)
            lock.lock()


def request_identify(img) -> bool:
    if settings.BACKEND_ENDPOINT_URI is None:
        return False

    request: Response = post(settings.BACKEND_ENDPOINT_URI, files=img)

    return request.status_code == 200


if __name__ == "__main__":
    main()
