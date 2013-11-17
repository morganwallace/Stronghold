import pygame
import os
from localdefs import *
from textbox import *

pygame.init()
font = pygame.font.Font(None,20)

def genFolder():
    if 'temp' not in os.listdir(os.path.join('mapfiles')):
        os.mkdir(os.path.join('mapfiles','temp'))
        savefile = os.path.join('mapfiles','temp')
    else:
        basename = 'temp-'
        filenumber = 0
        while basename+str(filenumber) in os.listdir(os.path.join('mapfiles')):
            filenumber += 1
        os.mkdir(os.path.join('mapfiles',basename+str(filenumber)))
        savefile = os.path.join('mapfiles',basename+str(filenumber))
    return savefile

def saveMenu(screen,background,savefile,movelist,basepos):
    menuback = pygame.Surface((screen.get_width()/2,screen.get_height()))
    menuback.convert_alpha()
    menuback.fill((0,0,0))
    menuback.set_alpha(85)
    menurect = menuback.get_rect(centerx=(scrwid+55)/2,centery=scrhei/2)

    instructions = font.render("For paths: 1-left,2-top,3-right,4-bottom",1,(255,255,255))
    instructrect = instructions.get_rect(left=menurect.left+10,top=50)

    nametext = font.render("Map name: ",1,(255,255,255))
    nametextpos = nametext.get_rect(left=menurect.left+10,centery=100)
    namebox = Textbox(1,nametextpos.right+2,nametextpos.centery-5,150)
    pathtexts = list()
    for ind in range(4):
        text = font.render("Path "+str(ind+1)+": ",1,(255,255,255))
        textpos = text.get_rect(left=menurect.left+10,centery=150+50*len(pathtexts))
        textbox = Textbox(ind+2,textpos.right+2,textpos.centery-5,150)
        pathtexts.append((text,textpos,textbox))
    savebutton = pygame.Surface((100,25))
    savebutton.convert_alpha()
    savebutton.fill((255,255,255))
    saverect = savebutton.get_rect(centerx=menurect.centerx,bottom=menurect.bottom-50)
    while 1:
        screen.blit(background,(0,0))
        screen.blit(menuback,menurect)
        screen.blit(instructions,instructrect)
        namebox.Draw(screen)
        screen.blit(savebutton,saverect)
        screen.blit(nametext,nametextpos)
        for t,tp,tb in pathtexts:
            screen.blit(t,tp)
            tb.Draw(screen)
        for event in pygame.event.get():
            keyinput = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if namebox.Rect.collidepoint(pygame.mouse.get_pos()):
                    namebox.key_event(event)
                for ind in range(4):
                    if pathtexts[ind][2].Rect.collidepoint(pygame.mouse.get_pos()):
                        pathtexts[ind][2].key_event(event)
            if event.type == QUIT:
                sys.exit()
            if keyinput[K_ESCAPE]:
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if saverect.collidepoint(event.dict['pos']):
                    if namebox.text:
                        os.mkdir(os.path.join('mapfiles',namebox.text))
                        savefile = os.path.join('mapfiles',namebox.text)
                    else:
                        savefile = genFolder()
                    pygame.image.save(background,os.path.join(savefile,'background.jpg'))
                    movefile = open(os.path.join(savefile,'movefile.txt'),'w')
                    movefile.write(str(basepos[0]/20)+','+str(basepos[1]/20)+'\n')
                    for ind,singlelist in enumerate(movelist):
                        if pathtexts[ind][2].text:
                            if int(pathtexts[ind][2].text) == 1:
                                movefile.write('-1,'+str(singlelist[0][1]/20)+'\n')
                            elif int(pathtexts[ind][2].text) == 2:
                                movefile.write(str(singlelist[0][0]/20)+',-1\n')
                            elif int(pathtexts[ind][2].text) == 3:
                                movefile.write(str(scrwid/squsize+1)+','+str(singlelist[0][1]/20)+'\n')
                            elif int(pathtexts[ind][2].text) == 4:
                                movefile.write(str(singlelist[0][0]/20)+','+str(scrhei/squsize+1)+'\n')
                            for x,y in singlelist:
                                movefile.write(str(x/20)+','+str(y/20)+'\n')
        pygame.display.flip()

