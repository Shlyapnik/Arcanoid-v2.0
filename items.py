import pygame
import random
import param
import numpy as np
import copy

from pygame.sprite import Sprite, spritecollide
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


    def sync(self):
        self.rect.centerx, self.rect.centery = [int(item) for item in self.center]


    def blit(self):
        self.sync()
        self.screen.blit(self.image, self.rect)


class Block(Item):
    def __init__(self, arg):
        colors = ['blue 60x20.png', 'yellow 60x20.png', 'red 60x20.png']
        old_image = arg.image_name
        arg.image_name += colors[random.randint(0, 2)]
        Item.__init__(self, arg)
        arg.image_name = old_image

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


    def update(self, arg):
        pass


    def blit(self):
        Item.blit(self)



class Platform(Item):
    def __init__(self, arg):
        Item.__init__(self, arg)

        self.area_rect = arg.game_area.rect

        self.rect.top = arg.settings.ga_height - self.rect.height - 10
        self.rect.centerx = self.screen_rect.width//2
        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))

        self.moving_right = False
        self.moving_left = False

        self.velocity = arg.settings.v_platform

        self.freeze_move = [-1, -1]
        self.freeze_count = 0
        self.default_freeze_count = 2

    def link_with_ball(self, arg):
        self.ball = arg.ball

    def fake_update(self, alpha):
        result = copy.copy(self.rect)
        fake_center = copy.copy(self.center)

        if not self.is_freezing():
            if self.moving_right:
                fake_center[0] += self.velocity * alpha
            elif self.moving_left:
                fake_center[0] -= self.velocity * alpha

        result.centerx, result.centery = [int(item) for item in fake_center]
        return [self.rect, result]


    def update(self, alpha):
        # cur_rect, next_rect = self.fake_update(alpha)
        # cur_center, next_center, radius = self.ball.fake_update(alpha)

        # flag_coll = False
        # for circle in [cur_center, next_center]:
        #     for rect in [cur_rect, next_rect]:
        #         if gf.collide_circle_rect(circle, rect, radius) != [-1, -1]:
        #             flag_coll = True

        # print(flag_coll, self.ball.thrown)
        # if not flag_coll or not self.ball.thrown:
        #     if self.moving_right:
        #         self.center[0] += self.velocity * alpha
        #     elif self.moving_left:
        #         self.center[0] -= self.velocity * alpha

        #     self.sync()
        if not self.is_freezing():
            if self.moving_right:
                self.center[0] += self.velocity * alpha
            elif self.moving_left:
                self.center[0] -= self.velocity * alpha

            self.sync()

        if self.rect.left < 0:
            self.center[0] -= self.rect.left
        if self.rect.right > self.area_rect.width:
            self.center[0] += self.area_rect.width - self.rect.right

        self.sync()

        
        self.unfreeze_one()

    def freeze(self):
        self.freeze_count = self.default_freeze_count

    def unfreeze_one(self):
        if self.freeze_count > 0:
            self.freeze_count -= 1

    def is_freezing(self):
        return self.freeze_count != 0

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
        self.platform = arg.platform
        self.rect.bottom = self.platform.rect.top
        self.rect.centerx = self.platform.rect.centerx
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


    def fake_update(self, alpha):
        result = copy.copy(self.rect)
        fake_center = copy.copy(self.center)

        if not self.thrown:
            result.bottom = self.platform.rect.top
            result.centerx = self.platform.rect.centerx
            fake_center = list(map(float, [self.rect.centerx, self.rect.centery]))
        else:
            for i in range(2):
                fake_center[i] += self.velocity[i] * self.alpha_velocity * alpha
        
        result.centerx, result.centery = [int(item) for item in fake_center]
        return [self.center, fake_center, self.radius]

    def update(self, alpha):
        if alpha != 1.0:
            print("Ball {}".format(alpha))

        if not self.thrown:
            self.rect.bottom = self.platform.rect.top
            self.rect.centerx = self.platform.rect.centerx
            self.center = list(map(float, [self.rect.centerx, self.rect.centery]))
        else:
            for i in range(2):
                self.center[i] += self.velocity[i] * self.alpha_velocity * alpha

        self.sync()

    def throw(self):
        if not self.thrown:
            self.thrown = True
            miss = random.random() - 0.5
            self.velocity = [miss*4, -1]
            v_mod = sum(self.velocity[i]**2 for i in range(2))**0.5
            self.velocity = [self.velocity[i]/v_mod for i in range(2)]

            self.rect.bottom = self.platform.rect.top - 2

    def restart(self, arg):
        self.thrown = False
        self.rect.bottom = arg.platform.rect.top
        self.rect.centerx = arg.platform.rect.centerx
        self.center = list(map(float, [self.rect.centerx, self.rect.centery]))
        self.velocity = [0, 0]
