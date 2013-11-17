import pygame
from pygame.locals import *
import localdefs
import os
import sys
import pickle

def pickMap(screen,clock):
    maplist = [d for d in os.listdir(os.path.join('mapfiles')) if
                os.path.isdir(os.path.join('mapfiles',d)) and d[0]!='.']
    font = pygame.font.Font(None,20)
    mapobjectlist = list()
    completionbar = list()
    for map in maplist:
        if os.path.isfile(os.path.join('mapfiles',map,'description.txt')):
            text = font.render("Map '%s': %s" % (map,open(os.path.join('mapfiles',map,'description.txt')).readline().strip()),1,(0,0,0))
        else:
            text = font.render("Map '%s'" % (map),1,(0,0,0))
        textpos = text.get_rect(left=5,top=5+25*len(mapobjectlist))
        ci = pygame.Surface((20,25))
        if map in localdefs.player.mapscompleted:
            ci.fill((0,200,0))
        else:
            ci.fill((0,0,0))
        cr = ci.get_rect(right=localdefs.scrwid-20,centery=textpos.centery)
        textpos.right = cr.left-10
        completionbar.append((ci,cr))
        mapobjectlist.append((text,textpos,map))
    text = font.render("BACK",1,(230,20,20))
    textpos = text.get_rect(left=5,top=5+25*len(mapobjectlist))
    mapobjectlist.append((text,textpos,""))
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    while 1:
        screen.blit(background,(0,0))
        for t,tp,m in mapobjectlist:
            screen.blit(t,tp)
        for i,r in completionbar:
            screen.blit(i,r)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                for t,tp,m in mapobjectlist:
                    if tp.collidepoint(event.dict['pos']):
                        return str(m)
            keyinput = pygame.key.get_pressed()
            if event.type == QUIT:
                sys.exit()
            if keyinput[K_ESCAPE] or keyinput[K_BACKSPACE]:
                return ""
            elif keyinput[K_f]:
                screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei),FULLSCREEN)
            elif keyinput[K_w]:
                screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei))
        pygame.display.flip()

def pickTower(screen,clock):
    towers = list()
    font = pygame.font.Font(None,30)
    skillgems = list()
    for tower in localdefs.towerlist:
        tower.rect = tower.image.get_rect(centerx=(len(towers)+1)*localdefs.scrwid/(len(localdefs.towerlist)+1.0),centery=localdefs.scrhei/2)
        tower.cost = tower.runes["Alpha"].cost*reduce(lambda x,y:x*y,[tower.runes[k].cost() for k in tower.runes.keys() if k!="Alpha" and tower.runes[k]],1) if tower.runes["Alpha"] else 0
        tower.costText = font.render("%d" % (tower.cost),1,(0,0,0))
        tower.costRect = tower.costText.get_rect(centerx=tower.rect.centerx,centery=tower.rect.centery+25)
        towers.append(tower)
    run = 1
    bg = pygame.Surface((localdefs.scrwid,localdefs.scrhei))
    bg.fill((255,255,255))
    backtext = font.render("BACK",1,(230,20,20))
    backtextpos = backtext.get_rect(centerx=localdefs.scrwid/2,centery=localdefs.scrhei-100)
    while run:
        clock.tick(30)
        screen.blit(bg,(0,0))

        for t in towers:
            screen.blit(t.image,t.rect)
            screen.blit(t.costText,t.costRect)

        screen.blit(backtext,backtextpos)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if backtextpos.collidepoint(event.dict['pos']):
                    localdefs.player.save()
                    localdefs.player.load()
                    return
                else:
                    for t in towers:
                        if t.rect.collidepoint(event.dict['pos']):
                            return editTower(screen,clock,t)
            else:
                keyinput = pygame.key.get_pressed()
                if keyinput[K_ESCAPE] or keyinput[K_BACKSPACE]:
                    return
                elif keyinput[K_f]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei),FULLSCREEN)
                elif keyinput[K_w]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei))

        pygame.display.flip()

