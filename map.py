import pygame

class Map():
    def __init__(self, windowsize):
        grid = []
        for i in range(windowsize[0]):
            grid.append([])
            for j in range(windowsize[1]):
                grid[i].append(".")
        self.grid = grid
        self.unit = 10