import pygame

from button import Button


class Menu:
    def __init__(self, arg, button_type, buttons_name, buttons_width, func_list):
        number = len(buttons_name)
        self.screen = arg.game_area.screen
        self.surface = pygame.Surface((arg.menu_width, arg.menu_height))
        self.rect = self.surface.get_rect()

        self.rect.centerx = arg.game_area.rect.width//2

        self.buttons = []
        for i in range(number):
            but_screen = pygame.Surface((buttons_width[i], arg.settings.mb_height))
            but_screen_rect = but_screen.get_rect()

            but_screen_rect.centerx = self.rect.width//2
            but_screen_rect.top = 0

            if number != 1:
                but_screen_rect.top += i * ((arg.menu_height - arg.settings.mb_height)//(number - 1))
            else:
                but_screen_rect.centery = arg.menu_height//2


            but = button_type[i](arg, self.surface, but_screen, but_screen_rect, buttons_name[i], func_list[i])
            self.buttons.append(but)

        self.func_for_escape = func_list[-1]
        self.n_selected = 0

    def update(self, arg):
        for i in range(len(self.buttons)):
            self.buttons[i].update(arg)
            if self.n_selected == i:
                self.buttons[i].set_selected(True)
            else:
                self.buttons[i].set_selected(False)

    def blit(self):
        self.surface.fill((0, 0, 0, 0), self.surface.get_rect())
        self.surface.set_colorkey((0, 0, 0))
        #self.surface.set_alpha(100)
        for but in self.buttons:
            but.blit()
        self.screen.blit(self.surface, self.rect)

