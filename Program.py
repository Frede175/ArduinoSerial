import time, pygame
from arduinoLib import arduino, stepper
import svgReader, head

a = arduino.Arduino("COM3", 115200)
a.connect()

a.printToLCD("Loading svg...:")

svg = svgReader.svg_reader()

a.printToLCD("Svg loaded:")

stepperX = stepper.Stepper(a, 200, 4, 6, 5, 7)
stepperY = stepper.Stepper(a, 200, 8, 10, 9, 11)
head = head.head(stepperX, stepperY)

pygame.init()
screen = pygame.display.set_mode((800,800))
currentPointNumber = 0
running = True
head.setSpeed(10)

drawRed = True

head_goto = None

a.printToLCD("Drawing:")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if drawRed:
        for x in range(0, len(svg.points)):
            screen.set_at(svg.points[x], (255, 0, 0))
            #a.printToLCD("Head; " + str(svg.points[x]))
        pygame.display.flip()
        drawRed = False

    if head_goto != None:
        try:
            p = next(head_goto)
            screen.set_at(p, (0, 255, 0))
            #a.printToLCD("Head; " + str(p))
        except StopIteration:
            head_goto = None
            screen.set_at(svg.points[currentPointNumber], (255, 255, 255))
            currentPointNumber += 1

    if currentPointNumber < len(svg.points) and head_goto == None:
        head_goto = head.goto(svg.points[currentPointNumber][0], svg.points[currentPointNumber][1])

    pygame.display.flip()

