from class_arg import MenuS, GameS
from items import Block
from pygame.sprite import Group

import game_functions as gf
import math

class UnitTest:
    def __init__(self):
        self.ball_pos = None
        self.ball_velocity = None
        self.alpha_velocity = 0.1
        self.blocks = list()
        self.platform_pos = None

        self.description = None

    def load(self, arg):
        arg.wasted = self.wasted
        arg.next_level = self.wasted
        self.training_flag = arg.stats.training_flag
        arg.stats.training_flag = False
        self.bot_activate = arg.stats.bot_activate
        arg.stats.bot_activate = False

        arg.ball.thrown = True
        arg.ball.alpha_velocity = self.alpha_velocity
        arg.ball.velocity = self.ball_velocity.copy()
        mod_vel = (arg.ball.velocity[0] ** 2 + arg.ball.velocity[1] ** 2) ** 0.5
        arg.ball.velocity[0] /= mod_vel
        arg.ball.velocity[1] /= mod_vel

        arg.ball.rect.centerx = self.ball_pos[0]
        arg.ball.rect.centery = self.ball_pos[1]
        arg.ball.center = list(map(float, [arg.ball.rect.centerx, arg.ball.rect.centery]))

        arg.platform.restart(arg)
        arg.platform.rect.centerx = self.platform_pos
        arg.platform.center = list(map(float, [arg.platform.rect.centerx, arg.platform.rect.centery]))

        arg.blocks = Group()
        for brick in self.blocks:
            arg.left_space, arg.top_space = brick
            arg.blocks.add(Block(arg))

        arg.state_flag = GameS
        

    def wasted(self, arg):
        arg.id_menu = 3
        arg.state_flag = MenuS

        arg.wasted = gf.wasted
        arg.next_level = gf.next_level
        arg.stats.training_flag = self.training_flag
        arg.stats.bot_activate = self.bot_activate

def get_tests(arg):
    result = list()

    result.append(make_test1(arg))
    result.append(make_test2(arg))
    result.append(make_test3(arg))
    result.append(make_test4(arg))

    return result

def make_test1(arg):
    result = UnitTest()

    result.description = "Double Hor"
    result.ball_pos = (50, 100)
    result.alpha_velocity = 14
    result.ball_velocity = [1, 0]

    result.blocks.append((300, 105))
    result.blocks.append((300, 75))
    result.blocks.append((0, 0))

    result.platform_pos = 40    

    return result

def make_test2(arg):
    result = UnitTest()

    result.description = "Corner"
    result.ball_pos = (300, 300)
    result.alpha_velocity = 14
    result.ball_velocity = [-140, -180]

    result.blocks.append((0, 0))

    result.blocks.append((100, 100))
    result.blocks.append((100, 120))
    result.blocks.append((160, 100))
    result.blocks.append((100, 140))
    

    result.platform_pos = 40    

    return result

def make_test3(arg):
    result = UnitTest()

    result.description = "Throgh"
    result.ball_pos = (227, 355)
    result.alpha_velocity = 20
    result.ball_velocity = [15, -230]

    result.blocks.append((0, 0))

    result.blocks.append((100, 100))
    result.blocks.append((175, 100))
    result.blocks.append((250, 100))
    result.blocks.append((325, 100))
    

    result.platform_pos = 40    

    return result


def make_test4(arg):
    result = UnitTest()

    result.description = "Throgh 2"
    result.ball_pos = (150, 210)
    result.alpha_velocity = 40
    result.ball_velocity = [0, -1]

    result.blocks.append((0, 0))

    result.blocks.append((100, 100))
    

    result.platform_pos = 40    

    return result