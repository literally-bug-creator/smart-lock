from source.entities.camera import Camera
from source.services.face_recognizer import FaceRecognition
import cv2

camera = Camera()
frame = camera.get_image()

if frame is None:
    print("Камера не передаёт изображение.")
else:
    print("Кадр получен.")
    cv2.imshow("Camera Feed", frame)

    # Ожидаем нажатия клавиши 'q' для выхода
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Освобождаем ресурсы
camera.capture.release()
cv2.destroyAllWindows()

# Проверяем наличие лица
face = FaceRecognition()
if frame is not None:
    print("Есть ли лицо на изображении:", face.contains_face(frame))