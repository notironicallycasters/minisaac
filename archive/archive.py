import pyxel
from math import *
from random import randint

# Taille de la fenetre 128x128 pixels
pyxel.init(128, 128, title="Nuit du c0de")

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
posX = 60
posY = 110
speed = 10
speedX = 0
speedY = 0

projX = []
projY = []
projR = []
projTick = 0

rd = pi/180

print(cos(60))

def move(x, y):
    global speedX,speedY,speed

    if pyxel.btn(pyxel.KEY_D):
        speedX += speed/30
        if speedX > 2:
            speedX = 2
        if speedX < 0:
             speedX = -speedX
    elif pyxel.btn(pyxel.KEY_A):
        speedX -= speed/30
        if speedX > 0:
             speedX = -speedX
        if speedX < -2:
            speedX = -2
    else:
        if speedX > 0:
              speedX -= speed/60
        elif speedX < 0:
              speedX += speed/30
        if abs(speedX) < 2*speed/30:
             speedX = 0

    if pyxel.btn(pyxel.KEY_S):
        speedY += speed/30
        if speedY < 0:
             speedY = -speedY
        if speedY > 2:
            speedY = 2
    elif pyxel.btn(pyxel.KEY_W):
        speedY -= speed/30
        if speedY > 0:
             speedY = -speedY
        if speedY < -2:
            speedY = -2
    else:
        if speedY > 0:
              speedY -= speed/60
        elif speedY < 0:
              speedY += speed/30
        if abs(speedY) < 2*speed/30:
             speedY = 0
    
    magnitude = (float(abs(speedX)>0) + float(abs(speedY)>0))**0.5
    magnitude += float(magnitude==0)
    if (x < 120) or (x > 0):
            x = x + speedX / magnitude
    if (y < 120) or (y > 0):
            y = y + speedY / magnitude

    return x, y

def projDraw():
    if projX == []:
        return
    
    if abs(projY[0]) >= 128 or abs(projX[0]) >= 128:
            projX.pop(0)
            projY.pop(0)
    
    for i in range(len(projX)):
        pyxel.rect(projX[i], projY[i], 2, 2, 6)
        projX[i] += sin(projR[i])
        projY[i] += cos(projR[i])


def update():
    global posX, posY, projTick

    projTick += 1
    if projTick > 5:
        projTick = 0

    # mise à jour de la position du vaisseau
    posX, posY = move(posX, posY)

    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and projTick == 0:
        projX.append((posX+3))
        projY.append(posY+3)
        projR.append(-atan2((pyxel.mouse_y-posY),(pyxel.mouse_x-posX))+(90*rd))


def draw():
    pyxel.cls(9)

    # vaisseau (carre 8x8)
    pyxel.rect(posX, posY, 9, 9, 15)

    pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 3, 3, 7)

    projDraw()
    


pyxel.run(update, draw)