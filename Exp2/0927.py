from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Color, Button
from pybricks.tools import wait

#------initialize------------------------------------------------------------------------------------------------------------------


# Initialize the EV3 Brick
ev3 = EV3Brick()

# Initialize Ports
lift_motor = Motor(Port.A)
left_motor = Motor(Port.C)
right_motor = Motor(Port.D)
color_sensor = ColorSensor(Port.S1)
ultra_sensor = UltrasonicSensor(Port.S4)

# Set the motor speed
SPEED = 50
TURN_RATE = 25

# Set the delay of the tracking line
DELAY = 10
CROSS_LINE_DELAY = 100

#Set the map data structure
color_order_list = ["blue", "red", "black"]

#------color define------------------------------------------------------------------------------------------------------------------

# Define the target color or light intensity (adjust based on your needs)
black = Color.BLACK  # or use a brightness level like color_sensor.reflection()
red = Color.RED 
blue = Color.BLUE 
yellow = Color.YELLOW

#------function------------------------------------------------------------------------------------------------------------------

#循跡:一律靠線的左邊

#循跡直到遇到目標顏色(尋黃線遇到藍、紅、黑；尋藍線遇到黃)
def track_color(direction, line_color, target_color):
    
    while color_sensor.color() != target_color:
        
        if color_sensor.color() == line_color:
            left_motor.run(direction* (SPEED - TURN_RATE) )
            right_motor.run(direction*SPEED)
        else:
            left_motor.run(direction*SPEED)
            right_motor.run(direction* (SPEED - TURN_RATE) )

        wait(DELAY)

#循跡直到遇到籃子(尋藍、紅、黑線遇到籃子)
#要注意停下來時color sensor譨感應到色卡
def track_ultra(line_color):

    while ultra_sensor.distance() > 10:
        
        if color_sensor.color() == line_color:
            left_motor.run(SPEED - TURN_RATE)
            right_motor.run(SPEED)
        else:
            left_motor.run(SPEED)
            right_motor.run(SPEED - TURN_RATE)

        wait(DELAY)


#停止、轉彎、直行與後退

def stop():
    left_motor.stop(Stop.HOLD)
    right_motor.stop(Stop.HOLD)
    wait(100)

def forward():
    left_motor.run(SPEED)
    right_motor.run(SPEED)
    wait(150)

def backward():
    left_motor.run(-SPEED)
    right_motor.run(-SPEED)
    wait(300)

#轉彎是活的轉彎，取兩輪中檢為軸旋轉
def turn_right(line_color):
    left_motor.run(SPEED)
    right_motor.run(-SPEED)
    wait(100)
    while color_sensor.color() != line_color:
        left_motor.run(SPEED)
        right_motor.run(-SPEED)
        wait(DELAY)

def turn_left(line_color):
    left_motor.run(-SPEED)
    right_motor.run(SPEED)
    wait(100)
    while color_sensor.color() != line_color:
        left_motor.run(-SPEED)
        right_motor.run(SPEED)
        wait(DELAY)




#控制爪子

def lift_up():
    #lift_motor.run_target(100, 90) #前面是速度、後面是"角度位置"
    lift_motor.run_angle(100, -90)  #前面是速度、後面是"角度距離"
    lift_motor.stop(Stop.HOLD)

def lift_down():
    #lift_motor.run_target(100, 90) #Moves the motor to the absolute position of 90 degrees.
    lift_motor.run_angle(100, 90)   #Moves the motor by 90 degrees from its current position.
    lift_motor.stop(Stop.HOLD)
    

#------sub_main------------------------------------------------------------------------------------------------------------------

def pick_up_the_ball(line_color):
    stop()
    forward()
    turn_left(line_color)
    track_ultra(line_color)
    stop()
    lift_down()
    backward()
    track_color(-1,line_color,yellow)
    stop()
    turn_right(yellow)     

def put_down_the_ball(line_color): #從主幹道轉進去放球在回到主幹道
    stop()
    forward() 
    turn_left(line_color)
    track_ultra(line_color)
    stop()
    lift_up()
    backward()
    track_color(-1,line_color,yellow)
    stop()
    turn_right(yellow)


#------main------------------------------------------------------------------------------------------------------------------

#第一步驟:按下橘色按鈕後車子才會動
ev3.screen.clear()
ev3.screen.print("press center buttom")
while Button.CENTER not in ev3.buttons.pressed():
    wait(10)

