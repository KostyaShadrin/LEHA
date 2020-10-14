import pygame
from pygame.draw import *
from random import randint
import numpy

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

score = 0
time = 0
exp_x = 0
exp_y = 0
exp_x1 = 0
exp_y1 = 0
Ecrx = 1000
Ecry = 700
FPS = 20
screen = pygame.display.set_mode((Ecrx, Ecry))
okno_x_min=100
okno_x_max=900
okno_y_min=100
okno_y_max=600

pygame.font.SysFont('arial', 36)
f1 = pygame.font.Font(None, 30)


class Hero:
    x = 0
    y = 0
    fi = 0
    r=20

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

    def risyi(self, cursor):
        if self.y <= cursor[1]:
            self.fi = numpy.arccos((cursor[0] - self.x) / numpy.sqrt(
                (cursor[0] - self.x) * (cursor[0] - self.x) + (cursor[1] - self.y) * (cursor[1] - self.y)))
        if self.y > cursor[1]:
            self.fi = numpy.pi + numpy.arccos(-(cursor[0] - self.x) / numpy.sqrt(
                (cursor[0] - self.x) * (cursor[0] - self.x) + (cursor[1] - self.y) * (cursor[1] - self.y)))
        circle(screen, [0, 0, 255], [int(self.x), int(self.y)], self.r)
        line(screen, [200, 200, 200], [int(self.x), int(self.y)],
             [int(self.x + 2*self.r * numpy.cos(self.fi)), int(self.y + 2*self.r * numpy.sin(self.fi))], 3)

    def vystrel(self):
        line(screen, [255, 200, 100], [int(self.x), int(self.y)],
             [int(self.x + 1000 * numpy.cos(self.fi)), int(self.y + 1000 * numpy.sin(self.fi))],5)


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
        self.time_of_birthday = time
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
        if self.time_of_birthday - self.time_of_birthday < 150:
            circle(screen, [50 + (time - self.time_of_birthday) % 150, 0, 0],
                   [int(self.x), int(self.y)], self.r)
            circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                   self.r + 3, 3)
        if (self.time_of_birthday - self.time_of_birthday > 150) and (
                self.time_of_birthday - self.time_of_birthday < 201):
            circle(screen, [255, 255, 0], [int(self.x), int(self.y)],
                   self.r)
            circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                   self.r + 3, 3)
        if self.time_of_birthday - self.time_of_birthday > 200:
            explosion(int(self.x), int(self.y),
                      self.time_of_birthday - self.time_of_birthday - 200)

    def check(self, hero, cursor):
        if abs((cursor[1] - hero[1]) * self.x + (hero[0] - cursor[0]) * self.y - hero[0] * (
                cursor[1] - hero[1]) + hero[1] * (cursor[0] - hero[0])) / numpy.sqrt(
            (cursor[1] - hero[1]) * (cursor[1] - hero[1]) + (cursor[0] - hero[0]) * (cursor[0] - hero[0])) < self.r:
            return 1
        else:
            return 0




clock = pygame.time.Clock()
finished = False

shar_1 = SharOdin()
shar_2 = SharOdin()
shar_3 = SharOdin()
shar_4 = SharOdin()
shar_5 = SharOdin()
player = Hero()

while not finished:
    clock.tick(FPS)
    screen.fill([0, 0, 0])
    polygon(screen, [255, 255, 255], [[okno_x_min,okno_y_min], [okno_x_min,okno_y_max], [okno_x_max, okno_y_max],
                                      [okno_x_max, okno_y_min]], 5)
    time += 1
    screen.blit(f1.render('score = ' + str(score), 1, (255, 255, 255)), (0, 0))
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            cursor_posM = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1) or (event.button == 3):
                cursor_posM = event.pos
                player.vystrel()
                if shar_1.check([player.x, player.y], cursor_posM):
                    score += 1
                    shar_1 = SharOdin()
    player.risyi(cursor_posM)
    pygame.display.update()
pygame.quit()
