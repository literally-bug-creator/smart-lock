import RPi.GPIO as GPIO


class Lock:
    def __init__(self, pin: int):
        self.__pin = pin
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

    def lock(self):
        GPIO.setup(self.__pin, GPIO.IN)

    def unlock(self):
        GPIO.setup(self.__pin, GPIO.OUT)
