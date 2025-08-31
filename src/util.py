from enum import Enum

class PinType(Enum):
    NORMAL=0
    PWM=1

VALID_PINS ={
    PinType.PWM: [18,12,13,18],
    PinType.NORMAL: [2,3,4,17,27,22,10,9,11,5,6,26,14,15,23,24,25,16]
}
