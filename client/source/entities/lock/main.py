import RPi.GPIO as GPIO


class Lock:
    def __init__(self):
        self.__is_locked = False

    def lock(self):  # TODO: Test logic of closing
        if self.__is_locked:
            return

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, GPIO.HIGH)

        self.__is_locked = True

    def unlock(self):  # TODO: Test logic of opening
        if not self.__is_locked:
            return

        GPIO.cleanup()

        self.__is_locked = False
