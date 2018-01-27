import pygame
import random
import math
import param
import numpy as np

from pygame.sprite import Sprite, spritecollide
#from game_functions import collide_circle_rect
import game_functions as gf


class Item(Sprite):
    def __init__(self, arg):
        super(Item, self).__init__()
        self.screen = arg.game_area.screen
        self.screen_rect = arg.game_area.rect
        self.settings = arg.settings

        self.image = pygame.image.load(arg.image_name)
        #self.image.fill((40, 130, 50), None, pygame.BLEND_MAX)

        self.rect = self.image.get_rect()
        self.rect.top = arg.top_space
        self.rect.left = arg.left_space

        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))

    def blit(self):
        self.rect.centerx, self.rect.centery = self.center

        self.screen.blit(self.image, self.rect)


class Block(Item):
    def __init__(self, arg):
        colors = ['blue 60x20.png', 'yellow 60x20.png', 'red 60x20.png']
        old_image = arg.image_name
        arg.image_name += colors[random.randint(0, 2)]
        Item.__init__(self, arg)
        arg.image_name = old_image

        # self.intersect_boxes = []
        # temp_box = pygame.Rect(0, 0, param.width_box, param.height_box)

        # i, j = 0, 0
        # while temp_box.left < arg.game_area.rect.width:
        #     while temp_box.top < arg.game_area.rect.height:
        #         if temp_box.colliderect(self.rect):
        #             self.intersect_boxes.append([j, i])
        #
        #         temp_box.top += param.height_box
        #         i += 1
        #
        #     temp_box.top = 0
        #     i = 0
        #     temp_box.left += param.width_box
        #     j += 1

        self.make_intersected(arg)

    def make_intersected(self, arg):
        sel1 = param.left_side < self.rect.right
        sel2 = param.right_side > self.rect.left
        sel3 = np.logical_and(sel1, sel2)
        sel4 = param.top_side < self.rect.bottom
        sel5 = param.bottom_side > self.rect.top
        sel6 = np.logical_and(sel4, sel5)

        sel7 = np.logical_and(sel3[np.newaxis, :], sel6[:, np.newaxis])
        self.intersected = np.transpose(sel7)

#        print(self.intersected)


    def update(self, arg):
        pass

    def blit(self):
        Item.blit(self)


class Platform(Item):
    def __init__(self, arg):
        Item.__init__(self, arg)

        self.rect.top = arg.settings.ga_height - self.rect.height - 10
        self.rect.centerx = self.screen_rect.width//2
        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))

        self.moving_right = False
        self.moving_left = False

        self.velocity = arg.settings.v_platform

    def update(self, arg):
        # point = gf.collide_circle_rect(arg.ball, self)
        # if point != [0, 0] and self.rect.top < arg.ball.center[1] < self.rect.bottom:
        #     a = point[0] - self.center[0]
        #     if a > 0:
        #         self.center[0] = arg.ball.center[0] - arg.ball.radius - self.rect.width/2
        #     else:
        #         self.center[0] = arg.ball.center[0] + arg.ball.radius + self.rect.width/2

        if self.moving_right:
            self.center[0] += self.velocity
            if gf.collide_circle_rect(arg.ball, self) != [0, 0]:
                self.center[0] -= self.velocity * arg.time
        if self.moving_left:
            self.center[0] -= self.velocity
            if gf.collide_circle_rect(arg.ball, self) != [0, 0]:
                self.center[0] += self.velocity * arg.time

        self.rect.centerx = self.center[0]
        if self.rect.left < 0:
            self.rect.left = 0
            self.center[0] = float(self.rect.centerx)
        if self.rect.right > self.screen_rect.width:
            self.rect.right = self.screen_rect.width
            self.center[0] = float(self.rect.centerx)

        self.rect.centerx, self.rect.centery = self.center

        # Штраф за простаивание
        if arg.stats.training_flag:
            if self.rect.right < arg.settings.ga_width//2:
                arg.stats.count -= param.side_penalty * math.fabs(self.rect.right - arg.settings.ga_width//2) / arg.settings.ga_width
            elif self.rect.left > arg.settings.ga_width//2:
                arg.stats.count -= param.side_penalty * math.fabs(self.rect.left - arg.settings.ga_width//2) / arg.settings.ga_width

    def make_intersected(self, arg):
        sel1 = param.left_side < self.rect.right
        sel2 = param.right_side > self.rect.left
        sel3 = np.logical_and(sel1, sel2)
        sel4 = param.top_side < self.rect.bottom
        sel5 = param.bottom_side > self.rect.top
        sel6 = np.logical_and(sel4, sel5)

        sel7 = np.logical_and(sel3[np.newaxis, :], sel6[:, np.newaxis])
        return np.transpose(sel7)

    def restart(self, arg):
        self.rect.top = arg.settings.ga_height - self.rect.height - 10
        self.rect.centerx = self.screen_rect.width // 2
        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))


