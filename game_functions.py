import sys
import pygame
import math
import time

from utilites import Timemanager
from pygame.sprite import Group, groupcollide, spritecollide
from menu import Menu
from items import Block, Ball, Platform
from label import Label
from game_area import Game_area
from stats import Stats
from class_arg import MenuS, GameS

from population import Population

from button import Button
from check_box import Check_box_button, Check_box



def check_keydown_game_events(event, arg):
    if event.key == pygame.K_RIGHT:
        arg.platform.moving_right = True
    elif event.key == pygame.K_LEFT:
        arg.platform.moving_left = True
    elif event.key == pygame.K_SPACE:
        if not arg.ball.thrown:
            arg.ball.throw()
    elif event.key == pygame.K_ESCAPE:
        arg.id_menu = 1
        arg.state_flag = MenuS

    if arg.stats.cheat_mode:
        if event.key == pygame.K_r:
            arg.ball.restart()
        elif event.key == pygame.K_b:
            restart(arg)
        elif event.key == pygame.K_KP_PLUS:
            arg.ball.alpha_velocity += 1
        elif event.key == pygame.K_KP_MINUS:
            arg.ball.alpha_velocity -= 1
    else:
        print("CheatMode не включен")


def check_keyup_game_events(event, arg):
    if event.key == pygame.K_RIGHT:
        arg.platform.moving_right = False
    elif event.key == pygame.K_LEFT:
        arg.platform.moving_left = False


def check_keydown_menu_events(event, arg):
    cur_menu = arg.menu[arg.id_menu]

    if event.key == pygame.K_ESCAPE:
        cur_menu.func_for_escape(arg)
    if event.key == pygame.K_UP and cur_menu.n_selected != 0:
        cur_menu.n_selected -= 1
    if event.key == pygame.K_DOWN and cur_menu.n_selected != len(cur_menu.buttons) - 1:
        cur_menu.n_selected += 1
    # Не нашёл в pygame заготовленный код для Enter-а
    if event.key == 13:
        print(cur_menu.buttons[cur_menu.n_selected].text)
        cur_menu.buttons[cur_menu.n_selected].func(arg)


def check_keyup_menu_events(event, arg):
    pass


def check_events(arg):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(arg)

        if arg.state_flag == GameS:
            if event.type == pygame.KEYDOWN:
                check_keydown_game_events(event, arg)

            elif event.type == pygame.KEYUP:
                check_keyup_game_events(event, arg)

        elif arg.state_flag == MenuS:
            if event.type == pygame.KEYDOWN:
                check_keydown_menu_events(event, arg)

            elif event.type == pygame.KEYUP:
                check_keyup_menu_events(event, arg)


def collide_circle_rect(a, b):
    b.rect.centerx, b.rect.centery = b.center
    sol = [0, 0]

    if b.rect.left < a.center[0] < b.rect.right:
        if math.fabs(a.center[1] - b.rect.top) < a.radius:
            sol = [a.center[0], b.rect.top]
        elif math.fabs(a.center[1] - b.rect.bottom) < a.radius:
            sol = [a.center[0], b.rect.bottom]
    elif b.rect.top < a.center[1] < b.rect.bottom:
        if math.fabs(a.center[0] - b.rect.left) < a.radius:
            sol = [b.rect.left, a.center[1]]
        elif math.fabs(a.center[0] - b.rect.right) < a.radius:
            sol = [b.rect.right, a.center[1]]
    else:
        temp_func = lambda a, point: True if ((a.center[0] - point[0])**2 + (a.center[1] - point[1])**2) ** 0.5 < a.radius else False

        for side_1 in [b.rect.left, b.rect.right]:
            for side_2 in [b.rect.top, b.rect.bottom]:
                if temp_func(a, (side_1, side_2)):
                    sol = [side_1, side_2]

    return sol


def update_screen(arg):
    # Выводим стену заднего фона на экран
    arg.screen.blit(arg.wall, arg.wall.get_rect())

    # Выводим разнообразые информациооные поля
    arg.fps_score.blit()

    if arg.state_flag == GameS:
        arg.speed_score.blit()

        # Вы водим все необходимые игровые данные на главный экран
        arg.score_table.blit()
        arg.best_score_table.blit()
        arg.lives_table.blit()
        arg.level_table.blit()
        arg.time_table.blit()
    elif arg.state_flag == MenuS:
        pass

    arg.game_area.blit(arg)


    # Отрисовываем всё на экране
    pygame.display.flip()


def update_state(arg):
    arg.fps_score.update()
    arg.game_area.update(arg)

    if arg.state_flag == GameS:
        arg.speed_score.update()

        arg.score_table.update()
        arg.best_score_table.update()
        arg.lives_table.update()
        arg.level_table.update()
        arg.time_table.update()
    elif arg.state_flag == MenuS:
        pass


