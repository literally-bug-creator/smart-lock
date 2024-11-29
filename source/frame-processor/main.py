import os
import cv2
import cv2.data
from cv2.typing import MatLike
from .settings import FrameProcessorSettings
from .exceptions import ConnectionError, FaceRecognizeError


class FrameProcessor:
    def __init__(self, settings: FrameProcessorSettings):
        self.__settings = settings

        try:
            self.__classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + self.__settings.CLASSIFIER
            )

        except () as e:  # TODO: Add all possible exceptions
            raise ConnectionError("Failed to exec classifier!") from e

    def contains_face(self, frame: MatLike) -> bool:
        try:
            grayed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.__classifier.detectMultiScale(
                image=grayed_frame,
                scaleFactor=self.__settings.SCALE_FACTOR,
                minNeighbors=self.__settings.MIN_NEIGHBORS,
                minSize=(self.__settings.MIN_SIZE_X, self.__settings.MIN_SIZE_Y),
            )

        except () as recognize_exception:  # TODO: Add all possible exceptions
            raise FaceRecognizeError(
                "Failed to recognize faces!"
            ) from recognize_exception

        return len(faces) > 0

    def save_frame(self, frame: MatLike):
        is_saved = cv2.imwrite("frame.png", frame)

        if is_saved:
            return os.path.abspath(os.path.join(os.getcwd(), "frame.png"))

        return None


def get_frame_processor():
    settings = FrameProcessorSettings()
    frame_processor = FrameProcessor(settings)
    return frame_processor
