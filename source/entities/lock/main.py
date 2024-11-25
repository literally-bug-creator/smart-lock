import RPi.GPIO as GPIO


class Lock:
    def __init__(self, pin: int):
        self.__pin = pin
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pin, GPIO.OUT)

    def lock(self):
        GPIO.setup(self.__pin, GPIO.IN)

    def unlock(self):
        GPIO.output(self.__pin, GPIO.HIGH)
