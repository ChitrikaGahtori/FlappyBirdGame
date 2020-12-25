import random  #For generating random numbers
import sys  #We will use sys.exit to exit the program
import pygame
from pygame.locals import * #Basic pygame imports

# Global Variables for the game
FPS = 32 #Frames Per Second - the numbers of frames displayed on the screen each second
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))  #Initialize a window or screen for display
GROUNDY = SCREENHEIGHT * 0.8
# image , sound dicts
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\bird.png'
BACKGROUND = 'D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\background.png'
PIPE = 'D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                return
            
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                # display.update() allows to update a portion of the screen, instead of the entire area of the screen. 
                # Passing no arguments, updates the entire display
                FPSCLOCK.tick(FPS)


def mainGame():
    
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)

    basex = 0
    
    # Create 2 pipes for blitting on the screen
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    # my List of upper pipes
    upperpipes = [
        {'x' : SCREENWIDTH + 200 , 'y' : newpipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 + SCREENWIDTH/2 , 'y' : newpipe2[0]['y']}
    ]

    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newpipe2[1]['y']},
    ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVely = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        crashTest = isCollide(playerx, playery, upperpipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return   

        #check for score
        PlayerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidpos <= PlayerMidPos < pipeMidpos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
          
        if playerVely <playerMaxVelY and not playerFlapped:
            playerVely += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)    

        # move pipes to the left
        for upperpipe , lowerpipe in zip(upperpipes,lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        # Add new pipe when first pipe is about to touch left of screen
        if 0 < upperpipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe , lowerpipe in zip(upperpipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'] , upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'] , lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperpipes, lowerPipes):
    
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
        
    return False
    
                
def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][1].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x': pipeX, 'y': -y1},#upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe
    

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() #Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird Game")

    # Game images
    GAME_SPRITES['numbers'] = (  # use 'convert_alpha()' on images with alpha channel, and 'convert()' on images without alpha channel    
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\0.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\1.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\2.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\3.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\4.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\5.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\6.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\7.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\8.png').convert_alpha(),
        pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\9.png').convert_alpha(),
        # For alpha transparency, like in . png images, use the convert_alpha() method after loading so that the image has per pixel transparency
    )

    GAME_SPRITES['message'] = pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('D:\\Python Course\\Flappy Bird Game\\gallery\\sprites\\base.png').convert_alpha()
    GAME_SPRITES['pipe'] = ( pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('D:\\Python Course\\Flappy Bird Game\\gallery\\audio\\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('D:\\Python Course\\Flappy Bird Game\\gallery\\audio\\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('D:\\Python Course\\Flappy Bird Game\\gallery\\audio\\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('D:\\Python Course\\Flappy Bird Game\\gallery\\audio\\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('D:\\Python Course\\Flappy Bird Game\\gallery\\audio\\wing.wav')

    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 

