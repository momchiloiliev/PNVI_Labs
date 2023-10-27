# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
BLUE      = (  0,   0, 255)
DARKBLUE  = (  0,   0, 155)
DARKGRAY  = ( 40,  40,  40)
ORANGE    = (255, 165,   0)
PINK      = (255, 192, 203)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    global newHead, worm2NewHead, start_time, score, start_button_text, start_button_rect, quit_button_rect, quit_button_text
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    worm2Coords = [{'x': startx, 'y': starty},  #REQUIREMENT No.1
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    direction2 = LEFT   #REQUIREMENT No.1

    # Start the apple in a random place.
    apple = getRandomLocation()
    score = 0
    start_time = pygame.time.get_ticks() #REQUIREMENT No.1

    flash1Position = getRandomLocation()    #REQUIREMENT No.2
    flash1 = Flash(flash1Position, ORANGE)  #REQUIREMENT No.2
    flash2Position = getRandomLocation()    #REQUIREMENT No.2
    flash2 = Flash(flash2Position, PINK)    #REQUIREMENT No.2

    start_button_font = pygame.font.Font('freesansbold.ttf', 20)    #REQUIREMENT No.3
    start_button_text = start_button_font.render('Start from the Beginning', True, WHITE) #REQUIREMENT No.3
    start_button_rect = start_button_text.get_rect() #REQUIREMENT No.3
    start_button_rect.center = (WINDOWWIDTH // 2 - 75, WINDOWHEIGHT // 2 + 200) #REQUIREMENT No.3

    quit_button_font = pygame.font.Font('freesansbold.ttf', 20) #REQUIREMENT No.3
    quit_button_text = quit_button_font.render('Quit', True, WHITE) #REQUIREMENT No.3
    quit_button_rect = quit_button_text.get_rect() #REQUIREMENT No.3
    quit_button_rect.center = (WINDOWWIDTH // 2 + 75, WINDOWHEIGHT // 2 + 200) #REQUIREMENT No.3


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP: #REQUIREMENT No.3
                if start_button_rect.collidepoint(event.pos):    #REQUIREMENT No.3
                    return
                elif quit_button_rect.colidepoint(event.pos):    #REQUIREMENT No.3
                    terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        elapsed_time = pygame.time.get_ticks() - start_time     #REQUIREMENT No.1

        if random.random() < 0.2:   #REQUIREMENT No.1
            direction2 = random.choice([UP, DOWN, LEFT, RIGHT]) #REQUIREMENT No.1
        for wormBody in wormCoords[1:]: #REQUIREMENT No.1
            if wormBody['x'] == worm2Coords[HEAD]['x'] and wormBody['y'] == worm2Coords[HEAD]['y']: #REQUIREMENT No.1
                worm2Coords.insert(0, worm2NewHead) #REQUIREMENT No.1
        for wormBody in worm2Coords[1:]:    #REQUIREMENT No.1
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                wormCoords.insert(0, newHead)   #REQUIREMENT No.1

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            score += 1
            del worm2Coords[-1]
        else:
            del wormCoords[-1] # remove worm's tail segment
            del worm2Coords[-1]

        if elapsed_time > 5000:     #REQUIREMENT No.2
            if flash1 is None or elapsed_time - flash1.start_time > flash1.duration * 1000:
                flash1 = Flash(flash1Position, ORANGE)      #REQUIREMENT No.2
        if elapsed_time > 12000:    #REQUIREMENT No.2
            if flash2 is None or elapsed_time - flash2.start_time > flash2.duration * 1000:
                flash2 = Flash(flash2Position, PINK)    #REQUIREMENT No.2

        if wormCoords[HEAD]['x'] == flash1Position['x'] and wormCoords[HEAD]['y'] == flash1Position['y']:   #REQUIREMENT No.2
            # don't remove worm's tail segment
            flash1Position = getRandomLocation()    #REQUIREMENT No.2
            flash1.color = BGCOLOR
            score += 3  #REQUIREMENT No.2
        if wormCoords[HEAD]['x'] == flash2Position['x'] and wormCoords[HEAD]['y'] == flash2Position['y']:   #REQUIREMENT No.2
            # don't remove worm's tail segment
            flash2Position = getRandomLocation()    #REQUIREMENT No.2
            flash2.color = BGCOLOR
            score += 3  #REQUIREMENT No.2

        # move the worm by adding a segment in the direction it is moving
        newHead = getDirection(direction, wormCoords)
        worm2NewHead = getDirection(direction2, worm2Coords)
        wormCoords.insert(0, newHead)
        worm2Coords.insert(0,worm2NewHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords,GREEN,DARKGREEN)
        if elapsed_time > 20000: #REQUIREMENT No.1
            drawWorm(worm2Coords,BLUE,DARKBLUE)
        if elapsed_time > 5000:  #REQUIREMENT No.2
            flash1.draw()
        if elapsed_time > 7000:  #REQUIREMENT No.2
            flash2.draw()
        drawApple(apple)
        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getDirection(direction, wormCoords):
    if direction == UP:
        return {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
    elif direction == DOWN:
        return {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
    elif direction == LEFT:
        return {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
    elif direction == RIGHT:
        return {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    global start_time, score
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    start_time = pygame.time.get_ticks()
    score = 0

    DISPLAYSURF.blit(start_button_text, start_button_rect) #REQUIREMENT No.3

    DISPLAYSURF.blit(quit_button_text, quit_button_rect) #REQUIREMENT No.3

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords,color1,color2):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color2, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, color1, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

class Flash:    #REQUIREMENT No.2
    def __init__(self,coord,color):
        self.size = CELLSIZE
        self.x = coord['x'] * CELLSIZE
        self.y = coord['y'] * CELLSIZE
        self.start_time = pygame.time.get_ticks()
        self.duration = 5
        self.color = color

    def draw(self): #REQUIREMENT No.2
        elapsed_time = pygame.time.get_ticks() - self.start_time
        # Make the element flash by alternating its color
        if elapsed_time % 1000 < 500:
            pygame.draw.rect(DISPLAYSURF, self.color, (self.x, self.y, self.size, self.size))

class Button:
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y

if __name__ == '__main__':
    main()

