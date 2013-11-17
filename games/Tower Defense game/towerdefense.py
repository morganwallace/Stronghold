#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/
#
# Original Coder: Austin Morgan (codenameduckfin@gmail.com)
# Version: 0.8.7b
#
# If altering the code, please keep this comment box at least. Also, please
# comment all changes or additions with two pound signs (##), so I can tell what's
# been changed and what hasn't. Adding another comment box below this one with your
# name will insure any additions or changes you made that make it into the next version
# will be credited to you. Preferably, you'd leave your email and a little description
# of your changes, but that's not absolutely needed.
#
# License:
# All code and work contained within this file and folder and package is open for
# use, however please include at least a credit to me and any other coders working
# on this project.
#
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/

##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#
##
## Gabriel Lazarini Baptistussi (gabrielbap1@gmail.com)
##
## I just made a small change in localclasses.Enemy.move(), now the enemies
## have a different picture for each direction they are moving.
##
##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

import sys
import pygame
from pygame.locals import *
from localdefs import *
from localclasses import *
from SenderClass import Sender
import MainFunctions
import time
import MainMenu

def main():
    pygame.init()
    print "Pygame Initialized"
    pygame.display.set_caption("PyGame Tower Defence Game")
    pygame.mouse.set_visible(1)
    #localdefs: mapvar = Map()
    
    print "Map Object Generated"
    screen = pygame.display.set_mode((scrwid,scrhei))
    print "Display Initialized"
    clock = pygame.time.Clock()

    player.start()
    player.addScreen(screen,clock)

    background = mapvar.loadMap((scrwid,scrhei),MainMenu.main(screen,clock))

    genEnemyImageArray()
    run=True #Run loop
    wavenum = 0
    selected = None #Nothing is selected

    MainFunctions.makeIcons()
    
    print "Begin Play Loop!!!"

    font = pygame.font.Font(None,20)
    speed = 3
    frametime = speed/30.0
    while run:
#        timehold = list()
        starttime = time.time()
#        temptime = time.time()

        MainFunctions.tickAndClear(screen, clock, background, frametime)
#        timehold.append(("tAC",time.time()-temptime))
#        temptime = time.time()

        MainFunctions.workSenders(frametime)
#        timehold.append(("wSe",time.time()-temptime))
#        temptime = time.time()

        MainFunctions.workTowers(screen,frametime)
#        timehold.append(("wTo",time.time()-temptime))
#        temptime = time.time()

        MainFunctions.dispExplosions(screen,frametime)
#        timehold.append(("dEx",time.time()-temptime))
#        temptime = time.time()

        MainFunctions.dispText(screen,wavenum)
#        timehold.append(("dTe",time.time()-temptime))
#        temptime = time.time()

        MainFunctions.workEnemies(screen,frametime)
#        timehold.append(("wEn",time.time()-temptime))
#        temptime = time.time()

        screen,selected,wavenum,speed,timedel = MainFunctions.workEvents(screen, frametime, selected, wavenum, Sender, speed,pygame.font.Font(None,30),pygame.font.Font(None,25))
#        timehold.append(("wEv",time.time()-temptime))
#        temptime = time.time()

        starttime += timedel

        MainFunctions.dispStructures(screen,pygame.mouse.get_pos())
#        timehold.append(("dSt",time.time()-temptime))
#        temptime = time.time()

        screen.blit(mapvar.baseimg,mapvar.baserect)

        if selected and selected.__class__ == Icon:
            MainFunctions.selectedIcon(screen, selected)
#            timehold.append(("sIc",time.time()-temptime))
#            temptime = time.time()

        if selected and Tower is selected.__class__:
            MainFunctions.selectedTower(screen,selected,pygame.mouse.get_pos())
#            timehold.append(("sTo",time.time()-temptime))
#            temptime = time.time()

        screen.blit(openbuttoninfo[0],openbuttoninfo[1])

        MainFunctions.dispIcons(screen, pygame.mouse.get_pos(), font, frametime)
#        timehold.append(("dIc",time.time()-temptime))

        pygame.display.flip()

        frametime = (time.time() - starttime) * speed
#        timehold.sort(key=lambda x: x[1])
#        timehold.reverse()
#        print timehold

main()

#Thanks to everyone who looks over this code, or tests this thing out. Feel free
#to contact me at the email address listed above with any questions, comments, or
#your own set of changes. I've wanted to do a game like this for a while, so I'll
#stay committed as long as it has some interest in the community.

#Have a nice day :)