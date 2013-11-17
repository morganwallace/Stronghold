import os.path
import math
import os
import sys
import pygame
import threading
import time
from sys import exit as sysexit
from pygame.locals import *
import pickle

scrwid = 800 #Screen width.
scrhei = 600 #Screen height. Uses 4:3 ratio.
squsize = 30
openbuttoninfo = []
opentowerinfo = []
class Map():
    def __init__(self):
        self.current = 1
        self.pathrectlist = None
        self.pointmovelist = None
        self.endrect = None
        self.mapdict = dict()
        self.pointmovelists = list()
        self.pathrectlists = list()
        self.wavesSinceLoss = 0
        self.rollNext = 0
        self.hasStarted = 0
        self.hasEnded = 0
        self.nextWaveRect = None
        self.currentCompleted = 0
    def getmovelist(self):
        movelists = list()
        movelistnum = -1
        f = open(os.path.join('mapfiles',str(self.current),'movefile.txt'))
        line = f.readline().strip().split(',')
        self.basepoint = (int(int(line[0])*20.0/squsize),int(int(line[1])*20.0/squsize))

        for line in f.readlines():
            line = line.strip().split(',')
            if int(line[0])<0 or int(line[1])<0 or int(line[0])>(scrwid) or int(line[1])>(scrhei/squsize):
                movelists.append(list())
                movelistnum+=1
            movelists[movelistnum].append((int(int(line[0])*20.0/squsize),int(int(line[1])*20.0/squsize)))

        for movelist in movelists:
            movelist.append(self.basepoint)
            pointmovelist = list([(point[0]*squsize+int(squsize/2.0),point[1]*squsize+int(squsize/2.0)) for point in movelist])
            pointmovelist.append((scrwid+squsize,scrhei+squsize))
            pathrectlist = list([pygame.Rect(pointmovelist[ind],(pointmovelist[ind+1][0]-pointmovelist[ind][0],pointmovelist[ind+1][1]-pointmovelist[ind][1])) for ind in range(len(pointmovelist)-2)])
            for rec in pathrectlist:
                rec.normalize()
            self.pointmovelists.append(pointmovelist)
            self.pathrectlists.append(pathrectlist)
            print "Move List Generated"
    def getmapproperties(self):
        self.mapdict = dict()
        f = open(os.path.join('mapfiles',str(self.current),'mapproperties.txt'))
        currentwave = 0
        self.enemylevel = 1
        for line in f.readlines():
            if line[0]!='*':
                if line.find("wave")>=0:
                    line = line.strip().split(':')
                    currentwave=line[0]
                    self.mapdict[currentwave] = list()
                else:
                    linepro = line.strip().split(',')
                    numrun = 0
                    thisdict = dict()
                    thisdict["img"] = 1
                    thisdict["cost"] = 1
                    thisdict["hp"] = 10
                    thisdict["speed"] = 1.0
                    thisdict["attack"] = 0
                    thisdict["damage"] = 0
                    thisdict["armor"] = 0
                    thisdict["timer"] = 1
                    thisdict["evasion"] = 0
                    thisdict["damagereduction"] = 1
                    thisdict["leveladj"] = 0
                    for spl in linepro:
                        k,v = spl.split('=')
                        if k == "num":
                            numrun = int(v)
                        elif k == "enemylevel":
                            self.enemylevel = int(v)
                        thisdict[k] = float(v)
                    for i in range(numrun):
                        self.mapdict[currentwave].append(thisdict)
        print "Map Properties Created"
    def backgroundGen(self,bgsize):
        print "Generating Background"

        dp = pygame.transform.smoothscale(imgLoad(os.path.join('backgroundimgs','roadsquare.jpg')),(squsize,squsize))

        background = imgLoad(os.path.join('mapfiles',str(self.current),'background.jpg'))
        for pathnum in range(len(self.pointmovelists)):
            pathrectlist = self.pathrectlists[pathnum]
            pointmovelist = self.pointmovelists[pathnum]
            for rec in [pygame.Rect(x,y,squsize,squsize) for x in range(0,scrwid,squsize) for y in range(0,scrhei,squsize)]:
                if any([rec.collidepoint(point) for point in pointmovelist]):
                    background.blit(dp,rec)
                elif len(list([rect for rect in pathrectlist if rect.colliderect(rec)]))==2:
                    background.blit(dp,rec)
                else:
                    collideindex = rec.collidelist(pathrectlist)
                    if collideindex!=-1:
                        background.blit(dp,rec.move(0,0))
        self.baseimg = imgLoad(os.path.join('backgroundimgs','base.png'))
        self.baserect = self.baseimg.get_rect(center=(self.basepoint[0]*squsize+(0.5*squsize),self.basepoint[1]*squsize+(0.5*squsize)))
        print "Background Generated"
        return background
    def loadMap(self,bgsize,mapname):
        self.xpbar = pygame.Rect(300,8,350,22)
        self.current = mapname
        self.iconhold = (None,0)
        if os.path.exists(os.path.join('mapfiles',str(self.current))):
            self.getmovelist()
            self.getmapproperties()
            return self.backgroundGen(bgsize)
        else:
            print "You Won!!!"
            sysexit(1)

