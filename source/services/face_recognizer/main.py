import cv2
from .settings import FaceRecognizerSettings
from .exceptions import ConnectionError, RecognizeError


class FaceRecognizerService:
    def __init__(
        self,
        settings: FaceRecognizerSettings,
    ):
        self.__settings = settings

    def connect(self):
        try:
            self.__classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + self.__settings.CLASSIFIER
            )

        except (
            cv2.error,
            FileNotFoundError,
            PermissionError,
            OSError,
        ) as connection_exception:
            raise ConnectionError(
                "Failed to exec classifier!"
            ) from connection_exception

    def contains_face(self, img) -> bool:
        try:
            grayed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.__classifier.detectMultiScale(
                image=grayed_img,
                scaleFactor=self.__settings.SCALE_FACTOR,
                minNeighbors=self.__settings.MIN_NEIGHBORS,
                minSize=(self.__settings.MIN_SIZE_X, self.__settings.MIN_SIZE_Y),
            )

        except (cv2.error, TypeError) as recognize_exception:
            raise RecognizeError("Failed to recognize faces!") from recognize_exception

        return len(faces) > 0
