import pygame
import random

class Map():
    def __init__(self, windowsize):
        self.unit = 25
        self.gridsize = (int(windowsize[0] / self.unit), int(windowsize[1] / self.unit))
        grid = []
        for i in range(self.gridsize[0]):
            grid.append([])
            for j in range(self.gridsize[1]):
                grid[i].append(".")
        self.grid = grid
        self.item = False
        
    def set_map(self, mapfile):
        f = open(mapfile, "r+")
        data = f.readlines()
        for i in range(self.gridsize[0]):
            for j in range(self.gridsize[1]):
                if i == 0:
                    self.grid[i][j] = "x"
                elif i == self.gridsize[0] - 1:
                    self.grid[i][j] = "x"
                else:
                    if j == 0:
                        self.grid[i][j] = "x"
                    elif j == self.gridsize[1] - 1:
                        self.grid[i][j] = "x"
                    else:
                        self.grid[i][j] = data[i][j - 1]
        self.check_cont()
        self.grid[1][1] = "."
        return
        
    def random_map(self):
        # wall, obstacle, river, grass
        for i in range(self.gridsize[0]):
            for j in range(self.gridsize[1]):
                if i == 0:
                    self.grid[i][j] = "x"
                elif i == self.gridsize[0] - 1:
                    self.grid[i][j] = "x"
                else:
                    if j == 0:
                        self.grid[i][j] = "x"
                    elif j == self.gridsize[1] - 1:
                        self.grid[i][j] = "x"
                    else:
                        num = random.randint(1, 500)
                        if num <= 50:
                            self.grid[i][j] = "o"
                        elif num > 50 and num <= 80:
                            self.grid[i][j] = "r"
                        elif num > 80 and num <= 100:
                            self.grid[i][j] = "g"
        self.check_cont()
        self.grid[1][1] = "."
        return
    
    def check_cont(self):
        for i in range(1, self.gridsize[0] - 1):
            for j in range(1, self.gridsize[1] - 1):
                count = 0
                if self.grid[i - 1][j] == "x" or self.grid[i - 1][j] == "r":
                    count += 1
                if self.grid[i][j - 1] == "x" or self.grid[i][j - 1] == "r":
                    count += 1
                if self.grid[i][j + 1] == "x" or self.grid[i][j + 1] == "r":
                    count += 1
                if self.grid[i + 1][j] == "x" or self.grid[i + 1][j] == "r":
                    count += 1
                while count == 4:
                    num = random.randint(1, 4)
                    if num == 1 and self.grid[i - 1][j] == "r":
                        self.grid[i - 1][j] = "."
                        count -= 1
                    if num == 2 and self.grid[i][j - 1] == "r":
                        self.grid[i][j - 1] = "."
                        count -= 1
                    if num == 3 and self.grid[i][j + 1] == "r":
                        self.grid[i][j + 1] = "."
                        count -= 1
                    if num == 4 and self.grid[i + 1][j] == "r":
                        self.grid[i + 1][j] = "."
                        count -= 1
        return
        
    def destroyObstacle(self, pos):
        self.grid[pos[0]][pos[1]] = "."