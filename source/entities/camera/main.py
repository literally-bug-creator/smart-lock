import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_image(self):
        try:
            ret, frame = self.capture.read()
            if not ret:
                print("Камера не передаёт изображение")
                return None

            if frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
                print("Изображение пустое или повреждено")
                return None

            return frame

        except Exception as e:
            print("Ошибка при подключении к камере:", str(e))
            return None
