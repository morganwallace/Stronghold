import localdefs
import MainFunctions
import localclasses
import sys
import TowerUpgradeScreen
import pygame.locals

def leftCheckSelect(event,selected):
    for object in localdefs.towerlist:
        if object.outyet and object.rect.collidepoint(event.dict['pos']):
            return object,True
    for object in localdefs.iconlist:
        if object.rect.collidepoint(event.dict['pos']):
            return object,True
    if localdefs.mapvar.nextWaveRect.collidepoint(event.dict['pos']):
        pygame.event.post(pygame.event.Event(pygame.locals.KEYDOWN,key=pygame.locals.K_n))
        return selected,False
    return selected,False

def leftSelectedTower(event,selected, screen):
    if selected.toolBarInfo["upgrade"][1].collidepoint(event.dict["pos"]):
        timeDel = TowerUpgradeScreen.upgrade(screen,selected)
        return selected,0,timeDel
    return None,0,0

def placeTower(event,selected):
    if not selected.tower.outyet and (not any([ttower.rect.collidepoint(event.dict['pos']) for ttower in localdefs.towerlist if ttower.outyet])
        and not any([p.inflate(25,25).collidepoint(event.dict['pos']) for pathrectlist in localdefs.mapvar.pathrectlists for p in pathrectlist])):
        selected.tower.place(MainFunctions.roundPoint(event.dict['pos']))
        return None,True,0
    return selected,False,0

def leftSelectedIcon(event,selected):
    if event.dict['pos'][1]<localdefs.scrhei-localdefs.squsize:
        if localdefs.player.money>=selected.tower.cost:
            return placeTower(event, selected)
        else:
            print "Not Enough Money"
    return selected,False,0

def leftAlreadySelected(event,selected, screen):
    if selected.__class__ == localclasses.Icon:
        return leftSelectedIcon(event, selected)
    elif localclasses.Tower is selected.__class__:
        return leftSelectedTower(event,selected, screen)

def rightAlreadySelected(event,selected):
    return False

def mouseButtonUp(event,selected,screen,font,font2):
    if event.dict['button']==1:
        selected,lCSb = leftCheckSelect(event, selected)
        if not lCSb and selected:
            return leftAlreadySelected(event, selected, screen)
        else:
            return selected,lCSb,0
    else:
        if selected and rightAlreadySelected(event,selected):
            return selected,(False if not selected else True),0
        else:
            return None,(False if not selected else True),0

def nextWave(event,wavenum,Sender):
    localdefs.mapvar.hasStarted = 1
    localdefs.mapvar.rollNext = 30
    wavenum+=1
    localdefs.mapvar.wavesSinceLoss+=1
    if ('wave'+str(wavenum)) in localdefs.mapvar.mapdict:
        Sender(wavenum)
    if ('wave'+str(wavenum)) not in localdefs.mapvar.mapdict:
        if len(localdefs.enemylist) == 0:
            localdefs.mapvar.currentCompleted = 1
            print "You won that one!"
            localdefs.player.save()
            sys.exit()
        else:
            print "There are still enemies on the screen!"
            wavenum-=1
            localdefs.mapvar.hasEnded = 1
    return wavenum
