import time, pygame
from arduinoLib import arduino, stepper
import svgReader, head

svg = svgReader.svg_reader()

a = arduino.Arduino("COM3", 115200)
a.connect()

stepperX = stepper.Stepper(a, 200, 2, 3, 4, 5)
stepperY = stepper.Stepper(a, 200, 6, 7, 8, 9)
head = head.head(stepperX, stepperY)

pygame.init()
screen = pygame.display.set_mode((800,800))
currentPointNumber = 0
running = True
head.setSpeed(10)

drawRed = True

head_goto = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if drawRed:
        for x in range(0, len(svg.points)):
            screen.set_at(svg.points[x], (255, 0, 0))
        pygame.display.flip()
        drawRed = False

    if head_goto != None:
        try:
            screen.set_at(next(head_goto), (0, 255, 0))
        except StopIteration:
            head_goto = None
            screen.set_at(svg.points[currentPointNumber], (255, 255, 255))
            currentPointNumber += 1

    if currentPointNumber < len(svg.points) and head_goto == None:
        head_goto = head.goto(svg.points[currentPointNumber][0], svg.points[currentPointNumber][1])

    pygame.display.flip()

