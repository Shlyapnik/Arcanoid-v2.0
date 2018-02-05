import sys
import pygame
import math
import time

from items import Block, Ball, Platform
from enums import MenuS, GameS



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


def blit_screen(arg):
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
        arg.tm.write_down("1")
        arg.speed_score.update()

        arg.score_table.update()
        arg.best_score_table.update()
        arg.lives_table.update()
        arg.level_table.update()
        arg.time_table.update()
        arg.tm.write_down("2")
    elif arg.state_flag == MenuS:
        pass


def make_target_wall(arg):
    number_in_row = (arg.settings.ga_width - 4)//arg.settings.target_width
    side_space = (arg.settings.ga_width - number_in_row * arg.settings.target_width)//2


    for i in range(arg.settings.width_target_wall):
        x_pos, y_pos = side_space, arg.settings.space_target + i * arg.settings.target_height

        while(x_pos + arg.settings.target_width <= arg.game_area.rect.width - side_space):
            arg.top_space, arg.left_space = y_pos, x_pos
            arg.blocks.add(Block(arg))

            x_pos += arg.settings.target_width



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
    arg.stats.lives -= 1

    if arg.stats.training_flag:
        arg.population.end_game(arg)
        new_game(arg)
    else:
        if arg.stats.lives == 0:
            new_game(arg)
        else:
            next_level(arg)



def close_game(arg):
    arg.stats.save_cur_session(arg)
    arg.population.save_cur_session(arg)
    exit()
