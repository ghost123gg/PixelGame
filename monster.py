import pygame
import random
import math

def trunc(f, n):
    slen = len('%.*f' % (n, f))
    try:
        return int(str(f)[:slen])
    except:
        return int(str(f)[:slen-1])

class Monster(pygame.sprite.Sprite):
    def __init__(self, image, speed, initial_position, level):
        pygame.sprite.Sprite.__init__(self)
        self.level=level
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=initial_position
        self.next_update_time = 0
        if random.randint(0,1)==0:
            self.xspeed=-4
        else:
            self.xspeed=4
        if random.randint(0,1)==0:
            self.yspeed=-4
        else:
            self.yspeed=4
        self.nextTurnTime=2000
        self.readyx=0
        self.speed=4

    def update(self, current_time, bottom, playerx, playery, timing):
        diffX = float(playerx - self.rect.left)+2
        diffY = float(playery - self.rect.top)+2
        diffLength = math.sqrt(diffX**2 + diffY**2)
        if diffLength>5:
            self.xspeed = diffX / diffLength * self.speed
            self.yspeed = diffY / diffLength * self.speed
            return diffLength
        else:
            return 0