ev3.screen.clear()
ev3.screen.print("Start in 1 second")
wait(1000)
ev3.screen.clear()

#第二步驟:車子往前進入第一彎道
forward()
track_color(1,yellow,blue)
stop()
forward()
turn_left(blue)
track_ultra(blue)
stop()

#第三步驟:判斷第一個籃子顏色

if color_sensor.color() == black:
    color_order_list[0] = "black"
    ev3.screen.print("black")    
elif color_sensor.color() == red:
    color_order_list[0] = "red"
    color_order_list[1] = "black"
    color_order_list[2] = "blue"
    ev3.screen.print("red")
    ev3.screen.print("black")
    ev3.screen.print("blue") 
else:
    color_order_list[1] = "black"
    color_order_list[2] = "red"
    ev3.screen.print("blue")
    ev3.screen.print("black")
    ev3.screen.print("red")

#第四步驟:把黑球拖到場外
if color_order_list[0] == "black":  #黑球在第一個籃子
    lift_down()
    backward()
    track_color(-1,blue,yellow)
    stop()
    turn_right(yellow)
    track_color(1,yellow,red)
    forward()
    track_color(1,yellow,black)
    forward()
    track_color(1,yellow,black)
    stop()
else:                               #黑球沒有在第一個的話迪定在第二個
    backward()
    track_color(-1,blue,yellow)
    stop()
    turn_right(yellow)
    track_color(1,yellow,red)
    pick_up_the_ball(red)           #去紅線拿黑球
    track_color(1,yellow,black)
    forward()
    track_color(1,yellow,black)
    stop()

lift_up()
backward()

#此時車子應該要停在黑球放置區
#第五步驟:開始變得很複雜...(總共四種case分開討論)

if color_order_list[0] == "blue":   #藍黑紅!!!!!!!!!!!!!!!!!!!!
    track_color(-1,yellow,black)
    pick_up_the_ball(black)         #去黑線拿紅球
    backward()
    track_color(-1,yellow,red)
    put_down_the_ball(red)          #去紅線放球
    stop()
    ev3.screen.clear()
    ev3.screen.print("mission complete")       

elif color_order_list[0] == "red":  #紅黑藍!!!!!!!!!!!!!!!!!!!!
    track_color(-1,yellow,black)
    backward()
    track_color(-1,yellow,red)
    backward()
    track_color(-1,yellow,blue)
    pick_up_the_ball(blue)          #去藍線拿紅球
    track_color(1,yellow,red)
    put_down_the_ball(red)          #去紅線放球
    track_color(1,yellow,black)
    pick_up_the_ball(black)         #去黑線拿藍球
    backward()
    track_color(-1,yellow,red)
    backward()
    track_color(1,yellow,blue)
    put_down_the_ball(blue)         #去藍線放球
    stop()
    ev3.screen.clear()
    ev3.screen.print("mission complete")    

else:                               #黑XX!!!!!!!!!!!!!!!!!!!!
    track_color(-1,yellow,black)
    stop()
    turn_left(black)
    track_ultra(black)
    stop()
    
    if color_sensor.color() == blue:  #黑紅藍!!!!!!!!!!!!!!!!!!!!
        ev3.screen.print("red")
        ev3.screen.print("blue")
        lift_down()
        backward()
        track_color(-1,black,yellow)
        stop()
        turn_right(yellow)
        backward()
        track_color(-1,yellow,red)
        backward()
        track_color(-1,yellow,blue)
        put_down_the_ball(blue)     #去藍線放球
        stop()
        ev3.screen.clear()
        ev3.screen.print("mission complete")  
    
    else:                           #黑藍紅!!!!!!!!!!!!!!!!!!!!
        ev3.screen.print("blue")
        ev3.screen.print("red")
        backward()
        track_color(-1,black,yellow)
        stop()
        turn_right(yellow)
        backward()
        track_color(-1,yellow,red)
        pick_up_the_ball(red)       #去紅線拿藍球
        backward()
        track_color(-1,yellow,blue)
        put_down_the_ball(blue)     #去藍線放球
        track_color(1,yellow,red)
        forward()
        track_color(1,yellow,black)   
        pick_up_the_ball(black)
        backward()
        track_color(1,yellow,red)
        put_down_the_ball(red)
        stop()
        ev3.screen.clear()
        ev3.screen.print("mission complete")         


