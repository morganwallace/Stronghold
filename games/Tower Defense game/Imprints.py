import random
class Imprint:
    def __init__(self,rune,modifier):
        self.rune = rune
        self.modifier = modifier
        for imp in self.rune.imprints:
            if imp.__class__ == self.__class__:
                imp.deprint()
                imp.modifier *= self.modifier
                imp.imprint()
                self.rune.imprints.remove(self)
        if self in self.rune.imprints:
            self.imprint()
    def imprint(self):
        print "Err: Imprint attempted - No Imprint function",self
    def deprint(self):
        print "Err: Deprint attempted - No Deprint function",self

class imprintCheaper(Imprint):
    def __init__(self,rune,low,high):
        Imprint.__init__(self,rune,random.uniform(low,high))
        self.text = "Reduce cost by %0.2f%%" % ((1-self.modifier)*100)
    def imprint(self):
        self.rune.cost *= self.modifier
    def deprint(self):
        self.rune.cost /= self.modifier

class imprintStronger(Imprint):
    def __init__(self,rune,low,high):
        Imprint.__init__(self,rune,random.uniform(low,high))
        self.text = "Increase damage by %0.2f%%" % ((self.modifier-1)*100)
    def imprint(self):
        self.rune.damageBonus *= self.modifier
    def deprint(self):
        self.rune.damageBonus /= self.modifier