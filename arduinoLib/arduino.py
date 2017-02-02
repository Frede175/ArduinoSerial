import serial
import time

INPUT = 0x0
OUTPUT = 0x1


class Arduino(object):

    def __init__(self, com_port, rate):
        self.serial = None
        self.error = None
        self.com = com_port
        self.rate = rate

    def connect(self):
        try:
            self.serial = serial.Serial(self.com, self.rate)
            time.sleep(3)
        except serial.SerialException:
            self.error = "Serial Error"
            print("ERROR: " + self.error)
            return False
        return True

    # Digital write on the arduino
    def digitalWrite(self, pin, value):
        # Check if the connect is ok
        if not self.serial is None:
            self.serial.write(("W:D:" + str(pin) + ":" + str(value) + "\n").encode('ascii'))

    def pinMode(self, pin, mode):
        if not self.serial is None:
            self.serial.write(("S:P:" + str(pin) + ":" + str(mode) + "\n").encode('ascii'))
            time.sleep(0.1)

    def digitalRead(self, pin):
        if not self.serial is None:
            self.serial.write(("R:D:" + str(pin) + "\n").encode('ascii'))
            # time.sleep(0.01)
            input = int(self.serial.readline())
            return input

    def read(self):
        return self.serial.readline()

    def attachServo(self, servoNumber, pin):
        if not self.serial is None:
            self.serial.write(("S:S:" + str(servoNumber) + ":" + str(pin) + "\n").encode('ascii'))
            time.sleep(0.1)

    def servoWrite(self, servoNumber, pos):
        if not self.serial is None:
            self.serial.write(("W:S:" + str(servoNumber) + ":" + str(pos) + "\n").encode('ascii'))

    def printToLCD(self, text):
        if not self.serial is None:
            self.serial.write(("D:T:" + str(text)).encode('ascii'))
        else:
            print(text)