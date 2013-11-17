from localdefs import senderlist,mapvar
from localclasses import Enemy

class Sender():
    def __init__(self,wave):
        self.wavenum = wave
        self.enemycounter = 0
        self.enemiesgone = 0
        senderlist.append(self)
        self.wavedictlist = mapvar.mapdict['wave'+str(self.wavenum)]
    def tick(self,frametime):
        self.enemycounter -= frametime
        if self.enemycounter<=0:
            Enemy(self.wavedictlist[self.enemiesgone],len(self.wavedictlist))
            self.enemiesgone+=1
            if self.enemiesgone<len(self.wavedictlist):
                self.enemycounter += self.wavedictlist[self.enemiesgone]["timer"]
            else:
                senderlist.remove(self)
