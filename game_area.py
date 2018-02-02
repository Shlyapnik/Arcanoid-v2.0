import pygame
import random
import time

from pygame.compat import xrange_
from class_arg import GameS, MenuS
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

    def update_bg(self, arg):
        self.start_color = [min(255, max(self.start_color[i] + self.start_step[i], 0)) for i in range(3)]
        self.end_color = [min(255, max(self.end_color[i] + self.end_step[i], 0)) for i in range(3)]

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

    def update(self, arg):
        # Обновляем динамический фон
        if arg.stats.visualising_flag:
            self.cnt += 1
            if self.cnt == 50:
                self.cnt = 0
                self.start_step, self.end_step = [[random.randint(-3, 3) for j in range(3)] for i in range(2)]
                self.stars.append(self.Star(self.screen))

            self.update_bg(arg)
            self.update_stars(arg)

        # Обновлем Меню либо игровое поле
        if arg.state_flag == GameS:
            if arg.stats.training_flag:
                #print("Запрос послан update game_area")
                arg.population.move(arg)  # Запрос на обновление
            elif arg.stats.bot_activate:
                arg.bot.move(arg)

            arg.platform.update(arg)
            arg.ball.update(arg)
            for block in arg.blocks.sprites():
                block.update(arg)
        elif arg.state_flag == MenuS:
            arg.menu[arg.id_menu].update(arg)


    def blit_bg(self, arg):

        #return
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
        rail = pygame.image.load('images/new/rail 200x10.png')
        x_pos = 0
        while(x_pos < arg.settings.screen_width):
            self.screen.blit(rail, (x_pos, arg.settings.ga_height-rail.get_rect().height+1))
            x_pos += rail.get_rect().width

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
