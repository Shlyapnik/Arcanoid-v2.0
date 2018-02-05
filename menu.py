import pygame
from enums import GameS, MenuS
from game_functions import new_game, close_game

from button import Button
from check_box import Check_box_button, Check_box
from unit_tests import get_tests

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


def make_menus(arg):
    arg.menu_height = 400
    arg.menu_width = arg.settings.ga_width
    arg.menu.append(make_welcome_menu(arg))

    arg.menu_height = 200
    arg.menu.append(make_stop_menu(arg))
    arg.menu.append(make_settings_menu(arg))
    arg.menu.append(make_unit_test_menu(arg))


def make_stop_menu(arg):
    names = ['Continue', 'Settings', 'Save&Exit']
    button_types = [Button, Button, Button]
    buttons_width = [150, 150, 150]

    def continue_game(arg):
        arg.state_flag = GameS

    def settings_button(arg):
        arg.id_menu = 2
        arg.prev_id_menu = 1

    def exit_button(arg):
        arg.id_menu = 0

    funcs = [continue_game, settings_button, exit_button, continue_game]

    return Menu(arg, button_types, names, buttons_width, funcs)


def make_settings_menu(arg):
    names = ['Cheat Mode', 'Activate bot', 'Activate training', 'Activate visualising']
    button_types = [Check_box_button, Check_box_button, Check_box_button, Check_box_button]
    buttons_width = [240, 240, 240, 240]

    def cheat_mode_set(arg, value):
        arg.stats.cheat_mode = value
    def cheat_mode_get(arg):
        return arg.stats.cheat_mode

    def bot_activate_set(arg, value):
        arg.stats.bot_activate = value
        if arg.stats.bot_activate:
            arg.stats.training_flag = False
            arg.bot = arg.population.get_best()
    def bot_activate_get(arg):
        return arg.stats.bot_activate

    def training_set(arg, value):
        arg.stats.training_flag = value
        arg.platform.moving_left = False
        arg.platform.moving_right = False
    def training_get(arg):
        return arg.stats.training_flag

    def visualising_set(arg, value):
        arg.stats.visualising_flag = value
    def visualising_get(arg):
        return arg.stats.visualising_flag

    def exit_button(arg):
        arg.id_menu = arg.prev_id_menu

    funcs = [[cheat_mode_set, cheat_mode_get], [bot_activate_set, bot_activate_get], [training_set, training_get],
             [visualising_set, visualising_get], exit_button]

    return Menu(arg, button_types, names, buttons_width, funcs)


def make_welcome_menu(arg):
    names = ['New Game', 'Load Game', 'Unit Tests', 'Settings', 'Exit']
    button_types = [Button, Button, Button, Button, Button]
    buttons_width = [150, 150, 150, 150, 150]

    def new_game_c(arg):
        new_game(arg)
        arg.state_flag = GameS

    def unit_test_button(arg):
        arg.id_menu = 3

    def settings_button(arg):
        arg.id_menu = 2
        arg.prev_id_menu = 0

    def empty_func(arg):
        pass

    funcs = [new_game_c, empty_func, unit_test_button, settings_button, close_game, close_game]

    return Menu(arg, button_types, names, buttons_width, funcs)


def make_unit_test_menu(arg):
    tests = get_tests(arg)
    
    names = list()
    button_types = list()
    buttons_width = list()
    funcs = list()

    def exit_func(arg):
        arg.id_menu = 0

    for test in tests:
        names.append(test.description)
        button_types.append(Button)
        buttons_width.append(150)
        funcs.append(test.load)

    names.append("Back")
    button_types.append(Button)
    buttons_width.append(150)
    funcs.append(exit_func)

    funcs.append(exit_func)

    return Menu(arg, button_types, names, buttons_width, funcs)
