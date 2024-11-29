from .settings import LockSettings
from .exceptions import ConnectionError, PinSetupError

try:
    import RPi.GPIO as GPIO
except RuntimeError as e:
    raise ConnectionError("Lock connection error!") from e


class Lock:
    def __init__(self, settings: LockSettings):
        self.__settings = settings

        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.cleanup()

        except RuntimeError as e:
            raise ConnectionError("Lock connection error!") from e

    def lock(self):
        try:
            GPIO.setup(self.__settings.PIN, GPIO.IN)

        except (RuntimeError, ValueError) as e:
            raise PinSetupError("Error setting the pin to the IN state!") from e

    def unlock(self):
        try:
            GPIO.setup(self.__settings.PIN, GPIO.OUT)

        except (RuntimeError, ValueError) as e:
            raise PinSetupError("Error setting the pin to the OUT state!") from e


def get_lock():
    settings = LockSettings()
    lock = Lock(settings)
    return lock
