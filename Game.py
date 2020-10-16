import pygame
from pygame.draw import *
from random import randint
import numpy
import os

pygame.init()

RED = (250, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
LBLUE = (62, 195, 255)
WHITE = (255, 255, 255)
KOJA = (255, 255, 150)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, LBLUE, WHITE, KOJA, BLACK]

score = 0
exp_x = 0
exp_y = 0
exp_x1 = 0
exp_y1 = 0
Ecrx = 1400
Ecry = 750
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Центрирем
FPS = 60
if FPS > 200:
    FPS = 200
cursor_pos = [0, 0]
screen = pygame.display.set_mode((Ecrx, Ecry))
okno_x_min = 150
okno_x_max = Ecrx - okno_x_min
okno_y_min = 100
okno_y_max = 700
Vsharikov = int(4 * 60 / FPS)
Vchelika = 3 * 60 / FPS
Vpuli = 7 * 60 / FPS
T_live_sharov = 5000

pygame.font.SysFont('arial', 36)
f1 = pygame.font.Font(None, 30)
f2 = pygame.font.Font(None, 80)
def draw_perezaryadis():
    screen.blit(f2.render('ПЕРЕЗАРЯДИСЬ!!!', 1, (255, 0, 0)), (400, 0))

class Hero:
    x = 200
    y = 300
    fi = 0
    r = 80
    tsvet_tela = 0
    tsvet_planseta = 2
    Hitbox = [[0, 0]] * 6

    def vverh(self):
        if self.y > okno_y_min + self.r // 2:
            self.y -= Vchelika

    def vniz(self):
        if self.y < okno_y_max - self.r // 2:
            self.y += Vchelika

    def vlevo(self):
        if self.x > okno_x_min + self.r // 2:
            self.x -= Vchelika

    def vpravo(self):
        if self.x < okno_x_max - self.r // 2:
            self.x += Vchelika

    def new_coord(self, dx, dy):
        return (int(self.x + dx * self.r * numpy.cos(self.fi) + dy * self.r * numpy.sin(self.fi)),
                int(self.y + dx * self.r * numpy.sin(self.fi) - dy * self.r * numpy.cos(self.fi)))

    def hitbox(self):
        return [self.new_coord(0.3, 0), self.new_coord(0.3, 0.5), self.new_coord(-0.2, 0.5),
                self.new_coord(-0.2, 0), self.new_coord(-0.2, -0.5), self.new_coord(0.3, -0.5)]

    def ugol(self, cursor):
        if self.y <= cursor[1]:
            self.fi = numpy.arccos((cursor[0] - self.x) / (1 + numpy.sqrt(
                (cursor[0] - self.x) * (cursor[0] - self.x) + (cursor[1] - self.y) * (cursor[1] - self.y))))
        if self.y > cursor[1]:
            self.fi = numpy.pi + numpy.arccos(-(cursor[0] - self.x) / numpy.sqrt(
                (cursor[0] - self.x) * (cursor[0] - self.x) + (cursor[1] - self.y) * (cursor[1] - self.y)))

    def risyi(self):
        polygon(screen, COLORS[8], [self.new_coord(0.3, 0.5), self.new_coord(0.5, 0.4), self.new_coord(0.4, 0.3)])
        polygon(screen, COLORS[8],
                [self.new_coord(0.3, -0.5), self.new_coord(0.5, -0.4), self.new_coord(0.4, -0.3)])
        polygon(screen, COLORS[self.tsvet_tela],
                [self.new_coord(-0.2, 0.2), self.new_coord(0, 0.6), self.new_coord(0.4, 0.5), self.new_coord(0.3, 0.4),
                 self.new_coord(0.1, 0.5), self.new_coord(0.2, 0.4), self.new_coord(0.3, 0.1),
                 self.new_coord(0.3, -0.1), self.new_coord(0.2, -0.4), self.new_coord(0.1, -0.5),
                 self.new_coord(0.3, -0.4), self.new_coord(0.4, -0.5), self.new_coord(0, -0.6),
                 self.new_coord(-0.2, -0.2)])

    def risyi_equip(self):
        polygon(screen, COLORS[self.tsvet_planseta],
                [self.new_coord(0.3, 0.2), self.new_coord(0.5, 0.6), self.new_coord(0.7, 0.5),
                 self.new_coord(0.5, 0.1)])
        line(screen, COLORS[self.tsvet_planseta], self.new_coord(0.45, -0.3), self.new_coord(0.45, -0.6), self.r // 20)
        polygon(screen, COLORS[7],
                [self.new_coord(0.325, 0.25), self.new_coord(0.525, 0.15), self.new_coord(0.675, 0.45),
                 self.new_coord(0.475, 0.55)])
        lines(screen, COLORS[9], False,
              [self.new_coord(0.6, 0.3), self.new_coord(0.625, 0.45), self.new_coord(0.525, 0.2),
               self.new_coord(0.585, 0.47),
               self.new_coord(0.485, 0.22), self.new_coord(0.545, 0.49), self.new_coord(0.445, 0.24),
               self.new_coord(0.505, 0.51), self.new_coord(0.405, 0.26), self.new_coord(0.465, 0.53),
               self.new_coord(0.365, 0.28), self.new_coord(0.4, 0.4), self.new_coord(0.6, 0.3)],
              1)
        line(screen, BLACK, self.new_coord(0.6, 0.3), self.new_coord(0.4, 0.4), 2)
        line(screen, BLACK, self.new_coord(0.675, 0.45), self.new_coord(0.475, 0.55), 2)
        line(screen, BLACK, self.new_coord(0.525, 0.15), self.new_coord(0.325, 0.25), 2)
        circle(screen, BLACK, self.new_coord(0.45, -0.3), int(self.r / 50))
        circle(screen, COLORS[8], [int(self.x), int(self.y)], int(0.2 * self.r))
        circle(screen, COLORS[self.tsvet_planseta + 1], self.new_coord(-0.075, 0), int(0.21 * self.r))

    def vystrel(self,N):
        Magazin[N]=Bullets()


class AntiHero(Hero):
    x = 600
    y = 300
    fi = 0
    r = 100
    tsvet_tela = 9
    tsvet_planseta = 0
    Hitbox = [[0, 0]] * 6
    time_of_birthday = pygame.time.get_ticks()
    live = True

    def ugol_epta(self, hero):
        super().ugol(hero)

    def risyi_epta(self):
        super().risyi()
        circle(screen, COLORS[8], [int(self.x), int(self.y)], int(0.15 * self.r))
        lines(screen, WHITE, False,
              [super().new_coord(0.05, 0.25), super().new_coord(-0.05, 0.25), super().new_coord(-0.05, 0.3),
               super().new_coord(0, 0.3), super().new_coord(0, 0.25)], 2)
        lines(screen, WHITE, False,
              [super().new_coord(0.05, 0.4), super().new_coord(-0.05, 0.4), super().new_coord(-0.05, 0.35),
               super().new_coord(-0.05, 0.45)], 2)
        polygon(screen, WHITE,
                [super().new_coord(0, -0.275), super().new_coord(0.05, -0.4), super().new_coord(0.025, -0.375),
                 super().new_coord(-0.025, -0.4), super().new_coord(-0.025, -0.45), super().new_coord(-0.05, -0.4),
                 super().new_coord(0, -0.35), super().new_coord(-0.05, -0.3), super().new_coord(-0.025, -0.25),
                 super().new_coord(-0.025, -0.3), super().new_coord(0, -0.325)])

    def shagi(self):
        if self.time_of_birthday - self.time_of_birthday < 20000 and self.live:
            self.x += Vpuli / 3 * numpy.cos(self.fi)
            self.y += Vpuli / 3 * numpy.sin(self.fi)
            if self.x < okno_x_min + self.r:
                self.fi = -self.fi
                self.x += Vpuli / 3 * numpy.sin(self.fi)
                self.y += Vpuli / 3 * numpy.cos(self.fi)
            if self.x > okno_x_max - self.r:
                self.x += Vpuli / 3 * numpy.sin(self.fi)
                self.y += Vpuli / 3 * numpy.cos(self.fi)
            if self.y < okno_y_min + self.r:
                self.fi = -self.fi
                self.x += Vpuli / 3 * numpy.sin(self.fi)
                self.y += Vpuli / 3 * numpy.cos(self.fi)
            if self.y > okno_y_max - self.r:
                self.fi = -self.fi
                self.x += Vpuli / 3 * numpy.sin(self.fi)
                self.y += Vpuli / 3 * numpy.cos(self.fi)


class Snaryad(AntiHero):
    def __init__(self):
        self.x = gopnic_1.x
        self.y = gopnic_1.y
        self.fi = 0
        self.fi_povorota = - numpy.pi / 2 + gopnic_1.fi
        self.r = 30
        self.Hitbox = [[0, 0]] * 4
        self.time_of_birthday = pygame.time.get_ticks()
        self.live = True

    def butylka(self):
        polygon(screen, COLORS[9],
                [super().new_coord(0.05, 0.5), super().new_coord(0.05, 0.3), super().new_coord(0.15, 0.2),
                 super().new_coord(0.15, -0.5),
                 super().new_coord(-0.15, -0.5), super().new_coord(-0.15, 0.2), super().new_coord(-0.05, 0.3),
                 super().new_coord(-0.05, 0.5)])

    def polet(self):
        self.fi += 0.03
        self.x += Vpuli / 2 * numpy.sin(-self.fi_povorota)
        self.y += Vpuli / 2 * numpy.cos(-self.fi_povorota)


def inside_check(x, y, a):
    det_prev = 0
    for iba in range(len(a)):
        a_x = a[iba][0]
        a_y = a[iba][1]
        b_x = a[(iba + 1) % len(a)][0]
        b_y = a[(iba + 1) % len(a)][1]
        # counting vector between the first neighbouring vertex and click position
        ev_point_x = x - a_x
        ev_point_y = y - a_y
        v_x = b_x - a_x
        v_y = b_y - a_y
        # counting the determinant(oriented area)
        det = - ev_point_x * v_y + ev_point_y * v_x
        # Ориентация поменялась?
        if det * det_prev < 0:
            return False
        det_prev = - ev_point_x * v_y + ev_point_y * v_x
    return True


def explosion(x, y, t):
    if t < 0.5 * T_live_sharov:
        for ik in range(0, 30):
            fi = randint(0, 500)
            dobavka_x = randint(-10, 10)
            dobavka_y = randint(-10, 10)
            circle(screen, [255, 255, 255],
                   [int(x + 0.15 * t * numpy.cos(fi) + dobavka_x),
                    int(y + 0.15 * t * numpy.sin(fi) + dobavka_y)], 10)


class SharOdin:
    def __init__(self):
        self.x = randint(okno_x_min + 200, okno_x_max - 200)
        self.y = randint(okno_y_min + 200, okno_y_max - 200)
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
            if pygame.time.get_ticks() - self.time_of_birthday < 3 * T_live_sharov / 4:
                circle(screen,
                       [50 + ((pygame.time.get_ticks() - self.time_of_birthday) * 200 / T_live_sharov % 150), 255, 0],
                       [int(self.x), int(self.y)], self.r)
                circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                       self.r + 3, 3)
            if (pygame.time.get_ticks() - self.time_of_birthday > 3 * T_live_sharov / 4) and (
                    pygame.time.get_ticks() - self.time_of_birthday < T_live_sharov):
                circle(screen, [255, 0, 0], [int(self.x), int(self.y)],
                       self.r)
                circle(screen, [0, 0, 0], [int(self.x), int(self.y)],
                       self.r + 3, 3)
            if pygame.time.get_ticks() - self.time_of_birthday > T_live_sharov and self.live:
                self.live = False
        else:
            for dot in player.hitbox():
                if (dot[0] - self.x) ** 2 + (dot[1] - self.y) ** 2 < (0.15 * (
                        pygame.time.get_ticks() - self.time_of_birthday - T_live_sharov)) ** 2 and not self.live:
                    global score
                    score -= 10
                    self.__init__()
            if pygame.time.get_ticks() - self.time_of_birthday < T_live_sharov * 1.5 and not self.live:
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
        self.N=0
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
                self.x += self.speed * numpy.cos(self.fi)
        if not self.live:
            self.x = 10
            self.y = 200 + 50 * self.N
            self.r = 10
            self.fi = 0

    def risyi(self):
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)