def editTower(screen,clock,tower):
    font = pygame.font.Font(None,30)
    runes = list()
    tower.rect = tower.image.get_rect(centerx=localdefs.scrwid/2,top=100)
    tower.cost = tower.runes["Alpha"].cost*reduce(lambda x,y:x*y,[tower.runes[k].cost() for k in tower.runes.keys() if k!="Alpha" and tower.runes[k]],1) if tower.runes["Alpha"] else 0
    tower.costText = font.render("%d" % (tower.cost),1,(0,0,0))
    tower.costRect = tower.costText.get_rect(centerx=tower.rect.centerx,centery=tower.rect.centery+25)
    class RP:
        rpcenter = {"Alpha":(localdefs.scrwid/2,localdefs.scrhei/2)}
        rpcenter["Beta"] = (rpcenter["Alpha"][0]+50,rpcenter["Alpha"][1])
        def __init__(self,sig):
            self.sig = sig
            self.outerrect = pygame.Rect(0,0,30,30)
            self.innerrect = pygame.Rect(0,0,25,25)
            self.outerrect.center = self.rpcenter[sig]
            self.innerrect.center = self.rpcenter[sig]
            self.img = pygame.Surface((30,30))
            self.img.fill((180,180,180))
        def blit(self):
            screen.blit(self.img,self.outerrect)
        def testMove(self,point,r):
            if self.outerrect.collidepoint(point):
                if self.sig in tower.runes.keys() and tower.runes[self.sig] and r[3] == None and r[2].slotIn(self.sig):
                    replist = None
                    for rlist in runes:
                        if rlist[2] == tower.runes[self.sig]:
                            replist = rlist
                    replist[3] = None
                    replist[2].tower = None
                    localdefs.player.spareRunes.append(replist[2])
                    localdefs.player.spareRunes.remove(r[2])
                    tower.runes[self.sig] = r[2]
                    r[3] = tower
                    r[2].tower = tower
                    r[1] = self.innerrect
                    tower.cost = tower.runes["Alpha"].cost*reduce(lambda x,y:x*y,[tower.runes[k].cost() for k in tower.runes.keys() if k!="Alpha" and tower.runes[k]],1) if tower.runes["Alpha"] else 0
                    tower.costText = font.render("%d" % (tower.cost),1,(0,0,0))
                    tower.costRect = tower.costText.get_rect(centerx=tower.rect.centerx,centery=tower.rect.centery+25)
                    r = None
                    tempnum = 0
                    for rlist in runes:
                        if rlist[3] == None:
                            rlist[1] = rlist[0].get_rect(left=100+35*tempnum,centery=localdefs.scrhei-150)
                            tempnum += 1
                    return r
                elif r[3] == None and r[2].slotIn(self.sig):
                    localdefs.player.spareRunes.remove(r[2])
                    tower.runes[self.sig] = r[2]
                    r[3] = tower
                    r[2].tower = tower
                    r[1] = self.innerrect
                    tower.cost = tower.runes["Alpha"].cost*reduce(lambda x,y:x*y,[tower.runes[k].cost() for k in tower.runes.keys() if k!="Alpha" and tower.runes[k]],1) if tower.runes["Alpha"] else 0
                    tower.costText = font.render("%d" % (tower.cost),1,(0,0,0))
                    tower.costRect = tower.costText.get_rect(centerx=tower.rect.centerx,centery=tower.rect.centery+25)
                    return r
            return 0
    runeposition = [RP(k) for k in tower.runes.keys()]
    for k in tower.runes.keys():
        if tower.runes[k]:
            img = pygame.Surface((25,25))
            img.fill((225,25,25) if tower.runes[k].col == "Red" else (25,225,25) if tower.runes[k].col == "Green" else (25,25,225))
            rect = img.get_rect(center=RP.rpcenter[k])
            runes.append([img,rect,tower.runes[k],tower])
    for i,rune in enumerate(localdefs.player.spareRunes):
        img = pygame.Surface((25,25))
        img.fill((225,25,25) if rune.col == "Red" else (25,225,25) if rune.col == "Green" else (25,25,225))
        rect = img.get_rect(left=100+35*i,centery=localdefs.scrhei-150)
        runes.append([img,rect,rune,None])
    run = 1
    bg = pygame.Surface((localdefs.scrwid,localdefs.scrhei))
    bg.fill((255,255,255))
    backtext = font.render("BACK",1,(230,20,20))
    backtextpos = backtext.get_rect(centerx=localdefs.scrwid/2,centery=localdefs.scrhei-100)
    mousedown = None
    while run:
        clock.tick(30)
        screen.blit(bg,(0,0))

        screen.blit(tower.image,tower.rect)
        screen.blit(tower.costText,tower.costRect)

        for rp in runeposition:
            rp.blit()

        for r in runes:
            screen.blit(r[0],r[1])

        screen.blit(backtext,backtextpos)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                for r in runes:
                    if r[1].collidepoint(event.dict['pos']):
                        mousedown = r
            elif event.type == MOUSEBUTTONUP:
                if backtextpos.collidepoint(event.dict['pos']):
                    localdefs.player.save()
                    localdefs.player.load()
                    return
                else:
                    if mousedown:
                        towhit = 0
                        for rp in runeposition:
                            r = rp.testMove(event.dict['pos'],mousedown)
                            if r:
                                for i in range(len(mousedown)):
                                    mousedown[i] = r[i]
                                towhit += 1
                                mousedown = None
                        if not towhit and mousedown[3]:
                            for k in tower.runes.keys():
                                if tower.runes[k] == mousedown[2]:
                                    tower.runes[k] = None
                            mousedown[3] = None
                            mousedown[2].tower = None
                            localdefs.player.spareRunes.append(mousedown[2])
                            mousedown[1] = mousedown[0].get_rect(left=100+35*len([r for r in runes if r[3]==None]),centery=localdefs.scrhei-150)
                            tower.cost = tower.runes["Alpha"].cost*reduce(lambda x,y:x*y,[tower.runes[k].cost() for k in tower.runes.keys() if k!="Alpha" and tower.runes[k]],1) if tower.runes["Alpha"] else 0
                            tower.costText = font.render("%d" % (tower.cost),1,(0,0,0))
                            tower.costRect = tower.costText.get_rect(centerx=tower.rect.centerx,centery=tower.rect.centery+25)
                            mousedown = None
            else:
                keyinput = pygame.key.get_pressed()
                if keyinput[K_ESCAPE] or keyinput[K_BACKSPACE]:
                    return
                elif keyinput[K_f]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei),FULLSCREEN)
                elif keyinput[K_w]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei))

        pygame.display.flip()

