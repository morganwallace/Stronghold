import pygame
import os
import sys
from pygame.locals import *
from localdefs import *
import random
import math
import TowerUpgrades
import pickle
import Runes

class Enemy():
    def __init__(self,wavedict,totnum):
        self.imgindex = int(wavedict["img"])
        self.image = EnemyImageArray[self.imgindex][0]
        self.curnode = 0
        self.distance = 0
        self.movelist = mapvar.pointmovelists[0][:]
        self.rect = self.image.get_rect(center=(self.movelist[self.curnode]))
        enemylist.append(self)
        self.cost = wavedict["cost"]
        self.maxhealth = self.health = wavedict["hp"]
        self.speed = wavedict["speed"]
        self.attackBonus = wavedict["attack"]
        self.damage = wavedict["damage"]
        self.leveladj = wavedict["leveladj"]
        self.starthealth = self.health
        self.route = 1
        self.xp = 1.0/int(totnum)
        self.slowtimers = list()
        self.holdcentx = self.rect.centerx*1.0
        self.holdcenty = self.rect.centery*1.0
        self.poisontimer = None
        self.armor = wavedict["armor"]
        self.currentTargetTimer = self.startTargetTimer = 2.5
        self.findrangesq = (2*squsize)**2
        self.hitrangesq = self.findrangesq/2.0
        self.evasion = wavedict["evasion"]
        self.damagereduction = wavedict["damagereduction"]
        self.towertarget = None
        self.findTarget()
    def takeTurn(self,frametime,screen):
        self.move(frametime)
        if self.damage:
            self.attack(frametime,screen)
    def attack(self,frametime,screen):
        self.currentTargetTimer -= frametime
        if self.currentTargetTimer<=0:
            random.shuffle(towerlist)
            for tower in towerlist:
                if tower.outyet:
                    if (self.rect.centerx-tower.rect.centerx)**2+(self.rect.centery-tower.rect.centery)**2<=self.hitrangesq:
                        tower.getAttack((random.randint(1,2000)*1.0/100.0)+self.attackBonus,self.damage)
                        self.currentTargetTimer=self.startTargetTimer
                        pygame.draw.line(screen,(255,0,0),self.rect.center,tower.rect.center)
                        return
    def findCloseTower(self):
        for tower in towerlist:
            if tower.outyet and tower.hp>0 and tower.enemytarget == None and (self.rect.centerx-tower.rect.centerx)**2+(self.rect.centery-tower.rect.centery)**2<=self.findrangesq:
                return tower
        return None
    def findTarget(self):
        if self.damage:
            self.towertarget = self.findCloseTower()
        if self.towertarget:
            self.towertarget.enemytarget = self
            targetrad = math.atan2(self.towertarget.rect.centery-self.rect.centery, self.towertarget.rect.centerx-self.rect.centerx)
        else:
            defl = (0 if random.random() >= 0.75 else random.uniform(-1.0/8.0*math.pi,1.0/8.0*math.pi))
            targetrad = math.atan2(self.movelist[self.curnode+1][1]-self.rect.centery, self.movelist[self.curnode+1][0]-self.rect.centerx)+defl
        dis = 40
        self.target = (self.rect.centerx+math.cos(targetrad)*dis,self.rect.centery+math.sin(targetrad)*dis)
        self.image = pygame.transform.rotozoom(EnemyImageArray[self.imgindex][0],targetrad*-180/math.pi,1)
