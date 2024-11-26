import cv2
from .settings import CameraSettings
from .exceptions import ConnectionError, FrameError, FrameConversionError


class CameraService:
    def __init__(self, settings: CameraSettings = None):
        self.__settings = settings

    def connect(self):
        try:
            self.__capture = cv2.VideoCapture(self.__settings.INDEX)
            self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__settings.WIDTH)
            self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__settings.HEIGHT)

        except ... as connect_exception:  # TODO: List all possible exceptions
            raise ConnectionError("Can't connect to a camera!") from connect_exception

    def get_frame(self):
        try:
            is_success, frame = self.__capture.read()

        except ... as camera_exception:  # TODO: List all possible exceptions
            raise FrameError("Error during frame capture!") from camera_exception

        if not is_success:
            raise FrameError("Unsuccessful frame capture!")

        return frame

    def convert_frame_to_png(self, frame):
        try:
            cv2.imwrite(self.__settings.IMG_PATH, frame)

        except ... as convertion_exception:  # TODO: List all possible exceptions
            raise FrameConversionError(
                "Frame conversion error!"
            ) from convertion_exception

        return self.__settings.IMG_PATH
