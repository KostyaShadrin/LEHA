import pygame
from pygame.draw import *
from random import randint
import numpy

pygame.init()

RED = (200, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, CYAN, MAGENTA]

score = 0
time = 0
exp_x = 0
exp_y = 0
exp_x1 = 0
exp_y1 = 0
Ecrx = 1000
Ecry = 700
FPS = 60
cursor_pos = [0, 0]
screen = pygame.display.set_mode((Ecrx, Ecry))
okno_x_min = 100
okno_x_max = 900
okno_y_min = 100
okno_y_max = 600

pygame.font.SysFont('arial', 36)
f1 = pygame.font.Font(None, 30)


class Hero:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.fi = 0
        self.r = 50
        self.tsvet_tela = COLORS[0]
        self.tsvet_planseta = COLORS[3]
        self.gun_x = int(self.x + 2 * self.r * numpy.cos(self.fi))
        self.gun_y = int(self.y + 2 * self.r * numpy.sin(self.fi))

    def vverh(self):
        if self.y > okno_y_min + self.r:
            self.y -= 100 / FPS

    def vniz(self):
        if self.y < okno_y_max - self.r:
            self.y += 100 / FPS

    def vlevo(self):
        if self.x > okno_x_min + self.r:
            self.x -= 100 / FPS

    def vpravo(self):
        if self.x < okno_x_max - self.r:
            self.x += 100 / FPS

    def new_coord(self, dx, dy):
        return [self.x + dx * self.r * numpy.cos(self.fi) + dy * self.r * numpy.sin(self.fi),
                self.y + dx * self.r * numpy.sin(self.fi) - dy * self.r * numpy.cos(self.fi)]

    def risyi(self, cursor):
        if self.y <= cursor[1]:
            self.fi = numpy.arccos((cursor[0] - self.x) / numpy.sqrt(
                (cursor[0] - self.x) * (cursor[0] - self.x) + (cursor[1] - self.y) * (cursor[1] - self.y)))
        if self.y > cursor[1]:
            self.fi = numpy.pi + numpy.arccos(-(cursor[0] - self.x) / numpy.sqrt(
                (cursor[0] - self.x) * (cursor[0] - self.x) + (cursor[1] - self.y) * (cursor[1] - self.y)))
        polygon(screen, [255, 255, 150], [self.new_coord(0.3, 0.5), self.new_coord(0.5, 0.4), self.new_coord(0.4, 0.3)])
        polygon(screen, [255, 255, 150],
                [self.new_coord(0.3, -0.5), self.new_coord(0.5, -0.4), self.new_coord(0.4, -0.3)])
        polygon(screen, self.tsvet_tela,
                [self.new_coord(-0.2, 0.2), self.new_coord(0, 0.6), self.new_coord(0.4, 0.5), self.new_coord(0.3, 0.4),
                 self.new_coord(0.1, 0.5), self.new_coord(0.2, 0.4), self.new_coord(0.3, 0.1),
                 self.new_coord(0.3, -0.1), self.new_coord(0.2, -0.4), self.new_coord(0.1, -0.5),
                 self.new_coord(0.3, -0.4), self.new_coord(0.4, -0.5), self.new_coord(0, -0.6),
                 self.new_coord(-0.2, -0.2)])
        polygon(screen, self.tsvet_planseta,
                [self.new_coord(0.3, 0.2), self.new_coord(0.5, 0.6), self.new_coord(0.7, 0.5),
                 self.new_coord(0.5, 0.1)])
        line(screen, self.tsvet_planseta, self.new_coord(0.45, -0.3), self.new_coord(0.45, -0.6), self.r // 20)
        circle(screen, [255, 255, 150], [int(self.x), int(self.y)], int(0.2 * self.r))

    def vystrel(self):
        bullet = Bullets()
        return bullet


def explosion(x, y, t):
    for i in range(0, 1000):
        fi = randint(0, 500)
        dobavka_x = randint(-10, 10)
        dobavka_y = randint(-10, 10)
        circle(screen, [255, 255, 255],
               [int(x + 3 * t * numpy.cos(fi) + dobavka_x), int(y + 3 * t * numpy.sin(fi) + dobavka_y)], 10)
        circle(screen, [0, 0, 0],
               [int(x + 3 * t * numpy.cos(fi) + dobavka_x), int(y + 3 * t * numpy.sin(fi) + dobavka_y)], 10, 1)


class SharOdin:
    time_of_birthday = 0

    def __init__(self):
        self.x = randint(200, Ecrx - 200)
        self.y = randint(200, Ecry - 200)
        self.r = randint(40, 100)
        self.speed_x = randint(-100, 100) / FPS
        self.speed_y = randint(-100, 100) / FPS
        self.time_of_birthday = time

    def dvizh(self):
        if self.time_of_birthday - self.time_of_birthday < 200:
            self.x += self.speed_x
            self.y += self.speed_y
            if self.x < okno_x_min + self.r:
                self.speed_x = -self.speed_x
                self.x = self.x + 2 * int(round(self.speed_x))
                self.speed_y = randint(-100, 100) / FPS
            if self.x > okno_x_max - self.r:
                self.speed_x = -self.speed_x
                self.x = self.x + 2 * int(round(self.speed_x))
                self.speed_y = randint(-100, 100) / FPS
            if self.y < okno_y_min + self.r:
                self.speed_y = -self.speed_y
                self.y = self.y + 2 * int(round(self.speed_y))
                self.speed_x = randint(-100, 100) / FPS
            if self.y > okno_y_max - self.r:
                self.speed_y = -self.speed_y
                self.y = self.y + 2 * int(round(self.speed_y))
                self.speed_x = randint(-100, 100) / FPS

    def risyi(self):
        if time - self.time_of_birthday < 150:
            circle(screen, [50 + (time - self.time_of_birthday) % 150, 0, 0],
                   [int(self.x), int(self.y)], self.r)
            circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                   self.r + 3, 3)
        if (time - self.time_of_birthday > 150) and (
                time - self.time_of_birthday < 201):
            circle(screen, [255, 255, 0], [int(self.x), int(self.y)],
                   self.r)
            circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                   self.r + 3, 3)
        if time - self.time_of_birthday > 200:
            explosion(int(self.x), int(self.y),
                      time - self.time_of_birthday - 200)

    def check(self, x, y, r):
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= (self.r + r) ** 2:
            return 1
        else:
            return 0