#        if targetrad >= -1*math.pi/4.0 and targetrad <= math.pi/4.0:
#            self.image = EnemyImageArray[self.imgindex][0]
#        elif targetrad >= math.pi/4.0 and targetrad <= 3*math.pi/4.0:
#            self.image = EnemyImageArray[self.imgindex][3]
#        elif targetrad >= 3*math.pi/4.0 or targetrad <= -3*math.pi/4.0:
#            self.image = EnemyImageArray[self.imgindex][2]
#        else:
#            self.image = EnemyImageArray[self.imgindex][1]
    def move(self,frametime):
        moveamt = frametime/1.6*self.speed
        for st in self.slowtimers[:]:
            st.time -= frametime
            if st.time<=0:
                self.slowtimers.remove(st)
        if self.slowtimers:
            moveamt*=(1-min(self.slowtimers,key=lambda x:x.amt).amt)
        for i in range(int(30)):
            if mapvar.baserect.colliderect(self.rect):
                enemylist.remove(self)
                player.health -= 1
                if player.health<=0:
                    player.die()
                mapvar.wavesSinceLoss = 0
                return
            elif self.rect.collidepoint(self.movelist[self.curnode+1]):
                self.curnode+=1
                self.findTarget()
            elif self.rect.collidepoint(self.target):
                if not self.towertarget or self.towertarget.hp<=0:
                    self.findTarget()
            else:
                self.distance += moveamt
                xdiff = self.holdcentx - self.target[0]
                ydiff = self.holdcenty - self.target[1]
                self.holdcentx += moveamt*xdiff**2/(xdiff**2+ydiff**2)*(1 if xdiff<0 else -1)
                self.holdcenty += moveamt*ydiff**2/(xdiff**2+ydiff**2)*(1 if ydiff<0 else -1)
                self.rect.centerx = self.holdcentx
                self.rect.centery = self.holdcenty
    def checkHealth(self,tower):
        if self.health<=0:
            self.die(tower)
    def die(self,tower):
        if self.towertarget:
            self.towertarget.enemytarget = None
        explosions.append((self.rect,0.35))
        if self in enemylist:
            enemylist.remove(self)
        player.money+=(self.cost)
        player.gainXP(self.xp)
        player.currentChain = min(player.modDict['chainMax'],player.currentChain+0.01)
        Runes.Rune.reward(self,tower)
    def getDamage(self,tower,amt):
        self.health -= max(0,amt-self.damagereduction) if (random.random() >= self.evasion) else 0
        self.checkHealth(tower)

class Icon():
    def __init__(self,tower):
        self.base = "Tower"
        self.tower = tower
        iconlist.append(self)
        self.img = pygame.transform.smoothscale(self.tower.image,(20,20))
        self.otherimg = self.img.copy()
        self.otherimg.fill((100,100,100,100))
        self.rect = self.img.get_rect(left=len(iconlist)*(25)-20,centery=scrhei-self.img.get_height()+5)
    def switchImg(self):
        t = self.img
        self.img = self.otherimg
        self.otherimg = t

