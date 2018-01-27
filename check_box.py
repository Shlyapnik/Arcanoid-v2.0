import pygame
from button import Button

class Check_box:
    def __init__(self, arg, screen, surface, pos, value_func):
        self.screen = screen
        self.surface = surface

        self.pos = pos
        self.value_func = value_func
        self.checked = False

        self.image_nonchecked = pygame.image.load('images/check_box_nonactive.png')
        self.image_checked = pygame.image.load('images/check_box_active.png')

    def update(self, arg):
        self.checked = self.value_func(arg)

    def blit(self):
        if self.surface:
            self.surface.fill((0, 0, 0), self.surface.get_rect())
            self.surface.set_colorkey((0, 0, 0))

            if self.checked:
                self.surface.blit(self.image_checked, (0, 0))
            else:
                self.surface.blit(self.image_nonchecked, (0, 0))
            self.screen.blit(self.surface, self.pos)
        else:
            if self.checked:
                self.screen.blit(self.image_checked, self.pos)
            else:
                self.screen.blit(self.image_nonchecked, self.pos)



class Check_box_button:
    def __init__(self, arg, screen, surface, pos, text, value_func):
        value_func_set, value_func_get = value_func
        self.screen = screen
        self.surface = surface
        self.pos = pos
        self.selected = False
        self.text = text


        self.check_box = Check_box(arg, self.surface, None, (0, 0), value_func_get)

        def value_func(arg):
            value_func_set(arg, (False if value_func_get(arg) else True))

        arg.wide_button_flag = True
        self.button = Button(arg, self.surface, None, (40, 0), text, value_func)
        self.func = self.button.func
        arg.wide_button_flag = False


    def set_selected(self, selected):
        self.selected = selected
        self.button.set_selected(self.selected)


    def update(self, arg):
        self.check_box.update(arg)


    def blit(self):
        self.surface.fill((0, 0, 0), self.surface.get_rect())
        self.surface.set_colorkey((0, 0, 0))

        self.check_box.blit()
        self.button.blit()

        self.screen.blit(self.surface, self.pos)