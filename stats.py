import pygame
import shelve
import os

class Stats:
    def __init__(self, arg):
        self.max_count = 0
        self.lives = 0
        self.count = 0
        self.start_time = 0
        self.reward = 0
        self.ball_velocity = 1
        self.level = 1

        self.cheat_mode = True
        self.bot_activate = False
        self.training_flag = True
        self.visualising_flag = True

    def restart(self, arg):
        self.start_time = pygame.time.get_ticks()
        self.lives = arg.settings.max_lives
        self.reward = arg.settings.default_reward
        arg.ball.alpha_velocity = arg.settings.ball_velocity
        self.count = 0
        self.level = 1

    def add(self, inc_score):
        self.count += inc_score
        self.max_count = max(self.max_count, self.count)

    def increase_difficulty(self, arg):
        self.level += 1
        arg.ball.alpha_velocity *= 1.2

    def check_and_correct_db(self):
        if not os.path.exists("db/"):
            os.mkdir("db")

    def save_cur_session(self, arg):
        self.check_and_correct_db
        stats_db = shelve.open('db/stats_db')

        stats_db['max_score'] = self.max_count
        stats_db['cheat_mode'] = self.cheat_mode
        stats_db['visualising'] = self.visualising_flag
        stats_db['training_flag'] = self.training_flag

        stats_db.close()

    def load_prev_session(self, arg):
        self.check_and_correct_db()
        stats_db = shelve.open('db/stats_db')

        self.max_count = stats_db.get('max_score', 0)
        self.cheat_mode = stats_db.get('cheat_mode', True)
        self.visualising_flag = stats_db.get('visualising', True)
        self.training_flag = stats_db.get("training_flag", True)

        stats_db.close()
