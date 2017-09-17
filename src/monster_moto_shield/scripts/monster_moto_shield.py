#!/usr/bin/env python
import time
import rospy
import RPi.GPIO as GPIO

class ArduinoPin:
    D0  = 15
    D1  = 14
    D2  = 17
    D3  = 27
    D4  = 22
    D5  = 5
    D6  = 6
    D7  = 13
    D8  = 19
    D9  = 26
    D10 = 12
    D11 = 16
    D12 = 20
    D13 = 21
    A0 = 7
    A1 = 8
    A2 = 25
    A3 = 24
    A4 = 23
    A5 = 18
    RESET = 4

class monster_moto_shield:
    A = ArduinoPin()
    pinInA = [ A.D7, A.D4 ]
    pinInB = [ A.D8, A.D9 ]
    pinPWM = [ A.D5, A.D6 ]

    RIGHT = 1
    LEFT = 2
    FORWARD = 3
    BACKWARD = 4

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for i in range(2):
            GPIO.setup(self.pinInA[i], GPIO.OUT)
            GPIO.setup(self.pinInB[i], GPIO.OUT)
            GPIO.setup(self.pinPWM[i], GPIO.OUT)
        self.pwm = [ GPIO.PWM(self.pinPWM[0], 60),
                     GPIO.PWM(self.pinPWM[1], 60) ]
        self.stop(self.RIGHT)
        self.stop(self.LEFT)

    def get_motor(self, motor):
        if motor == self.RIGHT:
            motor = 1
        elif motor == self.LEFT:
            motor = 0
        else:
            ROS_WARN("unknown motor %d" % motor)
            motor = 0
        return motor
  
    def stop(self, motor):
        motor = self.get_motor(motor)
        GPIO.output(self.pinInA[motor], GPIO.LOW)
        GPIO.output(self.pinInB[motor], GPIO.LOW)
        self.pwm[motor].stop()

    def start(self, motor, direction, power):
        power = power * 100.0
        if 100.0 < power:
            power = 100.0
        if power < 0.0:
            power = 0.0
        if direction == self.FORWARD:
            cw = False
        elif direction == self.BACKWARD:
            cw = True
        else:
            ROS_WARN("unknown motor %d" % motor)
            return
        if motor == self.LEFT:
            cw = not cw

        motor = self.get_motor(motor)

        if cw:
            GPIO.output(self.pinInA[motor], GPIO.HIGH)
            GPIO.output(self.pinInB[motor], GPIO.LOW)
        else:
            GPIO.output(self.pinInA[motor], GPIO.LOW)
            GPIO.output(self.pinInB[motor], GPIO.HIGH)
            
        self.pwm[motor].start(power)

if __name__ == '__main__':
    mms = monster_moto_shield()
    mms.start(mms.RIGHT, mms.FORWARD, 0.2)
    mms.start(mms.LEFT, mms.FORWARD, 0.2)
    time.sleep(5)
    mms.stop(mms.RIGHT)
    mms.stop(mms.LEFT)