def pickNewTowerImage(screen,clock,st):
    run = 1
    bg = pygame.Surface((localdefs.scrwid,localdefs.scrhei))
    bg.fill((255,255,255))
    font = pygame.font.Font(None,20)
    fontBig = pygame.font.Font(None,30)
    nametext = fontBig.render("Pick Tower %d's Image" % (st),1,(0,0,0))
    nametextpos = nametext.get_rect(centerx=localdefs.scrwid/2,top=10)
    ImageNames = ["Basic","Archer","Cleric","ClericNegative","Fighter","Mage","Node"]
    ImageFiles = dict()
    for n in ImageNames:
        ImageFiles[n] = localdefs.imgLoad(os.path.join("towerimgs",n+".png"))
    while run:
        clock.tick(30)
        screen.blit(bg,(0,0))

        screen.blit(nametext,nametextpos)

        textrectdict = dict()
        imgrectdict = dict()

        for i,key in enumerate(ImageFiles.keys()):
            text = font.render("%s" % (key),1,(0,0,0))
            textpos = text.get_rect(centerx=(1+i)*(localdefs.scrwid/(1+len(ImageFiles))),centery=localdefs.scrhei/2)
            textrectdict[key] = textpos
            imgrect = ImageFiles[key].get_rect(centerx=textpos.centerx,bottom=textpos.top-2)
            imgrectdict[key] = imgrect
            screen.blit(text,textpos)
            screen.blit(ImageFiles[key],imgrect)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == MOUSEBUTTONUP:
                for key in textrectdict.keys():
                    if textrectdict[key].collidepoint(event.dict['pos']) or imgrectdict[key].collidepoint(event.dict['pos']):
                        localdefs.player.modDict['tower'][st]['ImageName'] = key
                        localdefs.player.save()
                        localdefs.player.__init__()
                        return
            else:
                keyinput = pygame.key.get_pressed()
                if keyinput[K_ESCAPE] or keyinput[K_BACKSPACE]:
                    return
                elif keyinput[K_f]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei),FULLSCREEN)
                elif keyinput[K_w]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei))

        pygame.display.flip()

