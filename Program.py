import time, pygame
import queue

from arduinoLib import arduino, stepper
import svgReader, head, threading


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
clock.tick(60)

running = True

a = arduino.Arduino("COM3", 115200)
a.connect()

a.printToLCD("Loading svg...:")

stepperX = stepper.Stepper(a, 200, 4, 6, 5, 7)
stepperY = stepper.Stepper(a, 200, 8, 10, 9, 11)
head = head.head(stepperX, stepperY)

head.setSpeed(25)
currentPointNumber = 0
drawRed = True

progress = []
head_goto = None

a.printToLCD("Drawing:")

myfont = pygame.font.SysFont(None, 15)

# render text
label = myfont.render("Loading svg!", 1, (255,255,0))
screen.blit(label, (100, 100))
pygame.display.flip()

svg = svgReader.svg_reader('C:\\Users\\fsr19\\Desktop\\Raspberry_Pi_Logo.svg')
screen.fill((0, 0, 0))
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if drawRed:
        for x in range(0, len(svg.points)):
            screen.set_at(svg.points[x], (255, 0, 0))
            # a.printToLCD("Head; " + str(svg.points[x]))
        pygame.display.flip()
        drawRed = False

    if head_goto != None:
        try:
            p = next(head_goto)
            if head.servoPos is not 0:
                head.servoPos = 0
            screen.set_at(p, (0, 255, 0))
            # a.printToLCD("Head; " + str(p))
        except StopIteration:
            head_goto = None
            screen.set_at(svg.points[currentPointNumber], (255, 255, 255))
            currentPointNumber += 1

    if currentPointNumber < len(svg.points) and head_goto == None:
        head_goto = head.goto(svg.points[currentPointNumber][0], svg.points[currentPointNumber][1])


    pygame.display.flip()

''''
    for x in range(0, len(svg.points)):
        screen.set_at(svg.points[x], (255, 0, 0))

    for x in range(0, len(progress)):
        screen.set_at(progress[x], (0, 255, 0))

    if head.goto(svg.points[currentPointNumber][0], svg.points[currentPointNumber][1]):
        currentPointNumber += 1
    p = head.getPoint()
    screen.set_at(p, (0, 255, 0))
    progress.append(p)



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


'''