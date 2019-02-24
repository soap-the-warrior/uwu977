#!/usr/bin/env python3
import argparse
import pygame as pg
import random as r
import numpy as np

import blocks
import files

## Command line arguments
parser = argparse.ArgumentParser(description='UWU977: Crazy Hat builds a world!')
parser.add_argument('-v', type=int, default=0,
                    help='verbosity level')
parser.add_argument('-x', '--width', type=int, default=30,
                    dest='width',        ##other useless comment
                    help='world width (tiles)')
parser.add_argument('-y', '--height', type=int, default=10,
                    dest='height',
                    help='world height (tiles)')
args = parser.parse_args()

## ---------- blocks ----------
f=64
# block size on screen
blocks.loadBlocks(f)
pic = pg.transform.scale(pg.image.load("pic.png"),(f,f))
home = pg.transform.scale(pg.image.load("home.png"),(f,f))
##
bgColor = (64,64,64)
# dark gray
## coordinate transformation for the buffer
def tc(x,y):
    return(x*f, y*f)
## coordnate transformation for the actual screen
def screenCoords(x, y):
    return(sx + x*f, sy + y*f)
## ---------- initialize ----------
pg.init()
pg.mixer.init()
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
##
pg.display.set_caption(str(r.randint(0,9000)))
screenBuffer = pg.Surface(size=(4*screenw, 4*screenh))
screenBuffer.fill(bgColor)
# this is the buffer where movement-related drawing is done,
# afterwards it is copied to the screen
do = True
dist = 1
actuallyuselessvariable = 39
up = True
down = True
left = True
right = True
mup = False
mdown = False
mleft = False
mright = False
timer = pg.time.Clock()
lifes = 5
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
bb=1
seehome = 0
player = pg.sprite.Group()
##
s = files.loadWorld()
if s is not None:
    world = s['world']
    homeX = s['home'][0]
    homeY = s['home'][1]
    worldWidth = world.shape[1]
    worldHeight = world.shape[0]
else:
    ## ---------- Build the world ----------
    ## variables
    worldWidth = args.width
    worldHeight = args.height
    groundLevel = 0.5
    # in fraction, from bottom.  0.3 means bottom 30%
    ## sanity check
    worldHeight = min(max(worldHeight, 2), 400)
    worldWidth = min(max(worldWidth, 2), 2000)
    groundLevel = min(max(groundLevel, 0.0), 1.0)
    world = np.zeros((worldHeight, worldWidth), 'int8')
    iGround = int((1 - groundLevel)*worldHeight)
    world[iGround] = 3
    world[iGround+1:] = 5
    ## add ores and such
    brThickness = worldHeight - iGround
    nCoal = np.random.binomial(brThickness*worldWidth, 0.05)
    x = np.random.randint(0, worldWidth, size=nCoal)
    y = np.random.randint(iGround + 1, worldHeight, size=nCoal)
    world[y,x] = 6
    nGold = np.random.binomial(brThickness*worldWidth, 0.02)
    x = np.random.randint(0, worldWidth, size=nGold)
    y = np.random.randint(iGround + 1, worldHeight, size=nGold)
    world[y,x] = 11
    ## where crazy hat has her home:
    homeX = int(worldWidth/2)
    homeY = max(iGround - 1, 0)
## Draw the world
for x in range(world.shape[0]):
    for y in range(world.shape[1]):
        screenBuffer.blit( blocks.blocks[ world[x,y] ], tc(y, x))
## ---------- world-screen coordinate translation ----------
## upper left corner of the world will be drawn at (sx, sy) on screen.
## This will be done when copying the screen buffer on screen
sx = screenw/2 - worldWidth*f/2
sy = screenh/2 - worldHeight*f/2
## ---------- world done ----------

class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x, self.rect.y = screenCoords(x, y)
    def update(self, mup, mdown, mleft, mright):
        global sx, sy, world
        if mup:
            self.y = max(self.y - 1, 0)
        if mdown:
            self.y = min(self.y + 1, worldHeight - 1)
        if mleft:
            self.x = max(self.x - 1, 0)
        if mright:
            self.x = min(self.x + 1, worldWidth - 1)
        if world[self.y,self.x] in blocks.breakable:
            world[self.y,self.x] = blocks.breakto[world[self.y,self.x]]
            screenBuffer.blit( blocks.blocks[blocks.breakto[world[self.y,self.x]]], tc(self.x, self.y))
        sx = screenw/2-hullmyts.getxy()[0]*f
        sy = screenh/2-hullmyts.getxy()[1]*f
        self.rect.x, self.rect.y = screenCoords(self.x, self.y)
    def getxy(self):
        return(self.x,self.y)
def reset():
    global hullmyts
    lifes = 5
    player.empty()
    hullmyts = Player(homeX, homeY)
    player.add(hullmyts)
def build(x,y):
    global bb
    if x>=0 and y>=0 and x<worldWidth and y<worldHeight:
        world[y,x] = bb
        screenBuffer.blit( blocks.blocks[bb], tc(x, y))
# initialize player        
reset()
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mup = True  #useless comment
            elif event.key == pg.K_DOWN:
                mdown = True
            elif event.key == pg.K_LEFT:
                mleft = True
            elif event.key == pg.K_RIGHT:
                mright = True
            elif event.key == pg.K_a:
                build(hullmyts.getxy()[0]-1,hullmyts.getxy()[1])
            elif event.key == pg.K_s:
                build(hullmyts.getxy()[0],hullmyts.getxy()[1]+1)
            elif event.key == pg.K_d:
                build(hullmyts.getxy()[0]+1,hullmyts.getxy()[1])
            elif event.key == pg.K_w:
                build(hullmyts.getxy()[0],hullmyts.getxy()[1]-1)
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                reset()
            elif event.key == pg.K_h:
                homeX = hullmyts.getxy()[0]
                homeY = hullmyts.getxy()[1]
            elif event.key == pg.K_RIGHTBRACKET and bb < 11:
                bb += 1
            elif event.key == pg.K_LEFTBRACKET and bb > 1:
                bb -= 1
            elif event.key == pg.K_x:
                seehome = 1-seehome
            elif event.key == pg.K_z:
                files.saveWorld(world, (homeX, homeY))
            elif event.key == pg.K_c:
                xy=hullmyts.getxy()
                world[xy[1],xy[0]] = 0
                screenBuffer.blit( blocks.blocks[blocks.SKY], tc(xy[0],xy[1]))
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
                    pd = "PAUSED"
                    ptext = dfont.render(pd, True, (127,127,127))
                    ptext_rect = ptext.get_rect()
                    ptext_rect.centerx = screen.get_rect().centerx
                    ptext_rect.y = 50
                    screen.blit(ptext,ptext_rect)
                    screen.blit(text,text_rect)
                    pg.display.update()
    if lifes == 0:
        uded = "GAME OVER"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
        gameover = True
    while gameover:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    gameover = False
                    reset()
                    ## ---------- screen udpate ----------
    screen.fill(bgColor)
    screen.blit(screenBuffer, (sx,sy))
    if seehome == 1:
        screen.blit(home, screenCoords(homeX,homeY))
    score = ("Block: " + blocks.bn[bb])
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    pg.display.update()
    ##
    mup = False
    mdown = False
    mleft = False
    mright = False
    timer.tick(60)

pg.quit()
