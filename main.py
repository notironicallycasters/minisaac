import pyxel
from math import *
from random import randint,choice

# Taille de la fenetre 128x128 pixels
scale = 20
pyxel.init(16*scale, 9*scale, title="MinIsaac",quit_key=pyxel.KEY_ESCAPE)
pyxel.fullscreen(True)

# Position et velocité du joueur
posX = 16*scale/2
posY = 9*scale/2
speedX = 0
speedY = 0

#Info projectiles
projX = []
projY = []
projR = []
projT = []
pTimer= 0

#Info ennemis
foeX = []
foeY = []
foeT = []
foeSpeed = 20

#Stats
speed = 25 #Vitesse joueur
accel = 50 #Acceleration
pSpeed = 1 #Vitesse projectiles
pTick = 10 #Vitesse de tir
pRange = 72 #Portée
hp = 6 #Vie

inv = False #Invinsibilité
invTimer = 0
rd = pi/180
title = True

wave = 1
prev = 3
ennemis = 2
wavescore = 0

pyxel.load("PYXEL_RESOURCE_FILE.pyxres")
pyxel.playm(0,loop=True)

#Mouvement avec accélération
def move(x, y):
    global speedX,speedY,speed

    if pyxel.btn(pyxel.KEY_D):
        speedX += speed/accel
        if speedX > 2:
            speedX = 2
        if speedX < 0:
             speedX = -speedX
    elif pyxel.btn(pyxel.KEY_A):
        speedX -= speed/accel
        if speedX > 0:
             speedX = -speedX
        if speedX < -2:
            speedX = -2
    else: 
        if speedX > 0:
              speedX -= speed/60
        elif speedX < 0:
              speedX += speed/accel
        if abs(speedX) < 2*speed/accel:
             speedX = 0

    if pyxel.btn(pyxel.KEY_S):
        speedY += speed/accel
        if speedY < 0:
             speedY = -speedY
        if speedY > 2:
            speedY = 2
    elif pyxel.btn(pyxel.KEY_W):
        speedY -= speed/accel
        if speedY > 0:
             speedY = -speedY
        if speedY < -2:
            speedY = -2
    else:
        if speedY > 0:
              speedY -= speed/60
        elif speedY < 0:
              speedY += speed/accel
        if abs(speedY) < 2*speed/accel:
             speedY = 0
    
    #Normalisation
    magnitude = (float(abs(speedX)>0) + float(abs(speedY)>0))**0.5
    magnitude += float(magnitude==0)
    if (x < 120) or (x > 0):
            x = x + speedX / magnitude
    if (y < 120) or (y > 0):
            y = y + speedY / magnitude

    return x, y

def projUpdate():
    #Ignorer si 0 projectiles
    if projX == []:
        return
    
    #Déplacement projectiles
    for i in range(len(projX)):
        if i >= len(projX):
             return
        if abs(projR[i]) == 1:
            projX[i] += projR[i]*pSpeed
        if abs(projR[i]) == 2:
            projY[i] += (projR[i]/2)*pSpeed
        projT[i] += 1
        if projT[i] > pRange or (abs(projY[0]) >= 9*scale or abs(projX[0]) >= 16*scale):
            projX.pop(i)
            projY.pop(i)
            projR.pop(i)
            projT.pop(i)
    
def foeUpdate():
    #Ignorer si 0 ennemis
    if foeX == []:
        return

    #Déplacement vers le joueur
    for i in range(len(foeX)):
            if dist((foeX[i],foeY[i]),(posX,posY)) > 3:
                invDist = 1/dist((foeX[i],foeY[i]),(posX,posY))
                foeX[i] += (posX-foeX[i])*0.1*foeSpeed*invDist +(randint(-1,1)*foeT[i]==1)
                foeY[i] += (posY-foeY[i])*0.1*foeSpeed*invDist +(randint(-1,1)*foeT[i]==1)

def label(text:str,x,y):
    font = 12
    for i in range(len(text)):
        o = ord(text[i])-32
        u = o%16
        v = o//16
        pyxel.blt(x+i*font,y,1,font*u,font*v,font,font,9)