class Bullets:
    def __init__(self):
        self.x = player.x
        self.y = player.y
        self.r = 5
        self.speed = 300 / FPS
        self.fi = player.fi
        self.live = True
        self.color = (255, 0, 0)

    def dvizh(self):
        if (self.x > okno_x_min) and (self.x < okno_x_max) and self.live:
            if (self.y > okno_y_min) and (self.y < okno_y_max):
                self.y += self.speed * numpy.sin(self.fi)
            else:
                self.live = False
            self.x += self.speed * numpy.cos(self.fi)
        else:
            self.live = False

    def risyi(self):
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)


clock = pygame.time.Clock()
finished = False

shar_1 = SharOdin()
shar_2 = SharOdin()
shar_3 = SharOdin()
shar_4 = SharOdin()
shar_5 = SharOdin()
player = Hero()
bullet = Bullets()
bullet.x = 0
bullet.y = 0
while not finished:
    clock.tick(FPS)
    screen.fill([0, 0, 0])
    polygon(screen, [255, 255, 255],
            [[okno_x_min - 5, okno_y_min - 5], [okno_x_min - 5, okno_y_max + 5], [okno_x_max + 5, okno_y_max + 5],
             [okno_x_max + 5, okno_y_min - 5]], 5)
    time += 0.02 * FPS
    screen.blit(f1.render('score = ' + str(score), 1, (255, 255, 255)), (0, 0))
    bullet.dvizh()
    bullet.risyi()
    shar_1.dvizh()
    shar_1.risyi()
    keys = pygame.key.get_pressed()
    # движения игрока, если нажата одна из клавиш wasd
    if keys[pygame.K_w]:
        player.vverh()
    if keys[pygame.K_a]:
        player.vlevo()
    if keys[pygame.K_s]:
        player.vniz()
    if keys[pygame.K_d]:
        player.vpravo()
    if shar_1.check(bullet.x, bullet.y, bullet.r):
        score += 1
        shar_1 = SharOdin()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            cursor_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1) or (event.button == 3):
                cursor_pos = event.pos
                bullet = player.vystrel()
    player.risyi(cursor_pos)
    pygame.display.update()
pygame.quit()