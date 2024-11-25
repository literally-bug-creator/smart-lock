import cv2


class Camera:
    def __init__(
        self,
        camera_index: int,
        img_height: int,
        img_width: int,
    ):
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, img_height)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, img_width)

    def get_frame(self):
        try:
            is_success, frame = self.capture.read()

        except Exception:
            return None

        else:
            if not is_success:
                return None

            return frame
