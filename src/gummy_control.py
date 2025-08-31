import RPi.GPIO as GPIO
from enum import Enum
from util import PinType, VALID_PINS
import time

PWM_FREQUENCY=120

class GummyController:
    def __init__(self, pin_num:int, pin_type:PinType):
        """From pin_num and pin_type, initialize gpio pin"""
        if pin_type == PinType.PWM and pin in VALID_PINS[pin_type]:
            self.pin = GPIO.PWM(pin, PWM_FREQUENCY)
        elif pin_type == PinType.NORMAL and pin in VALID_PINS[pin_type]:
            self.pin =
        else:
            raise Exception("Failed to construct controller")
        self.pin_typ=pin_type

    def flash_pin(self, dur_sec:int, level:int=1):
        """
            Flash the pin for dur_sec. If configured for pwn, level is duty cycle
        """
        level = level % 101
        if self.pin_type == PinType.PWM:
            self.pin.start(level)
            time.sleep(dur_sec)
            self.pin.ChangeDutyCycle(0)
            self.pin.stop()
        elif self.pin_type == PinType.NORMAL:
            """"""
        else:
            raise Exception("idk what you did man...")
