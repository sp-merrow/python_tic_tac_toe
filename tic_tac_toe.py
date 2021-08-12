import pygame
pygame.init()

from pygame.locals import(
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONUP,
    K_RETURN,
    K_BACKSPACE,

)

screen = pygame.display.set_mode([500, 600])
screenWidth, screenHeight = 500, 600
pygame.display.set_caption('Tic Tac Toe')
boardImage = pygame.transform.scale(pygame.image.load('board.png'), (500, 500))
xImg = pygame.transform.scale(pygame.image.load('x.png'), ( round(screenWidth/3), round(screenWidth/3) ) )
oImg = pygame.transform.scale(pygame.image.load('o.png'), ( round(screenWidth/3), round(screenWidth/3) ) )
baseFont = pygame.font.Font(None, 32)

allZones = pygame.sprite.Group()

class Zone(pygame.sprite.Sprite):
    def __init__(self, visualObj, coords):
        self.visualObj = visualObj
        self.coords = coords
        self.rect = self.visualObj.get_rect()
        pygame.sprite.Sprite.__init__(self)

clickZones = []
x, y = 0, 0
for i in range(9):
    sizeFract = 500/3
    if i == 0:
        pass
    elif i % 3 == 0:
        y += sizeFract
        x = 0
    else:
        x += sizeFract
    newSurface = pygame.Surface( (sizeFract, sizeFract) )
    newSurface.fill((255, 255, 255))
    newZone = Zone(newSurface, (round(x), round(y)))
    clickZones.append(newZone)

allZones.add(clickZones)

running = True
players = []
text = baseFont.render('Enter name for player 1:', True, (0, 0, 0), None)
textRect = text.get_rect()
textRect.center = (screenWidth/2, 200)
inputRect = pygame.Rect((screenWidth/2), (screenHeight/2), (screenWidth/1.5), 40)
inputRect.center = ((screenWidth/2), (screenHeight/2))
inputText = 'Click to start typing'
inactiveColor = (100, 100, 100)
activeColor = (202, 202, 202)
color = inactiveColor
active = False
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
while running:
    for event in pygame.event.get():
        if inputRect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if inputRect.collidepoint(event.pos):
                active = not active
                inputText = ''
            else:
                active = False
            color = activeColor if active else inactiveColor
        if event.type == KEYDOWN and active:
            if event.key == K_RETURN:
                if inputText and inputText != 'Name cannot be blank!':
                    players.append(inputText)
                    inputText = ''
                    text = baseFont.render('Enter name for player 2:', True, (0, 0, 0), None)
                else:
                    inputText = 'Name cannot be blank!'
            elif event.key == K_BACKSPACE:
                inputText = inputText[:-1]
            else:
                if inputText == 'Name cannot be blank!':
                    inputText = ''
                inputText += event.unicode
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()

    screen.fill((255, 255, 255))
    inputSurf = baseFont.render(inputText, True, (0, 0, 0))
    screen.blit(inputSurf, (inputRect.x+5, inputRect.y+5))
    pygame.draw.rect(screen, color, inputRect, 2)
    screen.blit(text, textRect)

    pygame.display.flip()

    if len(players) == 2:
        running = False


running = True
xLocs = []
oLocs = []
count = 1

def hasWon(locations):
    for i in locations:
        if i in {0, 3, 6}:
            if all(x in locations for x in range(i, i+3)):
                return True
        if i in {0, 1, 2}:
            if all(x in locations for x in range(i, i+7, 3)):
                return True
        if i == 0:
            if all(x in locations for x in range(0, 9, 4)):
                return True
        if i == 2:
            if all(x in locations for x in range(2, 7, 2)):
                return True
    return False

def anyWon():
    if hasWon(xLocs):
        return f'{players[0]} wins!'
    if hasWon(oLocs):
        return f'{players[1]} wins!'
    return False

collisionTesters = {}
for c, i in enumerate(clickZones):
    collisionTesters[c] = pygame.Rect(i.coords[0], i.coords[1], i.visualObj.get_width(), i.visualObj.get_height())

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

while running:
    clickedBox = []
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONUP:
            for c, i in enumerate(clickZones):
                if collisionTesters[c].collidepoint(event.pos) and i[0] not in {xImg, oImg}:
                    if count % 2 == 0:
                        clickedBox.append(c)
                        clickedBox.append(oImg)
                        oLocs.append(c)
                        count += 1
                    else:
                        clickedBox.append(c)
                        clickedBox.append(xImg)
                        xLocs.append(c)
                        count += 1
        if allZones.collidepoint(pygame.mouse.get_pos()): #///////////////////////////////////////////////// LEFT OFF HERE
            print('collision detected')

    if count % 2 == 0:
        text = baseFont.render(f"{players[1]}'s turn", True, (0, 0, 0), None)
    else:
        text = baseFont.render(f"{players[0]}'s turn", True, (0, 0, 0), None)
    textRect = text.get_rect()
    textRect.center = (screenWidth/2, 550)

    if clickedBox:
        clickZones[clickedBox[0]].visualObj = clickedBox[1]
    screen.fill((255, 255, 255))
    for s in clickZones:
        screen.blit(s.visualObj, s.coords) 
    screen.blit(boardImage, (0,0))
    screen.blit(text, textRect)

    pygame.display.flip()
    if count == 10:
        running = False
    if anyWon():
        running = False

pygame.quit()