def changeTowerAbilities(screen,clock):
    run = 1
    bg = pygame.Surface((localdefs.scrwid,localdefs.scrhei))
    bg.fill((255,255,255))
    font = pygame.font.Font(None,20)
    fontBig = pygame.font.Font(None,30)
    nametext = fontBig.render("Pick Tower Abilities",1,(0,0,0))
    nametextpos = nametext.get_rect(centerx=localdefs.scrwid/2,top=10)

    towerlist = list()

    for num in range(0,localdefs.player.modDict['towerNum']):
        towerlist.append(dict())
        try:
            towerlist[num]["image"] = localdefs.imgLoad(os.path.join('towerimgs',localdefs.player.modDict['tower'][num+1]['ImageName']+'.png'))
        except:
            towerlist[num]["image"] = localdefs.imgLoad(os.path.join('towerimgs','Fighter.png'))

        towerlist[num]["imagerect"] = towerlist[num]["image"].get_rect(left=20,centery=nametextpos.bottom+(num+1)*(localdefs.scrhei-nametextpos.bottom)/(localdefs.player.modDict['towerNum']+2))
        towerlist[num]["upgrades"] = list()
        towerlist[num]["num"] = num

    upslist = list()
    nondisups = list()

    if 'upgrades' in localdefs.player.loadarray.keys():
        for up in localdefs.player.loadarray['upgrades']:
            if len(up)>0:
                if eval("PlayerUpgrades."+up[:-1]+".selectTower"):
                    img = pygame.Surface((20,20))
                    img.fill((137,109,213))
                    upslist.append(dict())
                    upslist[-1]["class"] = eval("PlayerUpgrades."+up[:-1])
                    upslist[-1]["name"] = up[:-1]
                    upslist[-1]["curtower"] = int(up[-1])-1
                    upslist[-1]["img"] = img
                    upslist[-1]["rect"] = upslist[-1]["img"].get_rect(left=60+30*len(towerlist[int(up[-1])-1]["upgrades"]),centery=towerlist[int(up[-1])-1]["imagerect"].centery)
                    towerlist[int(up[-1])-1]["upgrades"].append(upslist[-1])
                else:
                    nondisups.append(dict())
                    nondisups[-1]["name"] = up[:-1]
                    nondisups[-1]["curtower"] = -1
    else:
        print "No Abilities To Assign"
        return

    selected = None

    while run:
        clock.tick(30)
        screen.blit(bg,(0,0))

        screen.blit(nametext,nametextpos)

        for up in upslist:
            screen.blit(up["img"],up["rect"])

        for tower in towerlist:
            screen.blit(tower["image"],tower["imagerect"])

        if selected:
            screen.blit(selected["img"],pygame.mouse.get_pos())
        else:
            for up in upslist:
                if up["rect"].collidepoint(pygame.mouse.get_pos()):
                    try:text = font.render("%s" % (up["class"].singlename),1,(0,0,0))
                    except:text = font.render("%s" % (up["class"].name),1,(0,0,0))
                    if pygame.mouse.get_pos()[0]>localdefs.scrwid/2:
                        screen.blit(text,text.get_rect(right=up["rect"].left-10,bottom=up["rect"].top))
                    else:
                        screen.blit(text,text.get_rect(left=up["rect"].right+10,bottom=up["rect"].top))

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                for up in upslist:
                    if up["rect"].collidepoint(event.dict["pos"]):
                        selected = up
            elif event.type == MOUSEBUTTONUP:
                if selected:
                    for tower in towerlist:
                        if tower["imagerect"].collidepoint(event.dict["pos"]):
                            selected["rect"] = selected["img"].get_rect(left=60+30*len(tower["upgrades"]),centery=tower["imagerect"].centery)
                            selected["curtower"] = tower["num"]
                            tower["upgrades"].append(selected)
                selected = None
            else:
                keyinput = pygame.key.get_pressed()
                if keyinput[K_ESCAPE] or keyinput[K_BACKSPACE]:
                    localdefs.player.upgrades = list()
                    for up in upslist+nondisups:
                        localdefs.player.upgrades.append(up["name"]+str(up["curtower"]+1))
                    localdefs.player.save()
                    localdefs.player.__init__()
                    return
                elif keyinput[K_f]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei),FULLSCREEN)
                elif keyinput[K_w]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei))

        pygame.display.flip()

def main(screen,clock):
    bg = pygame.Surface((localdefs.scrwid,localdefs.scrhei))
    bg.fill((255,255,255))
    run = 1
    imgs = dict()
    rects = dict()
    for num,i in enumerate(["playmap","edittowers","options"]):
        imgs[i] = localdefs.imgLoad(os.path.join("menuimages",i+".png"))
        rects[i] = imgs[i].get_rect(centerx=localdefs.scrwid/2,centery=(num+1)*localdefs.scrhei/5)
    while run:
        clock.tick(30)
        screen.blit(bg,(0,0))

        for key in imgs.keys():
            screen.blit(imgs[key],rects[key])

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if rects["playmap"].collidepoint(event.dict['pos']):
                    map = pickMap(screen,clock)
                    if len(map)>2:
                        return map
                elif rects["edittowers"].collidepoint(event.dict['pos']):
                    pickTower(screen,clock)
                elif rects["options"].collidepoint(event.dict['pos']):
                    print "Not Yet Implemented"
            else:
                keyinput = pygame.key.get_pressed()
                if keyinput[K_ESCAPE]:
                    sys.exit()
                elif keyinput[K_f]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei),FULLSCREEN)
                elif keyinput[K_w]:
                    screen = pygame.display.set_mode((localdefs.scrwid,localdefs.scrhei))

        pygame.display.flip()