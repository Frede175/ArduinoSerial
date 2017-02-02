# Writing with help from the Arduino source code.
# https://github.com/arduino/Arduino/blob/master/libraries/Stepper/src/Stepper.cpp
import time
from arduinoLib import arduino


class Stepper(object):

    def __init__(self, a, number_of_steps, pin_1, pin_2, pin_3, pin_4):
        self.direction = 0
        self.step_number = 0
        self.last_step_time = 0
        self.arduino = a
        self.number_of_steps = number_of_steps
        self.pin_1 = pin_1
        self.pin_2 = pin_2
        self.pin_3 = pin_3
        self.pin_4 = pin_4
        self.delay = 60 * 1000 * 1000 / number_of_steps / 1

        self.arduino.pinMode(pin_1, arduino.OUTPUT)
        self.arduino.pinMode(pin_2, arduino.OUTPUT)
        self.arduino.pinMode(pin_3, arduino.OUTPUT)
        self.arduino.pinMode(pin_4, arduino.OUTPUT)

    def setSpeed(self, speed):
        self.delay = (60 * 1000 * 1000) / self.number_of_steps / speed

    def step(self, steps_to_move):
        steps_left = abs(steps_to_move)
        if steps_to_move < 0:
            self.direction = 0
        elif steps_to_move > 0:
            self.direction = 1


        while steps_left > 0:
            now = self.current_micro()
            if now - self.last_step_time >= self.delay:
                self.last_step_time = now

                if self.direction == 1:

                    self.step_number += 1
                    if self.step_number == self.number_of_steps:
                        self.step_number = 0
                if self.direction == 0:

                    if self.step_number == 0:
                        self.step_number = self.number_of_steps
                    self.step_number -= 1
                steps_left -= 1
                self.stepMotor(self.step_number % 4)

    def stepMotor(self, step):
        if step == 0:
            self.arduino.digitalWrite(self.pin_1, 1)
            self.arduino.digitalWrite(self.pin_2, 0)
            self.arduino.digitalWrite(self.pin_3, 1)
            self.arduino.digitalWrite(self.pin_4, 0)
        elif step == 1:
            self.arduino.digitalWrite(self.pin_1, 0)
            self.arduino.digitalWrite(self.pin_2, 1)
            self.arduino.digitalWrite(self.pin_3, 1)
            self.arduino.digitalWrite(self.pin_4, 0)
        elif step == 2:
            self.arduino.digitalWrite(self.pin_1, 0)
            self.arduino.digitalWrite(self.pin_2, 1)
            self.arduino.digitalWrite(self.pin_3, 0)
            self.arduino.digitalWrite(self.pin_4, 1)
        elif step == 3:
            self.arduino.digitalWrite(self.pin_1, 1)
            self.arduino.digitalWrite(self.pin_2, 0)
            self.arduino.digitalWrite(self.pin_3, 0)
            self.arduino.digitalWrite(self.pin_4, 1)

    @staticmethod
    def current_micro():
        return int(round(time.time() * 1000 * 1000))
