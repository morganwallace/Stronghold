class Upgrade:
    req = []
    @classmethod
    def checkReq(self,tower):
        return any([r in tower.upgrades for r in self.req]) or any([self.__name__ in eval(u+".req") for u in tower.upgrades])

class StartingPoint(Upgrade):
    pos = (0,0)
    req = []
    name = "Starting Point"
    @classmethod
    def checkReq(self,tower):
        return (len(tower.upgrades)==0)
    @classmethod
    def apply(self,tower):
        tower.upgrades.append(self.__name__)

class HitPoints1(Upgrade):
    pos = (0,-30)
    req = ["StartingPoint"]
    name = "Hit Points +1"
    @classmethod
    def apply(self,tower):
        if tower.curLV>0:
            tower.curLV-=1
            tower.maxhp += 1
            tower.hp += 1
            tower.upgrades.append(self.__name__)

class PhysDamPercent1(Upgrade):
    pos = (-30,0)
    req = ["StartingPoint"]
    name = "+5% Physical Damage"
    @classmethod
    def apply(self,tower):
        if tower.curLV>0:
            tower.curLV-=1
            tower.phyDamIncrease += 0.05
            tower.upgrades.append(self.__name__)

class HealSelf1(Upgrade):
    pos = (30,0)
    req = ["StartingPoint"]
    name = "+2.5% Health Regeneration"
    @classmethod
    def apply(self,tower):
        if tower.curLV>0:
            tower.curLV-=1
            tower.upgrades.append(self.__name__)
            tower.healthRegeneration *= 1.025

class Range1(Upgrade):
    pos = (0,30)
    req = ["StartingPoint"]
    name = "+7.5% Range"
    @classmethod
    def apply(self,tower):
        if tower.curLV>0:
            tower.curLV-=1
            tower.baserange *= 1.075
            tower.upgrades.append(self.__name__)