import RPi.GPIO as GPIO
from .settings import LockSettings
from .exceptions import ConnectionError, PinSetupError


class LockService:
    def __init__(self, settings: LockSettings):
        self.__settings = settings
        self.__pin = self.__settings.PIN

    def connect(self):
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.cleanup()

        except RuntimeError as connection_exception:
            raise ConnectionError("Lock connection error!") from connection_exception

    def lock(self):
        try:
            GPIO.setup(self.__pin, GPIO.IN)

        except (
            RuntimeError,
            ValueError,
        ) as pin_setup_exception:
            raise PinSetupError(
                "Error setting the pin to the IN state!"
            ) from pin_setup_exception

    def unlock(self):
        try:
            GPIO.setup(self.__pin, GPIO.OUT)

        except (
            RuntimeError,
            ValueError,
        ) as pin_setup_exception:
            raise PinSetupError(
                "Error setting the pin to the OUT state!"
            ) from pin_setup_exception
