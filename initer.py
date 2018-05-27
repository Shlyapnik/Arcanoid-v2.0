import pygame

from label import Label
from game_area import Game_area
from stats import Stats
from menu import Menu, make_menus
from pygame.sprite import Group, groupcollide, spritecollide
from items import Block, Ball, Platform
from timemanager import Timemanager
from population import Population

# Нужно будет реорганизвать все эти непонятные функции
from game_functions import new_game, wasted, next_level



class Initer:
    def __init__(self):
        pass

    def __call__(self, arg):
        # Загружаем стену
        arg.wall = self.make_wall('images/break.bmp', arg)

        # Создаём территорию для игры
        arg.game_area = Game_area(arg)

        # Создаём класс для подсчёта очков
        arg.stats = Stats(arg)
        arg.stats.load_prev_session(arg)

        # Создаём популяцию для обучения
        arg.population = Population(arg)
        arg.population.load_prev_session(arg)

        # Создаём объект платформы
        arg.image_name = 'images/new/platform 120x20.png'
        arg.platform = Platform(arg)

        # Создаём шар для игры
        arg.radius = 10
        arg.image_name = 'images/new/ball_aparture 20x20.png'
        arg.ball = Ball(arg)
        arg.platform.link_with_ball(arg)

        # Создаём меню
        make_menus(arg)

        # Создаём блоки для ломания
        arg.image_name = 'images/new/block_'
        arg.blocks = Group()

        # Создаём Таймменеджер
        arg.tm = Timemanager(arg.settings.length_of_log)

        arg.tm.sing_up("be all", "af ch_ev", "check_event")
        arg.tm.sing_up("af ch_ev", "af up_state", "update_state")
        arg.tm.sing_up("af up_state", "af bliting", "bliting")
        arg.tm.sing_up("af bliting", "af up_sing_ups", "update_sing_ups")
        arg.tm.sing_up("be all", "af up_sing_ups", "All")

        arg.tm.sing_up("1", "2", "updating score tables")

        # Создаём разнообразные панели для вывода резов
        self.make_tables(arg)

        # -------------------------------------------------------------------------------------
        # Привязываем конец игры к нужным функциям
        arg.next_level = next_level
        arg.wasted = wasted


    def make_tables(self, arg):
        arg.top_space = 10
        arg.left_space = arg.settings.screen_width - 90
        arg.fps_score = Label(arg, 'FPS:', lambda: int(
                
                1000.0 / max(1, 
                    arg.tm.get_sibscriber("All", False, False) / 
                    max(1, arg.tm.get_sibscriber("All", False, True))
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

    
    def make_wall(self, name, arg):
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