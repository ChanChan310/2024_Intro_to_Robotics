from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S1)
ultra_sensor = UltrasonicSensor(Port.S4)

while True:

    detected_color = color_sensor.color()
    rgb_values = color_sensor.rgb()  # Returns a tuple of (R, G, B)
    distance = ultra_sensor.distance()
    
    red, green, blue = rgb_values
    intensity = (red + green + blue) // 3

    if detected_color == ColorSensor.COLOR_BLACK:
        color_name = "Black"
    elif detected_color == ColorSensor.COLOR_BLUE:
        color_name = "Blue"
    elif detected_color == ColorSensor.COLOR_GREEN:
        color_name = "Green"
    elif detected_color == ColorSensor.COLOR_YELLOW:
        color_name = "Yellow"
    elif detected_color == ColorSensor.COLOR_RED:
        color_name = "Red"
    elif detected_color == ColorSensor.COLOR_WHITE:
        color_name = "White"
    elif detected_color == ColorSensor.COLOR_BROWN:
        color_name = "Brown"
    else:
        color_name = "Unknown"

    # Clear the previous output and print the detected color
    ev3.screen.clear()
    ev3.screen.print("Detected Color: " + color_name)
    ev3.screen.print("R: {} G: {} B: {}".format(red, green, blue))
    ev3.screen.print("Intensity: {}".format(intensity))
    ev3.screen.print("Distance: {} cm".format(distance))


    wait(10) 

