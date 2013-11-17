from localdefs import *
from localclasses import *
import pygame
from pygame.locals import *
import EventFunctions
import sys

def makeIcons():
    del openbuttoninfo[:]
    openbuttoninfo.append(pygame.Surface((25*len(iconlist)+5,25)))
    openbuttoninfo.append(pygame.Rect((0,scrhei-25),(25*len(iconlist)+5,25)))
    openbuttoninfo[0].fill((255,255,255))

    opentowerinfo.append(pygame.Surface((150,scrhei-45)))
    opentowerinfo.append(opentowerinfo[0].get_rect(topright=(scrwid,45)))
    opentowerinfo[0].fill((255,245,245))

def tickAndClear(screen,clock,background,frametime):
    clock.tick(40)
    screen.blit(background,(0,0))
    player.currentChain = max(player.currentChain-frametime/350.0,0)

def workSenders(frametime):
    for sender in senderlist:
        sender.tick(frametime)

def workTowers(screen,frametime):
    for tower in towerlist:
        if tower.outyet:
            tower.takeTurn(frametime,screen)

def dispExplosions(screen,frametime):
    #Display any explosions in the queue, then remove them.
    for rect,time in explosions:
        screen.blit(imgLoad('explosion.png'),rect)
        explosions.remove((rect,time))
        if time-frametime>0:
            explosions.append((rect,time-frametime))

def dispText(screen,wavenum):
    #This displays the basic status at the top left.
    sur = pygame.Surface((scrwid,45))
    sur.fill((0,0,0))
    screen.blit(sur,(0,0))
    font = pygame.font.Font(None,20)
    text1 = font.render("Wave: %d |" % (wavenum),1,(255,255,255))
    textpos1 = text1.get_rect(left=10,top=5)
    text3 = font.render("Money: %0.1f |" % (player.money),1,(255,255,255))
    textpos3 = text3.get_rect(left=10,top=textpos1.bottom+2)

    n = min(textpos1,textpos3,key=lambda k:k.right)
    x = max(textpos1,textpos3,key=lambda k:k.right)

    n.right = x.right

    text2 = font.render(" %d :Health" % (player.health),1,(255,255,255))
    textpos2 = text2.get_rect(left=textpos1.right,top=textpos1.top)
    text4 = font.render(" Press 'N' to send next wave!",1,(255,255,255))
    textpos4 = text4.get_rect(left=textpos3.right,top=textpos3.top)
    mapvar.nextWaveRect = textpos4

    for i in range(1,5):
        screen.blit(eval("text"+str(i)),eval("textpos"+str(i)))

    font = pygame.font.Font(None,28)
    t = font.render("Chain: %4.1f%%" % (player.currentChain*100),1,(255,255,255))
    tp = t.get_rect(right=scrwid-10,centery=textpos1.bottom+1)
    screen.blit(t,tp)

    screen.blit(opentowerinfo[0],opentowerinfo[1])

def workEnemies(screen,frametime):
    #Let the enemies do their thing. Move, draw to screen, draw health bars.
    infobox = 0
    for enemy in enemylist:
        enemy.takeTurn(frametime,screen)
        screen.blit(enemy.image,enemy.rect)
        pygame.draw.line(screen, (0,0,0), (enemy.rect.left,enemy.rect.top-2), (enemy.rect.right,enemy.rect.top-2), 3)
        if enemy.poisontimer:
            pygame.draw.line(screen, (0,255,0), (enemy.rect.left,enemy.rect.top-2), (enemy.rect.left+(enemy.health*1.0/enemy.starthealth*1.0)*enemy.rect.width,enemy.rect.top-2), 3)
        else:
            pygame.draw.line(screen, (255,0,0), (enemy.rect.left,enemy.rect.top-2), (enemy.rect.left+(enemy.health*1.0/enemy.starthealth*1.0)*enemy.rect.width,enemy.rect.top-2), 3)
        if enemy.rect.collidepoint(pygame.mouse.get_pos()) and not infobox:
            infoboxback = pygame.Surface((75,150),SRCALPHA)
            infoboxback.fill((0,0,0,75))
            font = pygame.font.Font(None,18)
            t = font.render("%d/%d" % (enemy.health,enemy.maxhealth),1,(200,75,75,255))
            tp = t.get_rect(centerx=infoboxback.get_width()/2,top=10)
            infoboxback.blit(t,tp)
            if enemy.attackBonus and enemy.damage:
                t = font.render("+%d (%d)" % (enemy.attackBonus,enemy.damage),1,(175,75,175,255))
                tp = t.get_rect(centerx=infoboxback.get_width()/2,top=tp.bottom+4)
                infoboxback.blit(t,tp)
            t = font.render("%dcr; %0.1fxp" % (enemy.cost,enemy.xp),1,(175,75,175,255))
            tp = t.get_rect(centerx=infoboxback.get_width()/2,top=tp.bottom+4)
            infoboxback.blit(t,tp)
            if enemy.leveladj:
                t = font.render("+%d drop" % (enemy.leveladj),1,(175,75,175,255))
                tp = t.get_rect(centerx=infoboxback.get_width()/2,top=tp.bottom+4)
                infoboxback.blit(t,tp)
            ibrect = infoboxback.get_rect(topleft=pygame.mouse.get_pos()) if pygame.mouse.get_pos()[1]+infoboxback.get_height()<scrhei else infoboxback.get_rect(bottomleft=pygame.mouse.get_pos())
            screen.blit(infoboxback,ibrect)
            infobox = 1