def draw_scren():
    screen.fill([200, 200, 200])
    player.ugol(cursor_pos)
    if not gotovnost_k_strelbye:
        draw_perezaryadis()
    player.risyi()
    player.risyi_equip()
    for bullet_d in Magazin:
        bullet_d.risyi()
    for shar_n in Protivniki:
        shar_n.risyi()
    gopnic_1.ugol_epta((player.x, player.y))
    gopnic_1.risyi_epta()
    gopnic_1.shagi()
    vodka_1.butylka()
    vodka_1.polet()
    draw_magazin()
    screen.blit(f1.render('score = ' + str(score), 1, (255, 255, 255)), (0, 0))
    polygon(screen, [255, 255, 255],
            [[okno_x_min - 5, okno_y_min - 5], [okno_x_min - 5, okno_y_max + 5], [okno_x_max + 5, okno_y_max + 5],
             [okno_x_max + 5, okno_y_min - 5]], 5)
    pygame.display.update()

def dvigai_objcts():
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

def reload():
    for i in range(k_bullets):
        Magazin[i].live=False
        Magazin[i].N=i
clock = pygame.time.Clock()
finished = False
player = Hero()
k_bullets = 7
Magazin = [Bullets()] * k_bullets
k_sharov = 6
Protivniki = [SharOdin()] * k_sharov
k_antihero = 1
for i in range(k_bullets):
    Magazin[i] = Bullets()
    Magazin[i].live = False
    Magazin[i].N=i
gotovnost_k_strelbye=True
for i in range(k_sharov):
    Protivniki[i] = SharOdin()

gopnic_1 = AntiHero()
vodka_1 = Snaryad()
def draw_magazin():
    for i in range(len(Magazin)):
        if not Magazin[i].live:
            Magazin[i].risyi()


draw_scren()
time_last_reload = pygame.time.get_ticks()
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
                odnorazovii_kostyl=True
                for i in range(k_bullets):
                    if not Magazin[i].live and odnorazovii_kostyl:
                        player.vystrel(i)
                        odnorazovii_kostyl=False
                if odnorazovii_kostyl:
                    gotovnost_k_strelbye=False


        if keys[pygame.K_r]and pygame.time.get_ticks()-time_last_reload>1000:
            time_last_reload=pygame.time.get_ticks()
            reload()
            gotovnost_k_strelbye=True

    if pygame.time.get_ticks() - time_prev_update > 500 / FPS:
        dvigai_objcts()
        if pygame.time.get_ticks() - time_prev_update > 10:
            vodka_1 = Snaryad()
        time_prev_update = pygame.time.get_ticks()
        draw_scren()
pygame.quit()
