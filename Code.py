import time
import board
import adafruit_hcsr04
import pulseio
import random
from adafruit_motor import servo
from adafruit_circuitplayground.express import cpx


def set_servo(x):
    """
    :param i: fuction to define a servo with the parameter of board pin
    :return: a servo
    """
    pwm = pulseio.PWMOut(x, duty_cycle=2 ** 15, frequency=50)
    return servo.Servo(pwm, min_pulse=620, max_pulse=2320)

servo1 = set_servo(board.A1)
servo2 = set_servo(board.A2)
servo3 = set_servo(board.A3)
servo4 = set_servo(board.A6)

#pwm1 = pulseio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
#servo1 = servo.Servo(pwm1, min_pulse=620, max_pulse=2320)
#pwm2 = pulseio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
#servo2 = servo.Servo(pwm2, min_pulse=620, max_pulse=2320)
#pwm3 = pulseio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency=50)
#servo3 = servo.Servo(pwm3, min_pulse=620, max_pulse=2320)
#pwm4 = pulseio.PWMOut(board.A6, duty_cycle=2 ** 15, frequency=50)
#servo4 = servo.Servo(pwm4, min_pulse=620, max_pulse=2320)

def move_constrain(i):
    """
    :param i: import number to control the movement when the distance is within 15
    :return: a range
    """
    if i < 0:
        i = 0
    elif i > 90:
        i = 90
    return i


def cry_constrain(i):
    """
    :param i: import number to control the random movement when the distance is out of 15
    :return: a range for hug_angle rotation
    """
    if i < 20:
        i = 20
    elif i > 40:
        i = 40
    return i

# Using Ultrasonic
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A4, echo_pin=board.A5)
# Servos list
list_servo = [servo1, servo2, servo3, servo4]
# Start list angle
list_hug_angle = [0, 0, 0, 0]
rotation = 2
servo3.angle = 120
servo4.angle = 120


while True:
    try:
        if sonar.distance <= 50:
            print (sonar.distance)
            list_hug_angle = [move_constrain(list_hug_angle[i] + rotation) for i in range(4)]

            #for i in range(4):
            #    list_hug_angle[i] += rotation
            #    list_hug_angle[i] = move_constrain(list_hug_angle[i])

        else:

            list_hug_angle = [cry_constrain(list_hug_angle[i]) + random.randint(-20, 20) for i in range(4)]

            #for i in range(4):
            #    list_hug_angle[i] = cry_constrain(list_hug_angle[i]) + random.randint(-20, 20)

    except RuntimeError:
        list_hug_angle = [cry_constrain(list_hug_angle[i]) + random.randint(-20, 20) for i in range(4)]

        #for i in range(4):
        #        list_hug_angle[i] = cry_constrain(list_hug_angle[i]) + random.randint(-20, 20)

    print (list_hug_angle)
    for i in range(4):
        if i <= 1:
            list_servo[i].angle = list_hug_angle[i]
        elif i >1 and i<=3:
            list_servo[i].angle = 120 - list_hug_angle[i]

    time.sleep(0.05)
