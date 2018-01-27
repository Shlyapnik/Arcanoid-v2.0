import pygame
import time
import game_functions as gf

from pygame.sprite import Group, GroupSingle, groupcollide
from class_arg import Arg
from settings import Settings
from items import Block, Ball, Platform
from game_area import Game_area
from label import Label



def run_game():
    pygame.init()

    arg = Arg()
    arg.settings = Settings()
    arg.screen = pygame.display.set_mode((arg.settings.screen_width, arg.settings.screen_height))#, pygame.NOFRAME)
    pygame.display.set_caption("Arcanoid")
    #pygame.mouse.set_visible(False)
    #pygame.time.set_timer(pygame.USEREVENT, 200)

    gf.init(arg)

    #pygame.time.set_timer(pygame.USEREVENT, 1000//20)
    arg.timer = [0 for i in range(2)]
    while True:
        gf.safe_before_iter(arg)

        gf.check_events(arg)
        gf.update_state(arg)
        gf.update_screen(arg)

        gf.calc_after_iter(arg)

if __name__ == '__main__':
    run_game()
