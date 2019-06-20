import pygame
import os.path
import mymap
import tank
import random
import gui

pygame.init()
windowsize = (500, 500)
screen = pygame.display.set_mode(windowsize)
done = False
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 22)

frame = 0
button = True
nf = False
mapfile = ""
gmap = None
player = None
count = 0
nowtick = 0
gameover = False
bullets = []
bcount = 0

startt = font.render("start", True, (255, 0, 0))
startf = font.render("start", True, (0, 0, 0))
readt = font.render("connect", True, (255, 0, 0))
readf = font.render("connect", True, (0, 0, 0))
notfound = font.render("not found", True, (255, 255, 255))
text1 = font.render("player file", True, (255, 255, 255))
text2 = font.render("GAME OVER", True, (255, 0, 0))
text3 = font.render("WIN", True, (255, 255, 0))

def init_game(windowsize, count):
    gmap = mymap.Map(windowsize)
    if mapfile:
        gmap.set_map(mapfile)
    else:
        gmap.random_map()
    player = tank.Tank(True, gmap, count)
    enemynum = random.randint(1, 10)
    enemies = []
    for i in range(enemynum):
        count += 1
        enemies.append(tank.Tank(False, gmap, count))
    
    return gmap, player, enemies

def changeDirection(enemies, player):
    for enemy in enemies:
        tmp = random.randint(0, 1)
        if tmp == 0:
            x1, y1 = player.getPosition()
            x2, y2 = enemy.getPosition()
            dx = x1 - x2
            dy = y1 - y2
            direct = []
            if dx > 0:
                direct.append(0)
            elif dx < 0:
                direct.append(2)
            if dy > 0:
                direct.append(1)
            elif dy < 0:
                direct.append(3)
            if direct:
                direction = random.choice(direct)
            else:
                direction = random.randint(0, 3)
        else:
            direction = random.randint(0, 3)
        enemy.setDirection(direction)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if (frame == 20 or frame == 30) and event.type == pygame.KEYDOWN:
            frame = 0
            break
        if frame == 10 and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(player.shoot(bcount))
            bcount += 1
        if frame == 1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                frame = 0
            elif event.key == pygame.K_RETURN:
                if os.path.exists(mapfile):
                    frame = 10
                else:
                    nf = True
                    mapfile = ""
            elif event.key == pygame.K_BACKSPACE:
                mapfile = mapfile[:-1]
                nf = False
            else:
                mapfile += event.unicode
                nf = False
        if frame == 0 and event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            button = not button
        if frame == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if button:
                frame = 10
                gmap, player, enemies = init_game(windowsize, count)
                drawer = gui.Gui(screen)
                tick = int(round(pygame.time.get_ticks()/1000))
            else:
                frame = 1
            
    screen.fill((0, 0, 0))
    if frame == 0:
        if button:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(80, 400, 120, 60))
            pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(300, 400, 120, 60))
            screen.blit(startt, (113, 415))
            screen.blit(readf, (322, 415))
        else:
            pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(80, 400, 120, 60))
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(300, 400, 120, 60))
            screen.blit(startf, (113, 415))
            screen.blit(readt, (322, 415))
    elif frame == 1:
        screen.blit(text1, (200, 200))
        pygame.draw.rect(screen, (8, 37, 103), pygame.Rect(100, 250, 300, 60))
        text = font.render(mapfile, True, (255, 255, 255))
        screen.blit(text, (110, 260))
        if nf:
            screen.blit(notfound, (210, 320))
    elif frame == 10:
        bulhit = []
        for bul in bullets:
            if bul.move(gmap, player, enemies, bullets):
                bulhit.append(bul.getId())
                hitobj, hitpos = bul.getHitInfo()
                if hitobj == "o":
                    gmap.destroyObstacle(hitpos)
                elif hitobj == "b":
                    bulhit.append(hitpos)
                elif hitobj == "p":
                    gameover = True
                    frame = 20
                elif hitobj == "e":
                    for c, e in enumerate(enemies):
                        if e.getId() == hitpos:
                            del enemies[c]
                            break
        bullets = [bul for bul in bullets if bul.getId() not in bulhit]
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            player.setDirection(3)
            gameover = player.move(gmap, None, enemies)
        elif pressed[pygame.K_DOWN]:
            player.setDirection(1)
            gameover = player.move(gmap, None, enemies)
        elif pressed[pygame.K_LEFT]:
            player.setDirection(2)
            gameover = player.move(gmap, None, enemies)
        elif pressed[pygame.K_RIGHT]:
            player.setDirection(0)
            gameover = player.move(gmap, None, enemies)
        if gameover:
            frame = 20
            
        nowtick = int(round(pygame.time.get_ticks()/1000))
        if nowtick > tick:
            changeDirection(enemies, player)
            for enemy in enemies:
                if random.randint(1, 100) <= 50:
                    bullets.append(enemy.shoot(bcount))
                    bcount += 1
            tick = nowtick
            
        if enemies:
            for enemy in enemies:
                gameover = enemy.move(gmap, player, enemies)
        else:
            frame = 30
            
        drawer.draw(gmap, player, enemies, bullets)
        
        if gameover:
            frame = 20
    elif frame == 20:
        gameover = False
        drawer.draw(gmap, player, enemies, bullets)
        screen.blit(text2, (180, 100))
    elif frame == 30:
        drawer.draw(gmap, player, enemies, bullets)
        screen.blit(text3, (200, 100))
            
    pygame.display.flip()
    clock.tick(60)