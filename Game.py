import pygame
from pygame.draw import *
from random import randint
import numpy

pygame.init()

RED = (250, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
LBLUE = (62, 195, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, LBLUE]

score = 0
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
Vsharikov = 5
Vchelika = 3
Vpuli = 7
T_live_sharov=5000

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
            self.y -= Vchelika

    def vniz(self):
        if self.y < okno_y_max - self.r:
            self.y += Vchelika

    def vlevo(self):
        if self.x > okno_x_min + self.r:
            self.x -= Vchelika

    def vpravo(self):
        if self.x < okno_x_max - self.r:
            self.x += Vchelika

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
        for i in range(len(Magazin) - 1):
            Magazin[i] = Magazin[i + 1]
        Magazin[5] = Bullets()


def explosion(x, y, t):
    if t < 0.5*T_live_sharov:
        for i in range(0, 30):
            fi = randint(0, 500)
            dobavka_x = randint(-10, 10)
            dobavka_y = randint(-10, 10)
            circle(screen, [255, 255, 255],
                   [int(x + 0.15 * t * numpy.cos(fi) + dobavka_x), int(y + 0.15 * t * numpy.sin(fi) + dobavka_y)], 10)


class SharOdin:
    def __init__(self):
        self.x = randint(200, Ecrx - 200)
        self.y = randint(200, Ecry - 200)
        self.r = randint(40, 100) // 2
        self.speed_x = randint(-Vsharikov, Vsharikov)
        self.speed_y = randint(-Vsharikov, Vsharikov)
        self.time_of_birthday = pygame.time.get_ticks()
        self.live = True

    def dvizh(self):
        if self.time_of_birthday - self.time_of_birthday < 20000 and self.live:
            self.x += self.speed_x
            self.y += self.speed_y
            if self.x < okno_x_min + self.r:
                self.speed_x = -self.speed_x
                self.x = self.x + 2 * int(round(self.speed_x))
            if self.x > okno_x_max - self.r:
                self.speed_x = -self.speed_x
                self.x = self.x + 2 * int(round(self.speed_x))
            if self.y < okno_y_min + self.r:
                self.speed_y = -self.speed_y
                self.y = self.y + 2 * int(round(self.speed_y))
            if self.y > okno_y_max - self.r:
                self.speed_y = -self.speed_y
                self.y = self.y + 2 * int(round(self.speed_y))

    def risyi(self):
        if self.live:
            if pygame.time.get_ticks() - self.time_of_birthday < 3*T_live_sharov/4:
                circle(screen, [50 + ((pygame.time.get_ticks() - self.time_of_birthday) *200/T_live_sharov % 150), 0, 0],
                       [int(self.x), int(self.y)], self.r)
                circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                       self.r + 3, 3)
            if (pygame.time.get_ticks() - self.time_of_birthday > 3*T_live_sharov/4) and (
                    pygame.time.get_ticks() - self.time_of_birthday < T_live_sharov):
                circle(screen, [255, 255, 0], [int(self.x), int(self.y)],
                       self.r)
                circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                       self.r + 3, 3)
            if pygame.time.get_ticks() - self.time_of_birthday > T_live_sharov and self.live:
                self.live = False
        else:
            if pygame.time.get_ticks() - self.time_of_birthday < T_live_sharov*1.5:
                explosion(int(self.x), int(self.y),
                          pygame.time.get_ticks() - self.time_of_birthday - T_live_sharov)
            else:
                self.__init__()

    def check(self, x, y, r):
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= (self.r + r) ** 2 and self.live:
            return 1
        else:
            return 0


class Bullets:
    def __init__(self):
        self.x = player.x
        self.y = player.y
        self.r = 5
        self.speed = Vpuli
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


def draw_scren():
    screen.fill([0, 0, 0])
    player.risyi(cursor_pos)
    for bullet in Magazin:
        bullet.risyi()
    for shar in Protivniki:
        shar.risyi()
    screen.blit(f1.render('score = ' + str(score), 1, (255, 255, 255)), (0, 0))
    polygon(screen, [255, 255, 255],
            [[okno_x_min - 5, okno_y_min - 5], [okno_x_min - 5, okno_y_max + 5], [okno_x_max + 5, okno_y_max + 5],
             [okno_x_max + 5, okno_y_min - 5]], 5)
    pygame.display.update()


clock = pygame.time.Clock()
finished = False
player = Hero()
if True:
    shar_0 = SharOdin()
    shar_1 = SharOdin()
    shar_2 = SharOdin()
    shar_3 = SharOdin()
    shar_4 = SharOdin()
    shar_5 = SharOdin()
    Protivniki = [shar_0, shar_1, shar_2, shar_3, shar_4, shar_5]
    bullet_0 = Bullets()
    bullet_1 = Bullets()
    bullet_2 = Bullets()
    bullet_3 = Bullets()
    bullet_4 = Bullets()
    bullet_5 = Bullets()
    bullet_6 = Bullets()
    Magazin = [bullet_0, bullet_1, bullet_2, bullet_4, bullet_5, bullet_6]


draw_scren()
time_prev_update = pygame.time.get_ticks()
while not finished:
    keys = pygame.key.get_pressed()
    for i in range(len(Protivniki)):
        for j in range(len(Magazin)):
            if Protivniki[i].check(Magazin[j].x, Magazin[j].y, Magazin[j].r):
                score += 1
                Protivniki[i] = SharOdin()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            cursor_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1) or (event.button == 3):
                cursor_pos = event.pos
                bullet = player.vystrel()
    if pygame.time.get_ticks() - time_prev_update > 500 / FPS:
        if keys[pygame.K_w]:
            player.vverh()
        if keys[pygame.K_a]:
            player.vlevo()
        if keys[pygame.K_s]:
            player.vniz()
        if keys[pygame.K_d]:
            player.vpravo()
        for bullet in Magazin:
            bullet.dvizh()
        for shar in Protivniki:
            shar.dvizh()
        time_prev_update = pygame.time.get_ticks()
        draw_scren()
pygame.quit()
