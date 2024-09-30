from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

color_sensor = ColorSensor(Port.S1)

def color_detect(color):
    
    rgb_values = color_sensor.rgb()
    red, green, blue = rgb_values
    detected_color = "white"
    if red > 0  and red < 0 and green > 0 and green < 0 and blue > 0 and blue < 0:
        detected_color = "yellow"
    elif red > 0  and red < 0 and green > 0 and green < 0 and blue > 0 and blue < 0:
        detected_color = "blue"
    elif red > 0  and red < 0 and green > 0 and green < 0 and blue > 0 and blue < 0:
        detected_color = "red"
    elif red > 0  and red < 0 and green > 0 and green < 0 and blue > 0 and blue < 0:
        detected_color = "black"
    
    if detected_color == color:
        return True
    else:
        return False