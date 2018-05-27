import pygame
import random
import time

import collision_functions as cf
import game_functions as gf

from pygame.compat import xrange_
from enums import GameS, MenuS
#from pygame._numpysurfarray import type_name *

class Game_area:
    def __init__(self, arg):
        self.screen = pygame.Surface((arg.settings.ga_width, arg.settings.ga_height))
        self.screen.fill(arg.settings.ga_bg_color)
        self.rect = self.screen.get_rect()

        self.rect.centerx = arg.screen.get_rect().centerx
        self.rect.bottom = arg.screen.get_rect().bottom

        self.cnt = 0
        self.start_step = [0, 0, 0]
        self.end_step = [0, 0, 0]
        self.start_color = [random.randint(0, 255) for i in range(3)]
        self.end_color = [random.randint(0, 255) for i in range(3)]
        self.stars = []

        self.rail = pygame.image.load('images/new/rail 200x10.png')

    def update_gradient(self, arg):
        self.start_color = [min(255, max(self.start_color[i] + self.start_step[i], 0)) for i in range(3)]
        self.end_color = [min(255, max(self.end_color[i] + self.end_step[i], 0)) for i in range(3)]

    def update_background(self, arg):
        # Изменяем направление градиента
        self.cnt += 1
        if self.cnt == 50:
            self.cnt = 0
            self.start_step, self.end_step = [[random.randint(-3, 3) for j in range(3)] for i in range(2)]
            self.stars.append(self.Star(self.screen))

        self.update_gradient(arg)
        self.update_stars(arg)

    def update_stars(self, arg):
        #print(len(self.stars))
        for star in self.stars:
            star.update()
            if star.pos[0] + star.radius < 0:
                self.stars.remove(star)
            elif star.pos[0] - star.radius > self.rect.width:
                self.stars.remove(star)
            elif star.pos[1] + star.radius < 0:
                self.stars.remove(star)
            elif star.pos[1] - star.radius > self.rect.height:
                self.stars.remove(star)


    def request_move(self, arg):
        if arg.stats.training_flag:
            arg.population.move(arg) 
        elif arg.stats.bot_activate:
            arg.bot.move(arg)


    def update_dynamic_objects(self, arg):
        # Нужно вот здесь реализовывать коллизии
        
        eps = 0.01
        step_alpha = 1.0

        cf.keep_nearest_blocks(arg)

        # Проверяем не можем ли мы сразу шагнуть на единичку
        if not cf.check_for_coll(arg, 1.0):
            cf.real_update(arg, 1.0)
        else:
            # Начинаем бинарный поиск
            while step_alpha > eps:
                min_alpha, max_alpha = 0.0, step_alpha
                while max_alpha - min_alpha > eps:
                    prob_alpha = (max_alpha + min_alpha) / 2

                    if cf.check_for_coll(arg, prob_alpha):
                        max_alpha = prob_alpha
                    else:
                        min_alpha = prob_alpha
                
                cf.real_update(arg, min_alpha)
                cf.detect_coll_and_change(arg, eps)
                step_alpha -= prob_alpha

        # Проверки на конец игры
        if len(arg.blocks) == 0:
            arg.next_level(arg)

        if arg.ball.center[1] - arg.radius > arg.game_area.rect.height:
            arg.wasted(arg)


        # ----------------------------------------------------------------------------
        # Please, coding above the line!


    def update(self, arg):
        # Обновляем динамический фон
        if arg.stats.visualising_flag:
            self.update_background(arg)

        # Обновлем меню либо игровое поле
        if arg.state_flag == GameS:
            self.request_move(arg)
            self.update_dynamic_objects(arg)
        elif arg.state_flag == MenuS:
            arg.menu[arg.id_menu].update(arg)


    def blit_bg(self, arg):
        ar = pygame.PixelArray(self.screen)
        r, g, b = [self.start_color[i] / 5 for i in range(3)]
        # Do some easy gradient effect.
        d_color = [(self.end_color[i] - self.start_color[i]) / 5 / ar.shape[1] for i in xrange_(3)]
        for y in xrange_(ar.shape[1]):
            # r, g, b = [self.start_color[i] + d_color[i] for i in xrange_(3)]
            r += d_color[0]
            g += d_color[1]
            b += d_color[2]

            ar[:, y] = (r, g, b)
        del ar


    def blit_rail(self, arg):
        x_pos = 0
        while(x_pos < arg.settings.screen_width):
            self.screen.blit(self.rail, (x_pos, arg.settings.ga_height - self.rail.get_rect().height+1))
            x_pos += self.rail.get_rect().width


    def blit(self, arg):
        # Собираем динамический фон
        if arg.stats.visualising_flag:
            self.blit_bg(arg)
            for i in range(len(self.stars)):
                self.stars[i].blit()
            self.blit_rail(arg)
        else:
            self.screen.fill((0, 0, 0), self.screen.get_rect())

        # Выводим Меню либо игровое поле
        if arg.state_flag == GameS and arg.stats.visualising_flag:
            arg.ball.blit()
            arg.platform.blit()
            arg.blocks.draw(arg.game_area.screen)
        elif arg.state_flag == MenuS:
            arg.menu[arg.id_menu].blit()

        # Выводим game_area на главный экран
        arg.screen.blit(self.screen, self.rect)



    class Star():
        def __init__(self, screen):
            self.screen = screen
            self.screen_rect = screen.get_rect()

            self.radius = random.randint(1, 5)
            self.color = [random.randint(220, 255) for i in range(3)]

            self.velocity = [random.random()*6-3 for i in range(2)]
            self.a = [random.random()*0.5-0.25 for i in range(2)]
            self.pos = [0, 0]

            if self.velocity[1] > 0:
                self.pos = [random.randint(0, self.screen_rect.width), -self.radius]
            elif self.velocity[0] < 0:
                self.pos = [self.screen_rect.width + self.radius, random.randint(0, self.screen_rect.height)]
            elif self.velocity[0] > 0:
                self.pos = [ -self.radius, random.randint(0, self.screen_rect.height)]

        def update(self):
            self.pos = [self.pos[i] + self.velocity[i] for i in range(2)]
            self.velocity = [self.velocity[i] + self.a[i] for i in range(2)]

        def blit(self):
            pygame.draw.circle(self.screen, self.color, [int(self.pos[i]) for i in range(2)], self.radius)
