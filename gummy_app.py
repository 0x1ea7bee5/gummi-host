from flask import Flask, request, render_template
from src.gummy_control import GummyController
from src.util import PinType, VALID_PINS, ControllerMode
import tomllib
import os

_CWD=os.getcwd()


app = Flask(__name__)

with open("app_cfg.toml","rb") as f:
    app_cfg = tomllib.load(f)

connection_cfg = app_cfg["connection"]

def gummy_request(req_dict:dict):
    """"""
    level = req_dict.get("level",1)
    pin_number = req_dict.get("pin_number",18)
    binary_dur = req_dict.get("binary_dur",0.25)
    morse_scale = req_dict.get("morse_scale",0.1)
    morse_rest = req_dict.get("morse_rest", 0.05)
    binary_rest = req_dict.get("binary_rest", 0.05)
    mode_str = req_dict.get("mode","")
    if mode_str not in ControllerMode:
        mode_str = ""
    mode=ControllerMode(mode_str)
    str_text = req_dict.get("str_text","")
    num_pulses = req_dict.get("num_pulses",10)
    pulse_on = req_dict.get("pulse_on", 2)
    pulse_off = req_dict.get("pulse_off",1)
    
    if pin in VALID_PINS[PinType.PWM]:
        pin_type = PinType.PWM
    elif pin in VALID_PINS[PinType.NORMAL]:
        pin_type = PinType.NORMAL
    else:
        raise Exception("Invalid Pin Number")
    controller = GummyController(pin_number, pin_type)
    controller.configure_timescale(morse_scale, binary_dur, morse_rest, binary_rest)
    if mode == ControllerMode.MORSE:
        controller.flash_morse(str_text,level)
    elif mode == ControllerMode.BINARY:
        controller.flash_binary(str_text,level)
    elif mode == ControllerMode.PULSE:
        controller.breathe_pulses(pulse_on, pulse_off, num_pulses)
    else:
        return "Successfully Completed Action"

def gummy_pulse(req_dict:dict):

    level = req_dict.get("level",1)
    pin_number = req_dict.get("pin_number",18)
    pin_number = int(pin_number)
    num_pulses = req_dict.get("num_pulses",10)
    num_pulses = int(num_pulses)
    pulse_on = req_dict.get("pulse_on", 2)
    pulse_on = float(pulse_on)
    pulse_off = req_dict.get("pulse_off",1)
    pulse_off = float(pulse_off)
    if pin_number in VALID_PINS[PinType.PWM]:
        pin_type = PinType.PWM
    elif pin_number in VALID_PINS[PinType.NORMAL]:
        pin_type = PinType.NORMAL
    else:
        raise Exception("Invalid Pin Number")    
    controller = GummyController(pin_number, pin_type)
    controller.breathe_pulses(pulse_on, pulse_off, num_pulses)


def gummy_morse(req_dict:dict):
    level = req_dict.get("level",1)
    pin_number = req_dict.get("pin_number",18)
    pin_number = int(pin_number)
    binary_dur = req_dict.get("binary_dur",0.25)
    morse_scale = req_dict.get("morse_scale",0.25)
    morse_rest = req_dict.get("morse_rest", 0.25)
    binary_rest = req_dict.get("binary_rest", 0.05)
    str_text = req_dict.get("str_text","")
    if pin_number in VALID_PINS[PinType.PWM]:
        pin_type = PinType.PWM
    elif pin_number in VALID_PINS[PinType.NORMAL]:
        pin_type = PinType.NORMAL
    else:
        raise Exception("Invalid Pin Number")    
    controller = GummyController(pin_number, pin_type)
    controller.configure_timescale(morse_scale, binary_dur, morse_rest, binary_rest)
    controller.flash_morse(str_text, level)



@app.route("/")
def home():
    html_path = os.path.join(_CWD,"html","gummi.html")
    return render_template("gummi.html")

@app.route("/handle_gummy_request", methods=["POST"])
def handle_gummy_request():
    """Handles Gummy Controller requests by the user"""
    if request.method == "POST":
        request_dict = request.form
        try:
            str_return = gummy_request(request_dict)
            return str_return
        except:
            return "Failed to handle request"

@app.route("/handle_gummy_morse", methods=["POST"])
def handle_gummy_morse():
    """Morse Requests"""
    if request.method == "POST":
        #breakpoint()
        request_dict = request.form
        try:
            str_return = gummy_morse(request_dict)
            return "Gummy bear has been morsed"
        except:
            return "Failed to handle request"

@app.route("/handle_gummy_pulse", methods=["POST"])
def handle_gummy_pulse():
    """Morse Requests"""
    if request.method == "POST":
        request_dict = request.form
        try:
            str_return = gummy_pulse(request_dict)
            return "Gummy bear has been pulsed"
        except:
            return "Failed to handle request"


if __name__=="__main__":
    print(connection_cfg["host"])
    app.run(host=connection_cfg["host"],port=connection_cfg["port"])