mapvar = Map()

class Player():
    def __init__(self):
        pass
    def start(self):
        self.name = "player"

        self.spareRunes = list()

        self.load()

        self.currentChain = 0.0
        self.health = 10
        self.money = 30

        self.modDict = dict()

        try:
            self.modDict['tower']['ImageName'] = self.loadarray['ImageName'][0]
        except:
            pass

        self.modDict['towerSellMod'] = 0

        self.modDict['chainMax'] = 0.50
    def load(self):
        try:
            infile = open(os.path.join(self.name+".txt"),"r")
            self.mapscompleted = list()
            for line in infile.readlines():
                if len(line.strip())>0:
                    self.mapscompleted.append(line.strip())
            infile.close()
        except:
            self.mapscompleted = list()

        towernum = 1+sum([1 for map in self.mapscompleted if "Basic" in map])

        import localclasses
        localclasses.Tower.loadTowers()

        for i in range(towernum-len(towerlist)):
            localclasses.Tower()

        import pickle
        try:
            for filename in os.listdir(os.path.join(self.name)):
                if "skilllist" in filename:
                    nsglist = pickle.load(open(os.path.join(self.name,filename),"r"))
                    for sg in nsglist:
                        self.spareRunes.append(sg)
        except:
            pass
    def addScreen(self,screen,clock):
        self.screen = screen
        self.clock = clock
    def save(self):
        import localclasses
        localclasses.Tower.saveTowers()

        if mapvar.currentCompleted and mapvar.current not in self.mapscompleted:
            self.mapscompleted.append(mapvar.current)
        outfile = open(os.path.join(self.name+".txt"),"w")
        for map in self.mapscompleted:
            outfile.write(map+"\n")
        outfile.close()

        pickle.dump(self.spareRunes,open(os.path.join(player.name,"skilllist.obj"),"w"))
        del self.spareRunes[:]
    def findMaxXP(self):
        self.maxXP = 10
    def gainXP(self,amt):
        for tower in towerlist:
            if tower.outyet:
                tower.gainXP(amt*(1+self.currentChain))
    def die(self):
        print "You have died!"
        sysexit(0)

enemylist = list()
towerlist = list()
bulletlist = list()
iconlist = list()
menulist = list()
explosions = list()
senderlist = list()
timerlist = list()

def imgLoad(img):
    file = os.path.join(img)
    image = pygame.image.load(file)
    image.convert_alpha()
    return image

player = Player()

def distance(first,second):
    return (math.sqrt((second.centerx-first.centerx)**2+(second.centery-first.centery)**2))

class SlowTimer():
    def __init__(self,percent,time):
        self.amt = percent
        self.time = time

class PoisonTimer(threading.Thread):
    def __init__(self,enemy,damage,seconds):
        threading.Thread.__init__(self)
        self.runtime = seconds
        self.dam = damage
        self.target = enemy
        enemy.poisontimer=self
        self.kill = False
    def run(self):
        sec = self.runtime*1.0
        while(sec>0):
            sec-=0.1
            time.sleep(0.1)
            if self.target.poisontimer == self or self.kill == True:
                if self.target.health>0:
                    self.target.health-=self.dam
                    if self.target.health<=0:
                        self.target.die()
                        return
                else:
                    return
            else:
                return
        if self.target.poisontimer == self:
            self.target.poisontimer = None

EnemyImageArray = list()
def genEnemyImageArray():
    for type in ["none","enemy","Speedy","Healthy","Armor","Fire","Cold","Shock","Acid"]:
        ia = list()
        try:enemyimage = imgLoad(os.path.join('enemyimgs',type+'.png'))
        except:enemyimage = imgLoad(os.path.join('enemyimgs','enemy.png'))
        ia.append(enemyimage)
        ia.append(pygame.transform.rotate(enemyimage,90))
        ia.append(pygame.transform.flip(enemyimage,True,False))
        ia.append(pygame.transform.rotate(enemyimage,-90))
        EnemyImageArray.append(ia)