def dispStructures(screen,mousepos):
    for struct in (towerlist):
        if struct.outyet:
            screen.blit(struct.image,struct.rect)
            pygame.draw.line(screen, (0,0,0), (struct.rect.left,struct.rect.top-2), (struct.rect.right,struct.rect.top-2), 3)
            if struct.hp>0:
                pygame.draw.line(screen, (255,0,0), (struct.rect.left,struct.rect.top-2), (struct.rect.left+(struct.hp*1.0/struct.maxhp*1.0)*struct.rect.width,struct.rect.top-2), 3)
            else:
                pygame.draw.line(screen, (200,200,200), (struct.rect.left,struct.rect.top-2), (struct.rect.left+((10+struct.hp)*1.0/(10.0))*struct.rect.width,struct.rect.top-2), 3)
            if struct.rect.collidepoint(mousepos):
                rn = int(struct.range())
                area = pygame.Surface((2*rn,2*rn),SRCALPHA)
                pygame.draw.circle(area,(255,255,255,85),(rn,rn),rn,0)
                screen.blit(area,struct.rect.move((-1*rn,-1*rn)).center)

def selectedIcon(screen,selected):
    mouseat = roundRect(selected.img.get_rect(center=pygame.mouse.get_pos()))
    screen.blit(selected.img,selected.img.get_rect(center=(mouseat[0]+squsize/2.0,mouseat[1]+squsize/2.0)))
    if selected.base == "Tower":
        rn = int(selected.tower.range())
        area = pygame.Surface((2*rn,2*rn),SRCALPHA)
        pygame.draw.circle(area,(255,0,0,75),(rn,rn),rn,0)
        screen.blit(area,mouseat.move((-1*rn,-1*rn)).center)

def selectedTower(screen,selected,mousepos):
    selected.writeToolBar(screen)

def dispIcons(screen,mousepos,font,frametime):
    isover = 0
    for icon in iconlist:
        screen.blit(icon.img,icon.rect)
        if icon.rect.collidepoint(mousepos):
            isover = 1
            if icon is mapvar.iconhold[0]:
                mapvar.iconhold = (icon,mapvar.iconhold[1]+frametime)
                if mapvar.iconhold[1]>3:
                    text = font.render("Speed %0.1f" % (icon.tower.speed()),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=icon.rect.top-2)
                    screen.blit(text,textpos)
                    text = font.render("Damage %0.1f-%0.1f" % (icon.tower.minDamage(),icon.tower.maxDamage()),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=textpos.top-2)
                    screen.blit(text,textpos)
                    text = font.render("Range %0.1f" % (icon.tower.range()),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=textpos.top-2)
                    screen.blit(text,textpos)
                    text = font.render("Armor Class %0.1f" % (icon.tower.ac),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=textpos.top-2)
                    screen.blit(text,textpos)
                    text = font.render("Max HP %0.1f" % (icon.tower.maxhp),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=textpos.top-2)
                    screen.blit(text,textpos)
                    text = font.render("Cost %0.1f" % (icon.tower.cost),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=textpos.top-2)
                    screen.blit(text,textpos)
                else:
                    text = font.render("Cost: %0.1f" % (icon.tower.cost),1,(0,0,0))
                    textpos = text.get_rect(left=icon.rect.left,bottom=icon.rect.top-2)
                    screen.blit(text,textpos)
            else:
                mapvar.iconhold = (icon,frametime)
                text = font.render("Cost: %0.1f" % (icon.tower.cost),1,(0,0,0))
                textpos = text.get_rect(left=icon.rect.left,bottom=icon.rect.top-2)
                screen.blit(text,textpos)
    if isover == 0:
        mapvar.iconhold = (None,0)

def roundPoint(point):
    x = squsize*(point[0]/squsize)
    y = squsize*(point[1]/squsize)
    return (x,y)

def roundRect(rect):
    new = rect.copy()
    new.topleft = roundPoint((rect.centerx,rect.centery))
    return new

def workEvents(screen,frametime,selected,wavenum,Sender,speed,font,font2):
    timedel = 0
    mapvar.rollNext -= frametime
    didrollthisturn = 0
    if mapvar.rollNext <= 0 and mapvar.hasStarted and not mapvar.hasEnded:
        wavenum = EventFunctions.nextWave(0, wavenum, Sender)
        didrollthisturn = 1
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            selected,mBUb,timedel = EventFunctions.mouseButtonUp(event, selected, screen, font,font2)
        else:
            keyinput = pygame.key.get_pressed()
            if keyinput[K_ESCAPE]:
                sys.exit()
            elif event.type==KEYDOWN and event.dict['key']==K_n and not didrollthisturn:
                wavenum = EventFunctions.nextWave(event, wavenum, Sender)
            elif keyinput[K_f]:
                screen = pygame.display.set_mode((scrwid,scrhei),FULLSCREEN)
            elif keyinput[K_w]:
                screen = pygame.display.set_mode((scrwid,scrhei))
            elif keyinput[K_UP]:
                if speed<10:
                    speed+=1
                    print speed
            elif keyinput[K_DOWN]:
                if speed>1:
                    speed-=1
                    print speed
    return screen,selected,wavenum,speed,timedel