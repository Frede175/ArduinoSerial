from arduinoLib import arduino, stepper

class head(object):

    def __init__(self, stepperX, stepperY):
        self.x = 0
        self.y = 0
        self.servoPos = 90  # 0 for down, 90 for up
        self.stepperX = stepperX
        self.stepperY = stepperY
        self.speed = 1
        self.stepperX.setSpeed(self.speed)
        self.stepperY.setSpeed(self.speed)

    def setSpeed(self, speed):
        self.stepperX.setSpeed(speed)
        self.stepperY.setSpeed(speed)

    def stepX(self, steps):
        self.x += steps
        self.stepperX.step(steps)

    def stepY(self, steps):
        self.y += steps
        self.stepperY.step(steps)

    def setValueX(self, x):
        self.x = x

    def setValueY(self, y):
        self.y = y

    def goto(self, x, y):
        x_diff = x - self.x
        y_diff = y - self.y
        if x_diff == 0 and y_diff == 0:
            return
        y_dir = 0
        if y_diff > 0: y_dir = 1
        elif y_diff < 0: y_dir = -1
        x_dir = 0
        if x_diff > 0: x_dir = 1
        elif x_diff < 0: x_dir = -1

        if abs(x_diff) == abs(y_diff) or x_diff == 0 or y_diff == 0:
            if x_diff == 0: to_move = abs(y_diff)
            else: to_move = abs(x_diff)

            while to_move > 0:
                self.stepperY.step(y_dir)
                self.y += y_dir
                self.stepperX.step(x_dir)
                self.x += x_dir
                to_move -= 1
                yield (self.x, self.y)

        else:
            ratio = abs(x_diff)/abs(y_diff)
            if ratio < 1:
                fx = ratio
                while self.y != y:
                    if round(fx) >= 1:
                        self.stepperX.step(x_dir)
                        self.x += x_dir
                        fx -= 1
                    self.stepperY.step(y_dir)
                    self.y += y_dir
                    fx += ratio
                    yield (self.x, self.y)
                while self.x != x:
                    dir = x - self.x
                    self.stepperX.step(dir)
                    self.x += dir
                    yield (self.x, self.y)
            else:
                ratio = abs(y_diff)/abs(x_diff)
                fy = ratio
                while self.x != x:
                    if round(fy) >= 1:
                        self.stepperY.step(y_dir)
                        self.y += y_dir
                        fy -= 1
                    self.stepperX.step(x_dir)
                    self.x += x_dir
                    fy += ratio
                    yield (self.x, self.y)
                while self.y != y:
                    dir = y - self.y
                    self.stepperY.step(dir)
                    self.y += dir
                    yield (self.x, self.y)



