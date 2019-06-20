import pygame
import random
import bullet

invdirection = [2, 3, 0, 1]

class Tank():
    def __init__(self, pebool, gmap, num):
        self.pebool = pebool
        if pebool:
            self.x = 1
            self.y = 1
            self.direction = 0  # 0: right, 1: dawn, 2: left, 3: up
            self.speed = 0.2
        else:
            while 1:
                x = random.randint(11, gmap.gridsize[0] - 1)
                y = random.randint(11, gmap.gridsize[1] - 1)
                if gmap.grid[x][y] == ".":
                    self.x = x
                    self.y = y
                    break
            self.direction = random.randint(0, 3)
            self.speed = 0.1
        self.id = num
        
    def setDirection(self, direction):
        self.direction = direction
    
    def getPosition(self):
        return self.x, self.y
        
    def getId(self):
        return self.id
            
    def move(self, gmap, player, enemies):
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
            return False
        else:
            if player:
                if self.collisionTank(x, y, player):
                    self.x = x
                    self.y = y
                    return True
                check = True
                for enemy in enemies:
                    if enemy.id == self.id:
                        continue
                    if self.collisionTank(x, y, enemy):
                        check = False
                        break
                if check:
                    self.x = x
                    self.y = y
            else:
                self.x = x
                self.y = y
                for enemy in enemies:
                    if self.collisionTank(x, y, enemy):
                        return True
        return False
        
    def collision(self, x, y, gmap):
        e = 0.00000001
        ix = int(x)
        iy = int(y)
        if gmap.grid[ix][iy] == "x" or gmap.grid[ix][iy] == "o" or gmap.grid[ix][iy] == "r":
            return True
        if (x - ix) > e:
            if gmap.grid[ix + 1][iy] == "x" or gmap.grid[ix + 1][iy] == "o" or gmap.grid[ix + 1][iy] == "r":
                return True
        if (y - iy) > e:
            if gmap.grid[ix][iy + 1] == "x" or gmap.grid[ix][iy + 1] == "o" or gmap.grid[ix][iy + 1] == "r":
                return True
        if (x - ix) > e and (y - iy) > e:
            if gmap.grid[ix + 1][iy + 1] == "x" or gmap.grid[ix + 1][iy + 1] == "o" or gmap.grid[ix + 1][iy + 1] == "r":
                return True
        return False
        
    def collisionTank(self, x, y, tank):
        if abs(x - tank.x) < 1 and abs(y - tank.y) < 1:
            return True
        return False
    
    def shoot(self, bcount):
        if self.direction == 0:
            return bullet.Bullet(self.pebool, self.direction, self.x + 1, self.y + 0.5, bcount)
        elif self.direction == 1:
            return bullet.Bullet(self.pebool, self.direction, self.x + 0.5, self.y + 1, bcount)
        elif self.direction == 2:
            return bullet.Bullet(self.pebool, self.direction, self.x, self.y + 0.5, bcount)
        elif self.direction == 3:
            return bullet.Bullet(self.pebool, self.direction, self.x + 0.5, self.y, bcount)