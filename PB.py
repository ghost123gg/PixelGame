import random
import os, pygame, sys
from pygame.locals import *
import spritesheet
import sound
import math
from monster import Monster
from map import Level
import sys
import os
#Utility functions
def find(f, seq):
    i=0
    for item in seq:
        if item==f:
            return i
        i+=1

def ispressing(buttontopleft, buttonbottomright, mousex, mousey):
    if mousex>buttontopleft[0] and mousex<buttonbottomright[0]:
        if mousey>buttontopleft[1] and mousey<buttonbottomright[1]:
            return True
    return False
def trunc(f, n):
    slen = len('%.*f' % (n, f))
    try:
        return int(str(f)[:slen])
    except:
        return int(str(f)[:slen-1])

#----End of Utility Functions----#
class PixelBuild:
    def __init__(self):
        #initialize timing variable
        self.timing=0
        # initialize sounds
        pygame.mixer.init()
        #looping
        self.looping=True
        #set variable shop for shop image
        self.shop = pygame.image.load("sprites/shop.bmp")
        self.shop.set_colorkey((255,255,255))
        #initialize if running or not
        self.running = True
        #variable with players coins
        self.coins=0
        #cheating!!!!
        self.godmode=False
        #sounds...
        self.placesound=pygame.mixer.Sound("sounds/place.wav")
        self.deletesound=pygame.mixer.Sound("sounds/delete.wav")
        #game icon
        self.icon = pygame.image.load("sprites/game.bmp")
        #set alpha color
        self.icon.set_colorkey((0,0,0))
        #set icon
        pygame.display.set_icon(self.icon)
        #initialize level
        self.level = Level()
        try:
    #try to load file
            self.level.loadFile("level0000.map")
        except:
            # if i cant load file create it from default.map
            os.system ("cp %s %s" % ("default.map", "level0000.map"))
            #load the file i created
            self.level.loadFile("level0000.map")
            #Spawn either a forest or clearing
            if random.randint(1,8)==1:
                for i in range(2):
                    self.level.spawntree()
                del(i)
            else:
                for i in range(5):
                    self.level.spawntree()
                del(i)
        # Initialize pygame
        pygame.init()
        # Initialize pygame window size 800 x 600
        self.screen = pygame.display.set_mode((800, 600))
        # Set window title
        pygame.display.set_caption('PixelBuild')
        # Run titlescreen scene
        self.titlescreen()
    def titlescreen(self):
        #get the rectangle from the icom
        iconRect = self.icon.get_rect()
        #set icon into the center
        iconRect.centerx = self.screen.get_rect().centerx
        #set the y value of icon
        iconRect.y=0
        #blit the icon onto the screen
        self.screen.blit(self.icon, iconRect)

        #set title
        font1 = pygame.font.Font(None, 72)
        text1 = font1.render('PixelBuild', True, (255, 255, 255))
        textRect1 = text1.get_rect()
        textRect1.centerx = self.screen.get_rect().centerx
        textRect1.y = 100
        self.screen.blit(text1, textRect1)

        #set instructions
        font2 = pygame.font.Font(None, 17)
        text2 = font2.render('Press <Enter> To Play', True, (255, 255, 255))
        textRect2 = text2.get_rect()
        textRect2.centerx = self.screen.get_rect().centerx
        textRect2.y = 150
        self.screen.blit(text2, textRect2)
        # Update the screen
        pygame.display.update()
        # Wait for enter to be pressed
        # The user can also quit
        waiting=True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    waiting=False
                    running=False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
        self.loading()
    def loading(self):
        #make spritesheet
        self.ss=spritesheet.spritesheet("sprites/spritesheet.bmp")
        #render the background
        self.background = self.level.render(self.ss)
        self.background.set_colorkey((255, 255, 255))
        pygame.display.set_caption('PixelBuild')
        self.character=self.ss.image_at(pygame.rect.Rect(96,64, 32, 32), colorkey = (255, 255, 255))
        self.carrying = self.ss.image_at(pygame.rect.Rect(0,512, 32, 32), colorkey = (255, 255, 255))
        #Create The Backgound
        self.background.blit(self.character, (400, 300))
        self.screen.blit(self.background, (-100, -100))
        self.clock = pygame.time.Clock()
        pygame.display.flip()
        #ss.image_at(pygame.Rect(32, 96, 32, 32))
        self.monsters=[]
        monsternum=25
        if self.level.monsters=={}:
            for mon in range(monsternum):
                self.monsters.append(Monster(ss.image_at(pygame.rect.Rect(96, 288, 32, 32), colorkey = (255, 255, 255)), 5, [random.randint(10, 1280), random.randint(10, 1280)], level))
            del(mon)
        else:
            for mon in self.level.monsters:
                self.monsters.append(Monster(self.ss.image_at(pygame.rect.Rect(96, 288, 32, 32), colorkey = (255, 255, 255)), 5, [int(self.level.monsters[mon]["x"]), int(self.level.monsters[mon]["y"])], self.level))
            del(mon)
        self.defaultmap=open("default.map", "r").read()
        self.xoffset=0
        self.yoffset=0
        self.selected=""
        self.monsterspeed=7
        self.monsterdirection=random.randint(0,4)
        self.inv=['1', '2', '3', '4', '5', '6','7', '8', '9','0', 'q', 'b', 't', 'i', 'd', 'g', 'tr', 'w', "wf"]
        self.invcount=[100, 100,100, 100,100, 100, 100,100, 100,100, 100,0, 0, 0, 1, 0, 5, 0, 0]
        self.currentselected=1
        self.currentselectednum=self.invcount[self.currentselected-1]
        self.playerx=400
        self.playery=300
        self.chunk=(0,0,0,0)
        pygame.key.set_repeat(1,25)
        self.background = self.level.render(self.ss)
        self.background.set_colorkey((255, 255, 255))
        self.currentbox=pygame.Surface((48, 64))
        self.currentbox.fill((255,255,255))
        self.running=True
        self.dead=False
        self.update()
    def update(self):
        #update shop item
        shopitem=self.ss.image_at(pygame.rect.Rect(((int(self.level.key[str(self.inv[self.currentselected-1])]['tile'].split(", ")[0])-1)*32, (int(self.level.key[str(self.inv[self.currentselected-1])]['tile'].split(", ")[1])-1)*32, 32, 32)))
        # client.Loop()
        #if len(self.blockdata)>1:
        #    print block
        self.currentbox.fill((255,255,255))
        self.currentselectednum=self.invcount[self.currentselected-1]
        if self.dead:
            self.looping=False
        self.time = pygame.time.get_ticks()

        self.screen.fill(0)
        self.screen.blit(self.background, (0+self.xoffset, 0+self.yoffset))
        selected = shopitem
        self.currentbox.blit(selected, (8,24))
        font = pygame.font.Font(None, 13)

        # Render the text

        text = font.render('Currently', True, (0,0, 0), (255, 255, 255))
        text1 = font.render('Selected', True, (0,0, 0), (255, 255, 255))
        text2 = font.render(str(self.currentselectednum), True, (0,0, 0), (255, 255, 255))
        self.currentbox.blit(text, (4,4))
        self.currentbox.blit(text1, (8,14))
        text2.set_colorkey((255, 255, 255))
        self.currentbox.blit(text2, (20 ,56))

        self.screen.blit(self.currentbox, (0, 536))
        self.screen.blit(self.character, (400, 300))
        self.screen.blit(self.carrying, (400, 300))
        self.screen.blit(self.shop, (117, 10))
        font2 = pygame.font.Font("fonts/Minecraftia.ttf", 14)
        cointext = font2.render(str(self.coins), True, (0, 0, 0), (127, 127, 127))
        self.screen.blit(cointext, (271, 35))
        self.screen.blit(selected, (132, 18))
        pygame.display.flip()
        if not self.dead:
            self.background.fill(0)
        self.chunk1=[str(self.chunk[0]), str(self.chunk[1]), str(self.chunk[2]), str(self.chunk[3])]
        self.timing+=1
        print(self.monsters)
        for mon in self.monsters:
            self.monsterstat=mon.update(self.time, 150, self.playerx, self.playery, self.timing)
            if self.monsterstat==0 and self.godmode==False:
                self.dead=True
            elif self.monsterstat>0:
                self.coins+=1

        self.background = self.level.render(self.ss)
        self.background.set_colorkey((255, 255, 255))

        for mon in self.monsters:
            self.background.blit(mon.image, (mon.rect[0],mon.rect[1]))

        for event in pygame.event.get():
            if event.type==QUIT:
                self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                self.level.writeConfig("level"+"".join(self.chunk1)+".map", self.monsters,True, invcount, player=(self.playerx, self.playery))
                pygame.quit()
                running=False
                sys.exit()
                break
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    if self.playery>0:
                        if self.level.getTile(trunc((self.playerx+16)/32,0), trunc((self.playery+4)/32,0))["name"]=="floor":
                            self.yoffset+=5
                            self.playery-=5
                        elif self.level.getTile(trunc((self.playerx+16)/32,0), trunc((self.playery+4)/32,0))["name"]=="pool":
                            self.yoffset+=3
                            self.playery-=3
                    else:
                        self.level.writeConfig("level"+"".join(self.chunk1)+".map", self.monsters)
                        #1280, -980, 2
                        screen.fill(0)
                        self.playery=1280
                        self.yoffset=-980
                        chunkb=chunk
                        if chunk[2]==0:
                            chunk=[chunk[0]+1, chunk[1], chunk[2], chunk[3]]
                        else:
                            chunk=[chunk[0], chunk[1], chunk[2]-1, chunk[3]]
                        self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        if os.path.exists("level"+"".join(self.chunk1)+".map")!=True:
                            open("level"+"".join(self.chunk1)+".map","w").write(defaultmap)
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")
                            if random.randint(1,2)==1:
                                for i in range(5):
                                    level.spawntree()
                            else:
                                for i in range(2):
                                    self.level.spawntree()
                            del(i)
                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                        else:
                            chunk=chunkb
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.writeConfig("level"+"".join(self.chunk1)+".map", [])
                            if chunk[2]==0:
                                chunk=[chunk[0]+1, chunk[1], chunk[2], chunk[3]]
                            else:
                                chunk=[chunk[0], chunk[1], chunk[2]-1, chunk[3]]
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")

                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()

                if event.key == K_s:
                    try:
                        if self.level.getTile(trunc((self.playerx+16)/32,0), trunc((self.playery+25)/32,0))["name"]=="floor":
                            self.yoffset-=5
                            self.playery+=5
                        elif self.level.getTile(trunc((self.playerx+16)/32,0), trunc((self.playery+25)/32,0))["name"]=="pool":
                            self.yoffset-=3
                            self.playery+=3
                    except KeyError:
                        self.level.writeConfig("level"+"".join(self.chunk1)+".map", self.monsters)
                        screen.fill(0)
                        self.playery=0
                        self.yoffset=300
                        chunkb=chunk
                        if chunk[0]==0:
                            chunk=[chunk[0], chunk[1], chunk[2]+1, chunk[3]]
                        else:
                            chunk=[chunk[0]-1, chunk[1], chunk[2], chunk[3]]
                        self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        if os.path.exists("level"+"".join(self.chunk1)+".map")!=True:
                            open("level"+"".join(self.chunk1)+".map","w").write(defaultmap)
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")
                            if random.randint(1,2)==1:
                                for i in range(5):
                                    self.level.spawntree()
                            else:
                                for i in range(2):
                                    self.level.spawntree()
                            del(i)
                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                        else:
                            chunk=chunkb
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]

                            self.level.writeConfig("level"+"".join(self.chunk1)+".map", [])
                            if chunk[0]==0:
                                chunk=[chunk[0], chunk[1], chunk[2]+1, chunk[3]]
                            else:
                                chunk=[chunk[0]-1, chunk[1], chunk[2], chunk[3]]
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")

                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                if event.key == K_a:
                    if self.level.getTile(trunc((self.playerx+12)/32,0), trunc((self.playery+16)/32,0))["name"]=="floor" and self.playerx>-5:
                        self.playerx-=5
                        self.xoffset+=5
                    elif self.level.getTile(trunc((self.playerx+12)/32,0), trunc((self.playery+16)/32,0))["name"]=="pool":
                        self.xoffset+=3
                        self.playerx-=3
                    if self.playerx<=-5:
                        self.level.writeConfig("level"+"".join(self.chunk1)+".map", self.monsters)
                        screen.fill(0)
                        #Figure out xoffset
                        self.playerx=900
                        self.xoffset=-496
                        chunkb=chunk
                        if chunk[3]==0:
                            chunk=[chunk[0], chunk[1]+1, chunk[2], chunk[3]]
                        else:
                            chunk=[chunk[0], chunk[1], chunk[2], chunk[3]-1]
                        self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        if os.path.exists("level"+"".join(self.chunk1)+".map")!=True:
                            open("level"+"".join(self.chunk1)+".map","w").write(defaultmap)
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")
                            if random.randint(1,2)==1:
                                for i in range(5):
                                    self.level.spawntree()
                            else:
                                for i in range(2):
                                    self.level.spawntree()
                            del(i)
                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                        else:
                            chunk=chunkb
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.writeConfig("level"+"".join(self.chunk1)+".map", [])
                            if chunk[3]==0:
                                chunk=[chunk[0], chunk[1]+1, chunk[2], chunk[3]]
                            else:
                                chunk=[chunk[0], chunk[1], chunk[2], chunk[3]-1]
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")

                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                if event.key == K_d:
                    try:
                        if self.level.getTile(trunc((self.playerx+25)/32,0), trunc((self.playery+16)/32,0))["name"]=="floor" and self.playerx<40*32:
                            self.xoffset-=5
                            self.playerx+=5
                        elif self.level.getTile(trunc((self.playerx+25)/32,0), trunc((self.playery+16)/32,0))["name"]=="pool":
                            self.xoffset-=3
                            self.playerx+=3
                    except KeyError:
                        self.level.writeConfig("level"+"".join(self.chunk1)+".map", self.monsters)
                        screen.fill(0)
                        #Figure out xoffset
                        self.playerx=0
                        self.xoffset=400
                        chunkb=chunk
                        if chunk[1]==0:
                            chunk=[chunk[0], chunk[1], chunk[2], chunk[3]+1]
                        else:
                            chunk=[chunk[0], chunk[1]-1, chunk[2], chunk[3]]
                        self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        if os.path.exists("level"+"".join(self.chunk1)+".map")!=True:
                            open("level"+"".join(self.chunk1)+".map","w").write(defaultmap)
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")
                            if random.randint(1,2)==1:
                                for i in range(5):
                                    self.level.spawntree()
                            else:
                                for i in range(2):
                                    self.level.spawntree()
                            del(i)
                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                        else:
                            chunk=chunkb
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.writeConfig("level"+"".join(self.chunk1)+".map", [])
                            if chunk[1]==0:
                                chunk=[chunk[0], chunk[1], chunk[2], chunk[3]+1]
                            else:
                                chunk=[chunk[0], chunk[1]-1, chunk[2], chunk[3]]
                            self.chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                            self.level.loadFile("level"+"".join(self.chunk1)+".map")

                            background = self.level.render(ss)
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                            screen.blit(character, (400, 300))
                            pygame.display.flip()
                if event.key == K_1:
                    currentselected=1
                if event.key == K_2:
                    currentselected=2
                if event.key == K_3:
                    currentselected=3
                if event.key == K_4:
                    currentselected=4
                if event.key == K_5:
                    currentselected=5
                if event.key == K_6:
                    currentselected=6
                if event.key == K_7:
                    currentselected=7
                if event.key == K_8:
                    currentselected=8
                if event.key == K_9:
                    currentselected=9
                if event.key == K_0:
                    currentselected=0
            #4 is down and 5 is up
            if event.type == MOUSEBUTTONDOWN and event.button==4:
                if currentselected==0:
                    currentselected=len(inv)
                else:
                    currentselected-=1
            elif event.type == MOUSEBUTTONDOWN and event.button==5:
                if currentselected==len(inv):
                    currentselected=0
                else:
                    currentselected+=1
            elif event.type==MOUSEBUTTONDOWN and event.button==1:
                if ispressing((122,22), (129, 46), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    if currentselected==0:
                        currentselected=len(inv)
                    else:
                        currentselected-=1
                elif ispressing((167,22), (174, 42), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    if currentselected==len(inv):
                        currentselected=0
                    else:
                        currentselected+=1
                elif ispressing((358,16), (501, 52), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    if coins>0:
                        coins-=1
                        self.invcount[currentselected-1]+=5
                else:
                    if self.invcount[currentselected-1]>0:
                        placesound.play()
                        mouse=[pygame.mouse.get_pos()[0]-400, pygame.mouse.get_pos()[1]-300]
                        try:
                            if self.level.getTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0))["name"]=="floor":
                                if self.level.getTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), False)!=inv[currentselected-1]:
                                    self.level.setTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), str(inv[currentselected-1]))
                                    # client.Client.newdata=["placeblock", []]
                                    background = self.level.render(ss)
                                    background.set_colorkey((255, 255, 255))
                                    screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                                    screen.blit(self.currentbox, (0, 536))
                                    screen.blit(character, (400, 300))
                                    screen.blit(shop, (117, 10))
                                    screen.blit(cointext, (550, 25))
                                    invcount[currentselected-1]-=1
                                    for mon in self.monsters:
                                        background.blit(mon.image, (mon.rect[0],mon.rect[1]))
                                    pygame.display.flip()

                        except:
                            pass
            elif event.type==MOUSEBUTTONDOWN and event.button==3:
                try:
                    deletesound.play()
                    mouse=[pygame.mouse.get_pos()[0]-400, pygame.mouse.get_pos()[1]-300]
                    invcount[find(self.level.getTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), False), inv)]+=1
                    if self.level.getTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0))['name'] in ['trap', 'wall']:
                        self.level.setTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), "g")
                    else:
                        self.level.setTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), "7")

                    background = self.level.render(ss)
                    background.set_colorkey((255, 255, 255))
                    screen.blit(background, (0+self.xoffset, 0+self.yoffset))
                    screen.blit(self.currentbox, (0, 536))
                    screen.blit(character, (400, 300))
                    for mon in self.monsters:
                        background.blit(mon.image, (mon.rect[0],mon.rect[1]))
                    pygame.display.flip()
                except TypeError:
                    if self.level.getTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), False)=="le":
                        invcount[find("4",inv)]+=1
                        self.level.setTile(trunc(((mouse[0]*1.0/32))+self.playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+self.playery*1.0/32,0), "g")
        if self.looping:
            self.update()
p=PixelBuild()
