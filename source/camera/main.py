import cv2
from cv2.typing import MatLike

from .exceptions import ConnectionError, GetFrameError
from .settings import CameraSettings


class Camera:
    def __init__(self, settings: CameraSettings) -> None:
        self.__settings = settings

        try:
            self.__capture = cv2.VideoCapture(self.__settings.INDEX)
            if not self.__capture.isOpened():
                raise ConnectionError(
                    f"Cannot open camera with index {self.__settings.INDEX}"
                )
            self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__settings.WIDTH)
            self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__settings.HEIGHT)
            self.__capture.set

        except cv2.error as e:
            raise ConnectionError("OpenCV error: failed to initialize camera") from e

    def get_frame(self) -> MatLike | None:
        try:
            is_success, frame = self.__capture.read()

        except (cv2.error, AttributeError) as e:
            raise GetFrameError("Error during frame capture!") from e

        if not is_success:
            frame = None

        return frame

    def get_index(self):
        return self.__settings.INDEX


def get_camera():
    settings = CameraSettings()
    camera = Camera(settings)
    return camera
