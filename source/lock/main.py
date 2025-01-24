from .settings import LockSettings

try:
    import RPi.GPIO as GPIO
except RuntimeError as e:
    raise ConnectionError("Lock connection error!") from e


class Lock:
    def __init__(self, settings: LockSettings):
        self.__settings = settings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.cleanup()

    def lock(self):
        GPIO.setup(self.__settings.PIN, GPIO.IN)

    def unlock(self):
        GPIO.setup(self.__settings.PIN, GPIO.OUT)


def get_lock():
    settings = LockSettings()
    lock = Lock(settings)
    return lock