def init(arg):
    # Загружаем стену
    arg.wall = make_wall('images/break.bmp', arg)

    # Создаём территорию для игры
    arg.game_area = Game_area(arg)

    # Создаём класс для подсчёта очков
    arg.stats = Stats(arg)
    arg.stats.load_prev_session(arg)

    # Создаём популяцию для обучения
    arg.population = Population(arg)
    arg.population.load_prev_session(arg)

    # Создаём меню
    arg.menu_height = 400
    arg.menu_width = arg.settings.ga_width
    arg.menu.append(make_welcome_menu(arg))

    arg.menu_height = 200
    arg.menu.append(make_stop_menu(arg))

    arg.menu.append(make_settings_menu(arg))

    # Создаём объект платформы
    arg.image_name = 'images/new/platform 120x20.png'
    arg.platform = Platform(arg)

    # Создаём шар для игры
    arg.radius = 10
    arg.image_name = 'images/new/ball_aparture 20x20.png'
    arg.ball = Ball(arg)

    # Создаём блоки для ломания
    arg.image_name = 'images/new/block_'
    arg.blocks = Group()

    # Создаём Таймменеджер
    arg.timemanager = Timemanager()

    arg.timemanager.sing_up("be all", "af ch_ev", "check_event")
    arg.timemanager.sing_up("af ch_ev", "af up_state", "update_state")
    arg.timemanager.sing_up("af up_state", "af bliting", "bliting")
    arg.timemanager.sing_up("af bliting", "af up_sing_ups", "update_sing_ups")
    arg.timemanager.sing_up("be all", "af up_sing_ups", "All")

    # Создаём разнообразные панели для вывода резов
    make_tables(arg)


def make_tables(arg):
    arg.top_space = 10
    arg.left_space = arg.settings.screen_width - 90
    arg.fps_score = Label(arg, 'FPS:', lambda: int(
            
            1000.0 / max(1, 
                arg.timemanager.get_sibscriber("All", False, False) / 
                max(1, arg.timemanager.get_sibscriber("All", False, True))
            )
        )
    )

    arg.left_space = arg.settings.screen_width - 220
    arg.speed_score = Label(arg, 'Speed:', lambda: arg.speed_count)

    arg.left_space = (arg.settings.screen_width - arg.settings.ga_width) // 2
    arg.top_space = arg.settings.screen_height - arg.settings.ga_height - 32
    arg.best_score_table = Label(arg, 'Best score:', lambda: int(arg.stats.max_count))

    arg.left_space += arg.settings.ga_width // 2
    arg.score_table = Label(arg, 'Score:', lambda: int(arg.stats.count))

    arg.left_space, arg.top_space = 10, 10
    arg.lives_table = Label(arg, 'Lives remain:', lambda: arg.stats.lives)

    arg.top_space += 30
    arg.level_table = Label(arg, 'Level:', lambda: arg.stats.level)

    arg.top_space, arg.left_space = 10, 200
    arg.time_table = Label(arg, 'Time:', lambda: (pygame.time.get_ticks() - arg.stats.start_time) // 1000)




def make_target_wall(arg):
    number_in_row = (arg.settings.ga_width - 4)//arg.settings.target_width
    side_space = (arg.settings.ga_width - number_in_row * arg.settings.target_width)//2


    for i in range(arg.settings.width_target_wall):
        x_pos, y_pos = side_space, arg.settings.space_target + i * arg.settings.target_height

        while(x_pos + arg.settings.target_width <= arg.game_area.rect.width - side_space):
            arg.top_space, arg.left_space = y_pos, x_pos
            arg.blocks.add(Block(arg))

            x_pos += arg.settings.target_width


def make_wall(name, arg):
    wall = pygame.Surface((arg.settings.screen_width, arg.settings.screen_height))
    wall.fill(arg.settings.bg_color)


    block = pygame.image.load(name).convert_alpha()

    block_rect = block.get_rect()
    wall_rect = wall.get_rect()

    side_space = (arg.settings.screen_width - arg.settings.ga_width)//2
    top_space = (arg.settings.screen_height - arg.settings.ga_height)
    piece_space = 10

    left_half_block = block.subsurface(block_rect.left, block_rect.top, piece_space, block_rect.bottom)
    right_half_block = block.subsurface(block_rect.right - piece_space, block_rect.top, piece_space, block_rect.bottom)

    y_pos = -(block_rect.height - top_space % block_rect.height)
    cnt = 0
    while y_pos < wall_rect.height:
        if cnt % 2: x_pos = 0
        else: x_pos = -block_rect.width//2

        while x_pos < wall_rect.width:
            wall.blit(block, (x_pos, y_pos))
            x_pos += block_rect.width

        if y_pos >= top_space:
            wall.blit(right_half_block, (side_space - piece_space, y_pos))
            wall.blit(left_half_block, (wall_rect.right - side_space, y_pos))

        cnt += 1
        y_pos += block_rect.height


    return wall


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
    names = ['New Game', 'Load Game', 'Records', 'Settings', 'Exit']
    button_types = [Button, Button, Button, Button, Button]
    buttons_width = [150, 150, 150, 150, 150]

    def new_game_c(arg):
        new_game(arg)
        arg.state_flag = GameS

    def settings_button(arg):
        arg.id_menu = 2
        arg.prev_id_menu = 0

    def empty_func(arg):
        pass

    funcs = [new_game_c, empty_func, empty_func, settings_button, close_game, close_game]

    return Menu(arg, button_types, names, buttons_width, funcs)


def restart(arg):
    arg.blocks.empty()
    make_target_wall(arg)

    arg.platform.restart(arg)
    arg.ball.restart(arg)


def new_game(arg):
    restart(arg)
    arg.stats.restart(arg)


def next_level(arg):
    print(1)
    restart(arg)
    arg.stats.increase_difficulty(arg)


def wasted(arg):
    #print('wasted')
    if arg.stats.training_flag:
        arg.population.end_game(arg)
    new_game(arg)


def close_game(arg):
    arg.stats.save_cur_session(arg)
    arg.population.save_cur_session(arg)
    exit()


def print_debug(arg):
    subscribers = ["All", "update_state", "bliting", "update_sing_ups"]
    for subscriber in subscribers:
        print(subscriber, arg.timemanager.get_sibscriber(subscriber, True), "%")
    print()