class Tower():
    def __init__(self):
        self.tempimage = pygame.transform.smoothscale(imgLoad(os.path.join('towerimgs','Fighter.png')),(squsize,squsize))
        self.image = self.tempimage.copy()
        self.image.fill((255,255,255,50))
        self.image.blit(self.tempimage,(0,0))
        self.cost = 25
        self.targetTimer = 0
        self.icon = Icon(self)
        self.outyet = False
        towerlist.append(self)
        self.upgrades = list()
        self.maxhp = 10
        self.ac = 10
        self.baserange = 2
        self.healthRegeneration = 1.0
        self.curXP = 0
        self.maxXP = 10
        self.curLV = 0
        self.totLV = 0
        self.phyDamIncrease = 0
        self.damIncrease = 0
        self.phyDamBonus = 0
        self.damBonus = 0
        self.speedIncrease = 0
        self.toolBarInfo = {}
        self.runes = {"Alpha":Runes.SingleAttack(self),"Beta":None}
        TowerUpgrades.StartingPoint.apply(self)
    def runeFind(self):
        return 0
    def runeBonus(self):
        return 0
    def range(self):
        return self.baserange*squsize
    def rangesq(self):
        return self.range()**2
    def speed(self):##This doesn't actually give any useful info
        return 1
    def minDamage(self):
        return self.runes["Alpha"].minDamage() if self.runes["Alpha"] else 0
    def maxDamage(self):
        return self.runes["Alpha"].maxDamage() if self.runes["Alpha"] else 0
    def findMaxXP(self):
        self.maxXP = self.maxXP*1.35
    def gainXP(self,amt):
        self.curXP += amt
        if self.curXP >= self.maxXP:
            self.curXP-=self.maxXP
            self.curLV += 1
            self.totLV += 1
            self.findMaxXP()
            print "Tower Leveled Up!"
    def place(self,tl):
        player.money-=self.cost
        self.outyet = True
        self.rect = self.image.get_rect(topleft=tl)
        self.enemytarget = None
        self.hp = self.maxhp
        self.icon.switchImg()
    def writeToolBar(self,screen):
        self.toolBarInfo = {}
        font = pygame.font.Font(None,20)
        upgradeButton = pygame.Surface((130,45))
        upgradeButton.fill((100,230,100))
        upgradeButtonRect = upgradeButton.get_rect(right=scrwid-10,bottom=scrhei-5)
        text = font.render("Upgrade!",1,(0,0,0))
        textrect = text.get_rect(center=upgradeButtonRect.center)
        screen.blit(upgradeButton,upgradeButtonRect)
        screen.blit(text,textrect)
        self.toolBarInfo["upgrade"] = [upgradeButton,upgradeButtonRect]
        bigrect = upgradeButtonRect
        font = pygame.font.Font(None,18)
        for rune in self.runes.keys():
            if self.runes[rune]:
                t = font.render("%s" % (",".join(self.runes[rune].types)),1,(0,0,0))
                tp = t.get_rect(left=upgradeButtonRect.left,bottom=bigrect.top-7)
                bigrect = tp
                screen.blit(t,tp)
                t = font.render("%s(%d)" % (self.runes[rune].name,self.runes[rune].cost),1,(0,0,0))
                tp = t.get_rect(left=upgradeButtonRect.left,bottom=bigrect.top-3)
                bigrect = tp
                screen.blit(t,tp)
            else:
                t = font.render("<%s>" % (rune),1,(75,75,75))
                bigrect = t.get_rect(left=upgradeButtonRect.left,bottom=bigrect.top-23)
                screen.blit(t,bigrect)
    @classmethod
    def loadTowers(self):
        towerlist[:] = []
        try:
            for towername in os.listdir(os.path.join(player.name)):
                if "tower" in towername:
                    nt = pickle.load(open(os.path.join(player.name,towername),"r"))
                    towerlist.append(nt)
                    iconlist.append(nt.icon)
                    nt.tempimage = pygame.transform.smoothscale(imgLoad(os.path.join('towerimgs','Fighter.png')),(squsize,squsize))
                    nt.image = nt.tempimage.copy()
                    nt.image.fill((255,255,255,50))
                    nt.image.blit(nt.tempimage,(0,0))
                    nt.icon.img = pygame.transform.smoothscale(nt.image,(20,20))
                    nt.icon.otherimg = nt.icon.img.copy()
                    nt.icon.otherimg.fill((100,100,100,100))

                    for k in nt.runes.keys():
                        nt.runes[k].tower = nt
                    nt.cost = nt.runes["Alpha"].cost*reduce(lambda x,y:x*y,[nt.runes[k].cost() for k in nt.runes.keys() if k!="Alpha" and nt.runes[k]],1) if tower.runes["Alpha"] else 0
        except:
            pass
    @classmethod
    def saveTowers(self):
        if not os.path.exists(os.path.join(player.name)):
            os.mkdir(player.name)
        for ind,tower in enumerate(towerlist[:]):
            tower.image = None
            tower.icon.img = None
            tower.icon.otherimg = None
            tower.tempimage = None
            tower.outyet = False
            tower.enemytarget = None
            tower.toolBarInfo = {}
            tower.costText = None
            for k in tower.runes.keys():
                if tower.runes[k]:
                    tower.runes[k].tower = None
            pickle.dump(tower,open(os.path.join(player.name,"tower"+str(ind)+".obj"),"w"))
            towerlist.remove(tower)
            iconlist.remove(tower.icon)
    def takeTurn(self,frametime,screen):
        if self.hp>0:
            self.hp = min(self.maxhp,self.hp+frametime/5.0*self.healthRegeneration)
            if self.runes["Alpha"]:
                self.runes["Alpha"].run(screen,frametime)
    def getAttack(self,roll,damage):
        if roll>=self.ac:
            if self.hp>0:
                self.hp -= damage
                if self.hp<=0:
                    self.enemytarget.findTarget()
                    self.enemytarget = None
                    self.outyet = False
                    self.icon.switchImg()
