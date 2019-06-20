import pygame
import math

class Bullet():
    def __init__(self, pebool, direction, x, y, num):
        self.pebool = pebool
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 0.3
        self.hitobject = None
        self.hitpos = None
        self.id = num
        self.hitten = False
        self.r = 5
        if pebool:
            self.color = (255, 255, 255)
        else:
            self.color = (255, 0, 0)
            
    def getHitInfo(self):
        return self.hitobject, self.hitpos
        
    def getId(self):
        return self.id
        
    def getPos(self):
        return (self.x, self.y)
        
    def getColor(self):
        return self.color
        
    def getR(self):
        return self.r
        
    def move(self, gmap, player, enemies, bullets):
        if self.hitten:
            return False
        xy = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        x = self.x + self.speed * xy[self.direction][0]
        y = self.y + self.speed * xy[self.direction][1]
        if self.collision(x, y, gmap):
            if self.direction == 0:
                self.x = int(x)
            elif self.direction == 1:
                self.y = int(y)
            elif self.direction == 2:
                self.x = int(x) + 1
            elif self.direction == 3:
                self.y = int(y) + 1
            return True
        else:
            for bul in bullets:
                if bul.id == self.id:
                    continue
                if self.collisionBullet(x, y, bul, gmap.unit):
                    self.hitobject = "b"
                    self.hitpos = bul.id
                    return True
            if self.pebool:
                for enemy in enemies:
                    if self.collisionTank(x, y, enemy, gmap.unit):
                        self.hitobject = "e"
                        self.hitpos = enemy.id
                        return True
                self.x = x
                self.y = y
            else:
                if self.collisionTank(x, y, player, gmap.unit):
                    self.hitobject = "p"
                    return True
                for enemy in enemies:
                    if self.collisionTank(x, y, enemy, gmap.unit):
                        return True
                self.x = x
                self.y = y
        return False
        
    def collision(self, x, y, gmap):
        e = 0.00000001
        ix = int(x)
        iy = int(y)
        if gmap.grid[ix][iy] == "x":
            return True
        if gmap.grid[ix][iy] == "o":
            self.hitobject = "o"
            self.hitpos = (ix, iy)
            return True
        if (x - ix) > e:
            if gmap.grid[ix + 1][iy] == "x":
                return True
            if gmap.grid[ix + 1][iy] == "o":
                self.hitobject = "o"
                self.hitpos = (ix + 1, iy)
                return True
        if (y - iy) > e:
            if gmap.grid[ix][iy + 1] == "x":
                return True
            if gmap.grid[ix][iy + 1] == "o":
                self.hitobject = "o"
                self.hitpos = (ix, iy + 1)
                return True
        if (x - ix) > e and (y - iy) > e:
            if gmap.grid[ix + 1][iy + 1] == "x":
                return True
            if gmap.grid[ix + 1][iy + 1] == "o":
                self.hitobject = "o"
                self.hitpos = (ix + 1, iy + 1)
                return True
        return False
        
    def collisionBullet(self, x, y, bul, unit):
        distance = math.sqrt(math.pow((bul.x - x) * unit, 2) + math.pow((bul.y - y) * unit, 2))
        if distance < (self.r + bul.r):
            return True
        return False
        
    def collisionTank(self, x, y, tank, unit):
        distance = math.sqrt(math.pow((tank.x + 0.5 - x) * unit, 2) + math.pow((tank.y + 0.5 - y) * unit, 2))
        if distance < (self.r + unit * 0.5):
            return True
        return False