def collision():
    global hp,inv,wave,wavescore,prev,ennemis
    #Projectiles/Ennemis
    for i in range(len(foeX)):
        for j in range(len(projX)):
             if dist((foeX[i],foeY[i]),(projX[j],projY[j])) < 4:
                projX.pop(j)
                projY.pop(j)
                projR.pop(j)
                projT.pop(j)
                foeX.pop(i)
                foeY.pop(i)
                foeT.pop(i)
                wavescore +=1
                if wavescore == ennemis:
                    t = ennemis
                    ennemis = int(round((prev + ennemis)**0.9))
                    prev = t
                    pyxel.play(2,13)
                    wave += 1
                    wavescore = 0
                return
        
                
    #Joueur/Ennemis:
    if inv:
        return
    for i in range(len(foeX)):
        if dist((foeX[i],foeY[i]),(posX,posY)) < 4:
            pyxel.play(3,11)
            hp -= 1
            if hp == 0:
                pyxel.reset()
            inv = True            
                 

def update():
    global posX, posY, pTimer, pTick,title,inv,invTimer

    #Timer des projectiles
    pTimer+= 1
    if pTimer> pTick:
        pTimer= 0

    if inv:
        invTimer+= 1
        if invTimer > 60:
            invTimer= 0
            inv = False

    if title:
        if pyxel.btn(pyxel.KEY_SPACE):
             title = False
             pyxel.playm(1,loop=True)
        return

    #Màj projectiles/ennemi
    projUpdate()
    foeUpdate()
    collision()

    #Déplacement
    posX, posY = move(posX, posY)

    #Lancer projectiles
    if  pTimer== 0:
        if pyxel.btn(pyxel.KEY_LEFT):
            projX.append((posX-2))
            projY.append(posY-2)
            projR.append(-1)
            projT.append(0)
            pyxel.play(2,10)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            projX.append((posX-2))
            projY.append(posY-2)
            projR.append(1)
            projT.append(0)
            pyxel.play(2,10)
        elif pyxel.btn(pyxel.KEY_UP):
            projX.append((posX-2))
            projY.append(posY-2)
            projR.append(-2)
            projT.append(0)
            pyxel.play(2,10)
        elif pyxel.btn(pyxel.KEY_DOWN):
            projX.append((posX-2))
            projY.append(posY-2)
            projR.append(2)
            projT.append(0)
            pyxel.play(2,10)
        

    #Apparition ennemis:
    if randint(0,64) == 0 and len(foeX) < ennemis:
        if randint(0,1) == 0:
            foeX.append(16*scale-(16*scale*randint(0,1)))
            foeY.append(randint(0,9*scale))
        else:
            foeX.append(randint(0,16*scale))
            foeY.append(9*scale-(9*scale*randint(0,1)))
        foeT.append(randint(0,1))


def draw():

    #Écran titre
    if title:
        pyxel.cls(7)
        pyxel.blt((16*scale/2)-128,(9*scale/2)-72,0,0,32,256,48,0)
        pyxel.blt((16*scale/2)-48,(9*scale/2)-16,0,0+(96*int(pTimer<=5)),80,96,96,0)
        return
        

    #Fond marron
    pyxel.cls(9)
    pyxel.blt((16*scale/2)-64,(9*scale/2)-48,0,0,176,128,96,0)
    

    #Joueur 16x16
    if invTimer % 2 == 0:
        pyxel.blt(posX-8,posY-8,0,0,0,16,16,9)
    #pyxel.rect(16*scale/2,9*scale/2,1,1,8)

    #Projectile
    for i in range(len(projX)):
        #pyxel.rect(projX[i], projY[i], 4, 4, 6)
        pyxel.blt(projX[i], projY[i],0,70,6,4,4,9)
    for i in range(len(foeX)):
        pyxel.blt(foeX[i]-8,foeY[i]-8,0,16*foeT[i],16,16,16,9)

    #HUD
    tempHp = hp
    for i in range(3):
        if tempHp >= 2:
            pyxel.blt((16*scale/2)-144+(i*20),(9*scale/2)-80,0,16,0,16,16,9)
        elif tempHp > 0:
            pyxel.blt((16*scale/2)-144+(i*20),(9*scale/2)-80,0,32,0,16,16,9)
        elif tempHp <= 0:
            pyxel.blt((16*scale/2)-144+(i*20),(9*scale/2)-80,0,48,0,16,16,9)
        tempHp -= 2
    label(f"Wave:{wave}",(16*scale/2)-144,(9*scale/2)-64)
    label(f"Remain:{ennemis-wavescore}",(16*scale/2)-144,(9*scale/2)-48)
    

pyxel.run(update, draw)