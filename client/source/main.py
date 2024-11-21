from os import getenv
from time import sleep

from entities import Camera, Lock
from requests import Response, post
from services import FaceRecognition

ENDPOINT_URI = getenv("BACKEND_ENDPOINT_URI")
COOLDOWN = int(getenv("COOLDOWN", 5))


def main():
    camera = Camera()
    lock = Lock()
    face_recog = FaceRecognition()

    while True:
        sleep(COOLDOWN)
        img: ... = camera.get_image()

        if img is None:
            continue

        opt_img = face_recog.optimize(img)
        is_contains_face = face_recog.contains_face(img)

        if not is_contains_face:
            continue

        if request_identify(opt_img):
            lock.unlock()
            sleep(COOLDOWN)
            lock.lock()


def request_identify(img) -> bool:
    if ENDPOINT_URI is None:
        return False

    request: Response = post(ENDPOINT_URI, files=img)

    return request.status_code == 200


if __name__ == "__main__":
    main()
