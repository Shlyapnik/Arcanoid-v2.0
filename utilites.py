# Классы что нужно изменить:
# items.Platform.update

import random
import time
import pygame

from class_arg import Arg
from settings import Settings
from initer import Initer

def print_debug(arg):
    subscribers = ["All", "update_state", "bliting", "update_sing_ups", "updating score tables"]
    for subscriber in subscribers:
        print(
            "{}\n {:5.4f}%".format(
                subscriber, arg.tm.get_sibscriber(subscriber, True)
            )
        )
    print()


def reduce_fps(arg):
    if random.randint(0, 100) < 5:
        diff_fps = arg.fps_score.func_text() - arg.settings.fps
        if diff_fps > 0:
            diff_fps *= 3
        arg.additional_time += diff_fps // 2
    
    pygame.time.delay(arg.additional_time)


def init():
    pygame.init()

    arg = Arg()
    arg.settings = Settings()
    arg.screen = pygame.display.set_mode((arg.settings.screen_width, arg.settings.screen_height))#, pygame.NOFRAME)
    pygame.display.set_caption("Arcanoid")
    arg.initer = Initer()

    arg.initer(arg)

    return arg
