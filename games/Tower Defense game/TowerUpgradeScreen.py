import pygame
import sys,os
from pygame.locals import *
import time
from localdefs import imgLoad,player,towerlist,scrwid,scrhei
import inspect
import TowerUpgrades

def upgrade(screen,tower):
    starttime = time.time()
    background = screen.copy()
    background.set_alpha(50)
    tb = screen.copy()
    tb.fill((0,0,0))
    scrwidoffset = scrwid/2
    scrheioffset = scrhei/2
    def resetIcons():
        icons = []
        ups = inspect.getmembers(TowerUpgrades,inspect.isclass)
        for c,d in ups:
            if c != "Upgrade":
                try:
                    next = (c,eval("TowerUpgrades."+c+".pos"),imgLoad(os.path.join("upgradeicons",c+".jpg")))
                    if (c in tower.upgrades):
                        temp = next[2].copy()
                        temp.fill((0,150,0))
                        temp.set_alpha(125)
                        next[2].blit(temp,(0,0))
                    elif not eval("TowerUpgrades."+c+".checkReq(tower)"):
                        temp = next[2].copy()
                        temp.fill((150,0,0))
                        temp.set_alpha(125)
                        next[2].blit(temp,(0,0))
                    icons.append(next)
                except:
                    try:
                        next = (c,eval("TowerUpgrades."+c+".pos"),imgLoad(os.path.join("upgradeicons",c[:2]+".jpg")))
                        if (c in tower.upgrades):
                            temp = next[2].copy()
                            temp.fill((0,150,0))
                            temp.set_alpha(125)
                            next[2].blit(temp,(0,0))
                        elif not eval("TowerUpgrades."+c+".checkReq(tower)"):
                            temp = next[2].copy()
                            temp.fill((150,0,0))
                            temp.set_alpha(125)
                            next[2].blit(temp,(0,0))
                        icons.append(next)
                    except:
                        taimg = pygame.Surface((20,20))
                        if (c in tower.upgrades):
                            taimg.fill((0,150,0))
                        elif not eval("TowerUpgrades."+c+".checkReq(tower)"):
                            taimg.fill((150,0,0))
                        else:
                            taimg.fill((90,90,255))
                        icons.append((c,eval("TowerUpgrades."+c+".pos"),taimg))
        return icons
    icons = resetIcons()
    font2 = pygame.font.Font(None,25)
    while 1:
        screen.blit(tb,(0,0))
        screen.blit(background,(0,0))
        mouseon = None
        info = font2.render("Points Remaining: %d" % (tower.curLV),1,(255,255,255))
        infopos = info.get_rect(topleft=(5,5))
        screen.blit(info,infopos)
        info = font2.render("Current XP: %d/%d" % (tower.curXP,tower.maxXP),1,(255,255,255))
        infopos = info.get_rect(topleft=(5,infopos.bottom+5))
        screen.blit(info,infopos)
        for c,p,i in icons:
            for r in eval("TowerUpgrades."+c+".req"):
                rp = eval("TowerUpgrades."+r+".pos")
                pygame.draw.aaline(screen,(255,255,255),i.get_rect(topleft=p).move(scrwidoffset,scrheioffset).center,(rp[0]+10+scrwidoffset,rp[1]+10+scrheioffset))
        for c,p,i in icons:
            screen.blit(i,(p[0]+scrwidoffset,p[1]+scrheioffset))
            if i.get_rect(topleft=p).move(scrwidoffset,scrheioffset).collidepoint(pygame.mouse.get_pos()):
                mouseon = c
                info = font2.render("%s" % (eval("TowerUpgrades."+c+".name")),1,(255,210,220))
                infopos = info.get_rect(center=(screen.get_width()/2,screen.get_height()-30))
                screen.blit(info,infopos)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if event.dict['button']==1:
                    if mouseon and eval("TowerUpgrades."+mouseon+".checkReq(tower)"):
                        eval("TowerUpgrades."+mouseon+".apply(tower)")
                        icons = resetIcons()
                else:
                    return time.time()-starttime
            else:
                keyinput = pygame.key.get_pressed()
                if keyinput[K_ESCAPE]:
                    sys.exit()
        keyinput = pygame.key.get_pressed()
        if keyinput[K_UP]:
            scrheioffset += 1
        elif keyinput[K_DOWN]:
            scrheioffset -= 1
        if keyinput[K_LEFT]:
            scrwidoffset += 1
        elif keyinput[K_RIGHT]:
            scrwidoffset -= 1
        pygame.display.flip()