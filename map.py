#Handles the map parsing
import configparser
import pygame
import time
import gzip
import random
import os
import io
from configobj import ConfigObj
class Level(object):
    def spawntree(self):
        x = random.randint(5, self.width-5)
        y = random.randint(5, self.height-5)
        self.setTile(x,y,"w")
        self.setTile(x,y-1,"w")
        self.setTile(x,y-2,"le")
        self.setTile(x,y-3,"le")
        self.setTile(x,y-4,"le")
        self.setTile(x,y-5,"le")
        self.setTile(x+1,y-2,"le")
        self.setTile(x+1,y-3,"le")
        self.setTile(x+1,y-4,"le")
        self.setTile(x+1,y-5,"le")
        self.setTile(x-1,y-2,"le")
        self.setTile(x-1,y-3,"le")
        self.setTile(x-1,y-4,"le")
        self.setTile(x-1,y-5,"le")
        self.setTile(x-2,y-3,"le")
        self.setTile(x-2,y-4,"le")
        self.setTile(x+2,y-3,"le")
        self.setTile(x+2,y-4,"le")
        return x
    def loadFile(self, filename="level.map"):
        self.map = []
        self.key = {}
        self.monsters = {}
        parser = configparser.ConfigParser()
        f = io.TextIOWrapper(gzip.open(filename, 'rb'))
        parser.read_file(f, filename)
        self.map = parser.get("level", "map").replace('""', "").replace("'''","").split("\n")
        tmpMap = []
        for line in self.map:
            tmpMap.append(line.split(";"))
        self.map = tmpMap
        self.map=self.map[:-1]
        for section in parser.sections():
            if section.startswith("mon"):
                desc = dict(parser.items(section))
                self.monsters[section] = desc

        self.key={'wf':{'tile':'3, 16', 'name':'floor'},'le':{'tile':'2, 13', 'name':'wall'}, 'w':{'tile':'1, 9', 'name':'wall'}, 'tr':{'tile':'4, 16', 'name':'trap'},'g':{'tile':'2, 5', 'name':'floor'},'q': {'tile': '4, 8', 'name': 'pool'}, 'b': {'tile': '3, 4', 'name': 'wall'}, 'd': {'tile': '4, 14', 'name': 'floor'}, 'cd': {'tile': '4, 13', 'name': 'floor'}, 'i': {'tile': '1, 13', 'name': 'ice'}, '1': {'tile': '1, 1', 'name': 'wall'}, '0': {'tile': '2, 3', 'name': 'wall'}, '3': {'tile': '3, 1', 'name': 'wall'}, '2': {'tile': '2, 1', 'name': 'wall'}, '5': {'tile': '1, 2', 'name': 'wall'}, 't': {'tile': '2, 8', 'name': 'floor'}, '7': {'tile': '3, 2', 'name': 'floor'}, '6': {'tile': '2, 2', 'name': 'wall'}, '9': {'tile': '1, 3', 'name': 'wall'}, '8': {'tile': '4, 2', 'name': 'wall'}, '4': {'tile': '4, 1', 'name': 'wall'}}
        try:
            self.inventory=parser.get("player", "inventory")
            self.inventory = self.inventory.split(", ")
            tmpinv = []
            for xyz in self.inventory:
                tmpinv.append(int(xyz))
            self.inventory=tmpinv
            del(tmpinv)
        except:
            self.inventory=[100, 100,100, 100,100, 100, 100,100, 100,100, 10000,20000, 100, 100, 100, 100, 100]
        try:
            self.playerx=parser.get("player", "x")
            self.playery=parser.get("player", "y")
            print("Found player")
        except:
            self.playerx, self.playery=400, 300
        self.width = len(self.map[0])
        self.height = len(self.map)

    def getTile(self, x, y, a=True):
        if a:
            try:
                char = self.map[y][x]
            except IndexError:
                return {}
            try:
                return self.key[char]
            except KeyError:
                return {}
        else:
            try:
                return self.map[y][x]
            except IndexError:
                return {}

    def is_wall(self, x, y):
        if self.getTile(x, y)["name"]!="floor":
            return True
        else:
            return False


    def renderRow(self, row, spritesheet):
        index=0
        image = pygame.Surface((self.width*32, 32))
        for column in row:
            coord = self.key[column]["tile"].split(", ")
            tile = spritesheet.image_at(pygame.rect.Rect((int(coord[0])-1)*32, (int(coord[1])-1)*32, 32, 32))
            image.blit(tile, (index*32, 0))
            index+=1
        return image

    def render(self, spritesheet):
        index = 0
        image = pygame.Surface((self.width*32, self.height*32))
        for y in self.map:
            image.blit(self.renderRow(y, spritesheet), (0, index*32))
            index+=1
        return image

    def setTile(self, x, y, id):
        if x<30 and x>=0 and y<41 and y>=0:
            self.map[y][x]=id

    def writeConfig(self, filename, monsters, savemon=True, invcount=None, player=None):
        config = ConfigObj()
        config.filename=filename
        map1=""
        index=0
        config["player"]={}
        if invcount!=None:
            print("inv:",invcount)
            print("player:",player)
            config["player"]={"inventory":invcount}
        if player!=None:
            config["player"]=dict(config["player"],**{"x":player[0]})
            config["player"]=dict(config["player"],**{"y":player[1]})
        if savemon:
            for mon in monsters:
                config["mon"+str(index)]={"x":mon.rect.left, "y":mon.rect.top}
                index+=1
        yfinal = ""
        for y in self.map:
            for x in y:
                yfinal+=x+";"
            map1=map1+yfinal[:-1]+"\n    "
            yfinal=''
        config["level"]={"tileset":"abc", "map":map1}
        config.filename="temp.text"
        config.write()
        level124=open("temp.text", "r")
        f_out = gzip.open(filename, 'w')
        f_out.writelines(level124)
        f_out.close()
        level124.close()