def runMapMaker():
    movelist = list([list() for a in range(4)])
    screen = pygame.display.set_mode((scrwid+55,scrhei))
    screen.convert_alpha()
    background = pygame.Surface(screen.get_size())
    background.convert_alpha()
    background.fill((255,255,255))
    grassbmp = imgLoad(os.path.join('backgroundimgs','Grass.bmp'))
    dsq = grassbmp.subsurface(pygame.Rect((40,41),(20,20)))
    for rec in [pygame.Rect(x,y,squsize,squsize) for x in range(0,scrwid,squsize) for y in range(0,scrhei,squsize)]:
        background.blit(dsq,rec)
    squarelist = list()
    squarelist.append((imgLoad(os.path.join('backgroundimgs','btile.png')),pygame.Rect((scrwid+5,5+25*len(squarelist)),(20,20))))
    squarelist.append((imgLoad(os.path.join('backgroundimgs','flag.png')),pygame.Rect((scrwid+5,5+25*len(squarelist)),(20,20))))
    squarelist[1][0].blit(font.render("1",1,(0,0,255)),(10,10))
    squarelist.append((imgLoad(os.path.join('backgroundimgs','flag.png')),pygame.Rect((scrwid+5,5+25*len(squarelist)),(20,20))))
    squarelist[2][0].blit(font.render("2",1,(0,0,255)),(10,10))
    squarelist.append((imgLoad(os.path.join('backgroundimgs','flag.png')),pygame.Rect((scrwid+5,5+25*len(squarelist)),(20,20))))
    squarelist[3][0].blit(font.render("3",1,(0,0,255)),(10,10))
    squarelist.append((imgLoad(os.path.join('backgroundimgs','flag.png')),pygame.Rect((scrwid+5,5+25*len(squarelist)),(20,20))))
    squarelist[4][0].blit(font.render("4",1,(0,0,255)),(10,10))
    [squarelist.append((grassbmp.subsurface(pygame.Rect((x*40,1+y*40),(20,20))),pygame.Rect((scrwid+5,5+25*len(squarelist)),(20,20)))) for x in range(3) for y in range(5)]
    selected = None
    savefile = None
    basepos = None
    while 1:
        screen.blit(background,(0,0))
        for s,r in squarelist:
            screen.blit(s,r)
        if selected:
            mx,my = pygame.mouse.get_pos()
            screen.blit(squarelist[selected-1][0],((mx/20)*20,(my/20)*20))
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if event.dict['button']==1:
                    for i,o in enumerate(squarelist):
                        if o[1].collidepoint(event.dict['pos']):
                            selected = i+1
                    if event.dict['pos'][0]<=scrwid and event.dict['pos'][0]>=0:
                        if event.dict['pos'][1]<=scrhei and event.dict['pos'][1]>=0:
                            background.blit(squarelist[selected-1][0],((event.dict['pos'][0]/20)*20,(event.dict['pos'][1]/20)*20))
                            if selected == 1:
                                basepos = event.dict['pos']
                            elif selected >= 2 and selected <=5:
                                movelist[selected-2].append(event.dict['pos'])
                else:
                    selected = None
            keyinput = pygame.key.get_pressed()
            if event.type == QUIT:
                sys.exit()
            if keyinput[K_ESCAPE]:
                sys.exit()
            if keyinput[K_s]:
                if basepos:
                    saveMenu(screen,background,savefile,movelist,basepos)
                else:
                    print "You need to place a base."

        instructions = None
        if not basepos:
            instructions = font.render("1. Click on the B tile to place a base",1,(255,255,255))
            instructrect = instructions.get_rect(centerx=scrwid/2,bottom=15)

        if instructions:
            screen.blit(instructions,instructrect)

        pygame.display.flip()

runMapMaker()