class Ball(Item):
    def __init__(self, arg):
        Item.__init__(self, arg)

        self.radius = arg.radius
        self.color_cirle = arg.settings.cirle_color

        self.thrown = False
        self.velocity = [0, 0]
        self.alpha_velocity = self.settings.ball_velocity

        # Ставим на платформу
        self.rect.bottom = arg.platform.rect.top
        self.rect.centerx = arg.platform.rect.centerx
        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))

    def make_intersected(self, arg):
        sel1 = param.left_side < self.rect.right
        sel2 = param.right_side > self.rect.left
        sel3 = np.logical_and(sel1, sel2)
        sel4 = param.top_side < self.rect.bottom
        sel5 = param.bottom_side > self.rect.top
        sel6 = np.logical_and(sel4, sel5)

        sel7 = np.logical_and(sel3[np.newaxis, :], sel6[:, np.newaxis])
        return np.transpose(sel7)

    def blit(self):
        Item.blit(self)
        #pygame.draw.circle(self.screen, self.color_cirle, self.rect.center, self.radius, 2)

    def update(self, arg):
        self.rect.centerx, self.rect.centery = int(self.center[0]), int(self.center[1])
        if not self.thrown:
            self.rect.bottom = arg.platform.rect.top
            self.rect.centerx = arg.platform.rect.centerx
            self.center = list(map(float, [self.rect.centerx, self.rect.centery]))
        else:
            self.center[0] += self.velocity[0] * self.alpha_velocity * arg.time
            self.center[1] += self.velocity[1] * self.alpha_velocity * arg.time


        # Обрабатываем пересечение с платформой
        if gf.collide_circle_rect(self, arg.platform) != [0, 0]:
            # Update additional
            point  = gf.collide_circle_rect(self, arg.platform)
            a = [point[0] - self.center[0], point[1] - self.center[1]]
            a_mod = math.pow((math.pow(a[0], 2) + math.pow(a[1], 2)), 0.5)
            a = [a[0] / a_mod, a[1] / a_mod]


            v = [self.center[0] - arg.platform.center[0], self.center[1] - arg.platform.center[1]]
            mod_v = (v[0]**2 + v[1]**2)**0.5
            v = [v[0]/mod_v, v[1]/mod_v]
            #print(self.velocity)
            self.velocity = [v[0], v[1]]

            # Только теперь меняю позицию шара
            self.center = [point[i] - a[i] * (self.radius+1) for i in range(2)]
            # Считаю скольк бот отбил шаров
            if arg.stats.training_flag:
                arg.stats.count += arg.settings.catch_reward

        # Обрабатываем пересечение с блоками
        #break_blocks = spritecollide(self, arg.blocks, True, lambda a, b: gf.collide_circle_rect(a, b) != [0, 0])
        for block in arg.blocks.sprites():
            point = gf.collide_circle_rect(self, block)

            if point != [0, 0]:
                a = [point[0] - self.center[0], point[1] - self.center[1]]
                a_mod = math.pow((math.pow(a[0], 2) + math.pow(a[1], 2)), 0.5)
                a = [a[0] / a_mod, a[1] / a_mod]

                # Update additional
                self.center = [point[i] - a[i] * (self.radius+1) for i in range(2)]

                v = self.velocity
                v_mod = math.pow((math.pow(v[0], 2) + math.pow(v[1], 2)), 0.5)

                p_v_to_a = (a[0]*v[0] + a[1]*v[1])
                v = [v[i] - 2*a[i]*p_v_to_a for i in range(2)]
                if math.fabs(v[1]) < 0.1:
                    v[1] = 0.1

                v_mod = math.pow((math.pow(v[0], 2) + math.pow(v[1], 2)), 0.5)
                self.velocity = [v[0]/v_mod, v[1]/v_mod]

                arg.stats.add(arg.stats.reward)
                arg.blocks.remove(block)
                if len(arg.blocks) == 0:
                    gf.next_level(arg)
                break

        # Обрабатываем пересечение с границами поля
        self.rect.centerx, self.rect.centery = self.center
        if self.rect.left < 0:
            self.rect.left = 0
            self.center[0] = float(self.rect.centerx)
            self.velocity[0] *= -1
        if self.rect.right > self.screen_rect.width:
            self.rect.right = self.screen_rect.width
            self.center[0] = float(self.rect.centerx)
            self.velocity[0] *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.center[1] = float(self.rect.centery)
            self.velocity[1] *= -1
        if self.rect.top >= self.screen_rect.height:
            arg.stats.lives -= 1
            if arg.stats.lives != 0:
                self.restart()
                return
            else:
                gf.wasted(arg)
                return
        if self.rect.centery+2 >= arg.platform.rect.centery:
            self.velocity = [0, 1]
            return

    def throw(self):
        if not self.thrown:
            self.thrown = True
            miss = random.random() - 0.5
            self.velocity = [miss*4, -1]
            v_mod = sum(self.velocity[i]**2 for i in range(2))**0.5
            self.velocity = [self.velocity[i]/v_mod for i in range(2)]

    def restart(self, arg):
        self.thrown = False
        self.rect.bottom = arg.platform.rect.top
        self.rect.centerx = arg.platform.rect.centerx
        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))
        self.velocity = [0, 0]
