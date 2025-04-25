import cv2
from cv2.typing import MatLike

from .exceptions import GetFrameError
from .settings import CameraSettings


class Camera:
    def __init__(self, settings: CameraSettings) -> None:
        self.__settings = settings

    def get_frame(self) -> MatLike | None:
        try:
            capture = self.__get_capture()
            is_success, frame = capture.read()
            capture.release()

        except (cv2.error, AttributeError) as e:
            raise GetFrameError("Error during frame capture!") from e

        if not is_success:
            frame = None

        return frame

    def __get_capture(self) -> cv2.VideoCapture:
        capture = cv2.VideoCapture(self.__settings.INDEX)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__settings.WIDTH)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__settings.HEIGHT)
        return capture


def get_camera():
    settings = CameraSettings()
    camera = Camera(settings)
    return camera
