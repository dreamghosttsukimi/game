import pygame

class Gui():
    def __init__(self, screen):
        self.screen = screen

    def draw(self, gmap, player, enemies, bullets):
        self.drawMap(gmap)
        self.drawTank(gmap, player)
        for enemy in enemies:
            self.drawTank(gmap, enemy)
        for bul in bullets:
            self.drawBullet(gmap, bul)
        self.drawGrass(gmap)

    def drawMap(self, gmap):
        for i in range(gmap.gridsize[0]):
            for j in range(gmap.gridsize[1]):
                if gmap.grid[i][j] == "x":
                    pygame.draw.rect(self.screen, (125, 125, 125), pygame.Rect(i * gmap.unit, j * gmap.unit, gmap.unit, gmap.unit))
                elif gmap.grid[i][j] == "o":
                    pygame.draw.rect(self.screen, (178, 34, 34), pygame.Rect(i * gmap.unit, j * gmap.unit, gmap.unit, gmap.unit))
                elif gmap.grid[i][j] == "r":
                    pygame.draw.rect(self.screen, (0, 255, 255), pygame.Rect(i * gmap.unit, j * gmap.unit, gmap.unit, gmap.unit))
        return
        
    def drawTank(self, gmap, tank):
        if tank.pebool:
            color = (107, 42, 35)
        else:
            color = (204, 204, 77)
        # 0: right, 1: dawn, 2: left, 3: up
        if tank.direction == 0:
            pygame.draw.rect(self.screen, color, pygame.Rect(tank.x * gmap.unit, tank.y * gmap.unit, gmap.unit * 0.6, gmap.unit))
            pygame.draw.rect(self.screen, color, pygame.Rect(tank.x * gmap.unit, (tank.y + 0.4) * gmap.unit, gmap.unit, 5))
        elif tank.direction == 1:
            pygame.draw.rect(self.screen, color, pygame.Rect(tank.x * gmap.unit, tank.y * gmap.unit, gmap.unit * 1, gmap.unit * 0.6))
            pygame.draw.rect(self.screen, color, pygame.Rect((tank.x + 0.4) * gmap.unit, tank.y * gmap.unit, 5, gmap.unit))
        elif tank.direction == 2:
            pygame.draw.rect(self.screen, color, pygame.Rect((tank.x + 0.4) * gmap.unit, tank.y * gmap.unit, gmap.unit * 0.6, gmap.unit))
            pygame.draw.rect(self.screen, color, pygame.Rect(tank.x * gmap.unit, (tank.y + 0.4) * gmap.unit, gmap.unit, 5))
        elif tank.direction == 3:
            pygame.draw.rect(self.screen, color, pygame.Rect(tank.x * gmap.unit, (tank.y + 0.4) * gmap.unit, gmap.unit, gmap.unit * 0.6))
            pygame.draw.rect(self.screen, color, pygame.Rect((tank.x + 0.4) * gmap.unit, tank.y * gmap.unit, 5, gmap.unit))
        return
    
    def drawBullet(self, gmap, bul):
        x, y = bul.getPos()
        pygame.draw.circle(self.screen, bul.getColor(), (int(x * gmap.unit), int(y * gmap.unit)), bul.getR())
    
    def drawGrass(self, gmap):
        for i in range(gmap.gridsize[0]):
            for j in range(gmap.gridsize[1]):
                if gmap.grid[i][j] == "g":
                    pygame.draw.rect(self.screen, (153, 230, 77), pygame.Rect(i * gmap.unit, j * gmap.unit, gmap.unit, gmap.unit))