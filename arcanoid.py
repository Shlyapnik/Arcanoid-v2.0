import pygame
import time
import game_functions as gf

from pygame.sprite import Group, GroupSingle, groupcollide
from class_arg import Arg
from settings import Settings



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
    
    #arg.timemanager.sing_up("before all", "after all", "check + update + blit")
    #arg.timemanager.sing_up("be print", "af ", "")

    arg.timer = [0 for i in range(2)]
    while True:
        arg.timemanager.write_down("be all")
        gf.check_events(arg)
        arg.timemanager.write_down("af ch_ev")
        gf.update_state(arg)
        arg.timemanager.write_down("af up_state")
        gf.update_screen(arg)
        arg.timemanager.write_down("af bliting")
        arg.timemanager.update_sing_ups()
        
        gf.reduce_fps(arg)
        arg.timemanager.write_down("af up_sing_ups")
        # gf.print_debug(arg)

if __name__ == '__main__':
    run_game()
