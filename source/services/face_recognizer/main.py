import cv2


class FaceRecognition:
    def __init__(
        self,
        classifier: str,
        scale_factor: float,
        min_neighbors: int,
        min_size_x: int,
        min_size_y: int,
    ):
        self.__classifier = cv2.CascadeClassifier(cv2.data.haarcascades + classifier)
        self.__scale_factor = scale_factor
        self.__min_neighbors = min_neighbors
        self.__min_size = (min_size_x, min_size_y)

    def contains_face(self, img) -> bool:
        grayed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.__classifier.detectMultiScale(
            image=grayed_img,
            scaleFactor=self.__scale_factor,
            minNeighbors=self.__min_neighbors,
            minSize=self.__min_size,
        )

        return len(faces) > 0
