from enum import Enum
from src.util import PinType, VALID_PINS, MORSE_LUT, MorseChars
import time
from gpiozero import LED, PWMLED


class GummyController:
    instances=[]
    def __init__(self, 
                 pin_num:int, 
                 pin_type:PinType):
        """From pin_num and pin_type, initialize gpio pin"""
        if pin_num in GummyController.instances:
            raise Exception(f"An instance of GummyController for pin {pin_num} already exists.")
        else:
            self.pin_num=pin_num
            GummyController.instances.append(pin_num)
        if pin_type == PinType.PWM and pin_num in VALID_PINS[pin_type]:
            self.pin = PWMLED(pin_num)
        elif pin_type == PinType.NORMAL and pin_num in VALID_PINS[pin_type]:
            self.pin = LED(pin_num)
        else:
            raise Exception("Failed to construct controller. Check GPIO pins")
        self.pin_type=pin_type
        self.binary_dur=0.25
        self.morse_rest=0.05
        self.binary_rest=0.05
        self.morse_scale=0.1

    @property
    def morse_lens(self):
        return{MorseChars.DOT: self.morse_scale,
               MorseChars.DASH: self.morse_scale*3,
               MorseChars.NONE: 0}
    
    def configure_timescale(self,
                            morse_scale:float,
                            binary_dur:float,
                            morse_rest:float,
                            binary_rest:float):
        """Configure timescales"""
        self.binary_dur = binary_dur
        self.morse_rest = morse_rest
        self.binary_rest = binary_rest
        self.morse_scale = morse_scale
        
    def light_pin(self, dur_sec:int, level:float=1):
        """
            Light the pin for dur_sec. If configured for pwm, level is duty cycle
        """
        if level>1:
            level=1
        elif level<0:
            level=0

        if self.pin_type == PinType.PWM:
            self.pin.value=level
        elif self.pin_type == PinType.NORMAL:
            if level == 0:
                self.pin.off()
            else:
                self.pin.on()
        else:
            raise Exception("idk what you did man...")  
        time.sleep(dur_sec)

    def flash_pin(self, dur_sec:int, level:float=1):
        """
            Flash the pin for dur_sec. If configured for pwn, level is duty cycle
        """
        self.light_pin(dur_sec, level)
        if self.pin_type == PinType.PWM:
            self.pin.value=0
        elif self.pin_type == PinType.NORMAL:
            self.pin.off()
        else:
            raise Exception("You can't keep getting away with this...")

    def breathe_pulses(self, 
                       on_dur:float,
                       off_dur:float,
                       pulse_cnt:int):
        """Flash the gummy bear to breathe in a pulse"""
        if self.pin_type == PinType.PWM:
            self.pin.pulse(n=pulse_cnt,
                           fade_in_time=on_dur,
                           fade_out_time=off_dur,
                           background=False)
        elif self.pin_type == PinType.NORMAL:
            self.pin.blink(on_time=on_dur, off_time=off_dur)

    def flash_morse(self, flash_str:str, level:float=1):
        """Flash gummy bear from flash_str using morse"""
        str_upper = flash_str.upper()
        morse_mapped_str = "".join(list([MORSE_LUT.get(character, "") for character in str_upper]))
        for char_str in morse_mapped_str:
            morse_char = MorseChars(char_str)
            char_dur = self.morse_lens[morse_char]
            self.flash_pin(char_dur, level)
            time.sleep(self.morse_rest)
    
    def flash_binary(self, flash_str:str, level:float=1):
        """Flash gummy bear from flash_str using binary"""
        bin_mapped_str = ''.join(format(ord(char), '08b') for char in flash_str)
        for bin_str in bin_mapped_str:
            if bin_str == "1":
                self.flash_pin(self.binary_dur, level)
            else:
                self.flash_pin(self.binary_dur, 0.1)
            time.sleep(self.binary_rest)

    def __del__(self):
        if self.pin_num in GummyController.instances:
           GummyController.instances.remove(self.pin_num)
