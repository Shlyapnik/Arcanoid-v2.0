import pygame
import game_functions as gf
import utilites as ut

def run_game():
    
    #pygame.mouse.set_visible(False)
    arg = ut.init()
    
    #arg.timemanager.sing_up("before all", "after all", "check + update + blit")
    #arg.timemanager.sing_up("be print", "af ", "")

    while True:
        arg.tm.write_down("be all")
        gf.check_events(arg)
        arg.tm.write_down("af ch_ev")
        gf.update_state(arg)
        arg.tm.write_down("af up_state")
        gf.blit_screen(arg)
        arg.tm.write_down("af bliting")

        arg.tm.update_sing_ups()
        
        # ut.reduce_fps(arg)
        arg.tm.write_down("af up_sing_ups")
        # ut.print_debug(arg)


if __name__ == '__main__':
    run_game()
