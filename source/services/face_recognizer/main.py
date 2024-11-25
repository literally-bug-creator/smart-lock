import cv2
from source.entities.camera import Camera

class FaceRecognition:
    def __init__(self):
        # Загрузка предобученного классификатора для обнаружения лиц
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def contains_face(self, img) -> bool:
        # Преобразуем изображение в оттенки серого для классификатора
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Ищем лица на изображении
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        print(f"Найдено лиц: {len(faces)}")

        # Если хотя бы одно лицо найдено, возвращаем True
        return len(faces) > 0
