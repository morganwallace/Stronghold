import random
import localdefs
import pygame
import Imprints

class Rune:
    name = ""
    slots = []
    def __init__(self,tower):
        self.types = []
        self.tower = tower
        self.col = "Grey"
    def speed(self):
        pass
    def slotIn(self,slot):
        if slot in self.slots:
            return True
        return False
    @classmethod
    def reward(self,enemy,tower):
        while random.randint(1,100)+enemy.leveladj+tower.runeFind()>=100:
            a = localdefs.mapvar.enemylevel+enemy.leveladj+tower.runeBonus()
            b = min(len(skillGemsList),a)
            c = random.randint(1,a)
            d = random.randint(1,b)
            gemgot = skillGemsList[d-1](None,c-d if c-d>=0 else 0)
            print "Received a",gemgot.name,"rune!"
            localdefs.player.spareRunes.append(gemgot)

class SingleAttack(Rune):
    name = "Single Attack"
    slots = ["Alpha"]
    posimprints = [("Cheaper",0.96,0.98),("Stronger",1.02,1.06)]
    def __init__(self,tower,randomgen=0):
        Rune.__init__(self,tower)
        self.types = ["Attack"]
        self.col = "Red"
        self.cost = 25
        self.tempspeed = self.maxspeed = 1.0
        self.imprints = []
        self.damageBonus = 1.0
        if randomgen:
            self.generateImprints(randomgen)
    def generateImprints(self,modifier):
        if modifier<=2:
            name,min,max = random.choice(self.posimprints)
            self.imprints.append(eval("Imprints.imprint"+str(name)+"(self,"+str(min)+","+str(max)+")"))
            print self.imprints[0].text
        else:
            for i in range(2):
                name,min,max = random.choice(self.posimprints)
                self.imprints.append(eval("Imprints.imprint"+str(name)+"(self,"+str(min)+","+str(max)+")"))
                print self.imprints[0].text
    def speed(self):
        return self.maxspeed*(1-self.tower.speedIncrease)*reduce(lambda x,y:x*y,[self.tower.runes[k].speed() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)
    def minDamage(self):
        return 4*self.damageModifier()*reduce(lambda x,y:x*y,[self.tower.runes[k].minDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)*reduce(lambda x,y:x*y,[self.tower.runes[k].physDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)
    def maxDamage(self):
        return 6*self.damageModifier()*reduce(lambda x,y:x*y,[self.tower.runes[k].maxDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)*reduce(lambda x,y:x*y,[self.tower.runes[k].physDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)
    def damageModifier(self):
        return (1+self.tower.phyDamIncrease)*self.damageBonus*(1+self.tower.damIncrease)+self.tower.phyDamBonus+self.tower.damBonus
    def run(self,screen,time):
        enemypoint = None
        self.tempspeed -= time
        if self.tempspeed<=0:
            if self.tower.enemytarget and self.tower.enemytarget in localdefs.enemylist and (self.tower.rect.centerx-self.tower.enemytarget.rect.centerx)**2+(self.tower.rect.centery-self.tower.enemytarget.rect.centery)**2<=self.tower.rangesq():
                hitrect = self.tower.enemytarget.rect
                self.tower.enemytarget.getDamage(self.tower,random.uniform(self.minDamage(),self.maxDamage()))
                enemypoint = hitrect.center
            else:
                for enemy in sorted(localdefs.enemylist,key=(lambda x: x.distance),reverse=True):
                    if not enemypoint and (self.tower.rect.centerx-enemy.rect.centerx)**2+(self.tower.rect.centery-enemy.rect.centery)**2<=self.tower.rangesq():
                        enemy.getDamage(self.tower,random.uniform(self.minDamage(),self.maxDamage()))
                        enemypoint = enemy.rect.center
            if enemypoint:
                temp = self.tower.image.copy()
                temp.fill((255,255,255))
                screen.blit(temp,self.tower.rect)
                pygame.draw.line(screen,(255,255,255),self.tower.rect.center,enemypoint)
                self.tempspeed = self.speed()
        return enemypoint

class QuickAttack(Rune):
    name = "Quick Attack"
    slots = ["Alpha"]
    posimprints = [("Cheaper",0.96,0.98),("Stronger",1.02,1.06)]
    def __init__(self,tower,randomgen=0):
        Rune.__init__(self,tower)
        self.types = ["Attack"]
        self.col = "Red"
        self.cost = 20
        self.tempspeed = self.maxspeed = 0.6
        self.imprints = []
        self.damageBonus = 1.0
        if randomgen:
            self.generateImprints(randomgen)
    def generateImprints(self,modifier):
        if modifier<=2:
            name,min,max = random.choice(self.posimprints)
            self.imprints.append(eval("Imprints.imprint"+str(name)+"(self,"+str(min)+","+str(max)+")"))
            print self.imprints[0].text
        else:
            for i in range(2):
                name,min,max = random.choice(self.posimprints)
                self.imprints.append(eval("Imprints.imprint"+str(name)+"(self,"+str(min)+","+str(max)+")"))
                print self.imprints[0].text
    def speed(self):
        return self.maxspeed*(1-self.tower.speedIncrease)*reduce(lambda x,y:x*y,[self.tower.runes[k].speed() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)
    def minDamage(self):
        return 1.5*self.damageModifier()*reduce(lambda x,y:x*y,[self.tower.runes[k].minDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)*reduce(lambda x,y:x*y,[self.tower.runes[k].physDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)
    def maxDamage(self):
        return 2*self.damageModifier()*reduce(lambda x,y:x*y,[self.tower.runes[k].maxDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)*reduce(lambda x,y:x*y,[self.tower.runes[k].physDamage() for k in self.tower.runes.keys() if k!="Alpha" and self.tower.runes[k]],1)
    def damageModifier(self):
        return (1+self.tower.phyDamIncrease)*self.damageBonus*(1+self.tower.damIncrease)+self.tower.phyDamBonus+self.tower.damBonus
    def run(self,screen,time):
        enemypoint = None
        self.tempspeed -= time
        if self.tempspeed<=0:
            if self.tower.enemytarget and self.tower.enemytarget in localdefs.enemylist and (self.tower.rect.centerx-self.tower.enemytarget.rect.centerx)**2+(self.tower.rect.centery-self.tower.enemytarget.rect.centery)**2<=self.tower.rangesq():
                hitrect = self.tower.enemytarget.rect
                self.tower.enemytarget.getDamage(self.tower,random.uniform(self.minDamage(),self.maxDamage()))
                enemypoint = hitrect.center
            else:
                for enemy in sorted(localdefs.enemylist,key=(lambda x: x.distance),reverse=True):
                    if not enemypoint and (self.tower.rect.centerx-enemy.rect.centerx)**2+(self.tower.rect.centery-enemy.rect.centery)**2<=self.tower.rangesq():
                        enemy.getDamage(self.tower,random.uniform(self.minDamage(),self.maxDamage()))
                        enemypoint = enemy.rect.center
            if enemypoint:
                temp = self.tower.image.copy()
                temp.fill((255,255,255))
                screen.blit(temp,self.tower.rect)
                pygame.draw.line(screen,(255,255,255),self.tower.rect.center,enemypoint)
                self.tempspeed = self.speed()
        return enemypoint

skillGemsList = [SingleAttack,QuickAttack]