import param
import random
import shelve
import math
import numpy as np
from individual import Individual
from model import Model

infinity = 10**9

class Population:
    def __init__(self, arg):
        self.cur_bot_id = 0
        self.max_live_bot = 3
        self.cur_live_bot = 1

        self.shift_between_era = 10
        self.sum_population = None

        self.epoch = 1
        self.population = []
        for i in range(param.max_population):
            new_model = Model(arg)
            new_model.init_random()
            self.population.append(new_model)
        self.count_sum(arg)

    def get_best(self):
        sol_id = 0 if not self.cur_bot_id else 1
        for i in range(len(self.population)):
            if i == self.cur_bot_id:
                if self.population[i].fitness/self.cur_live_bot > self.population[sol_id].fitness:
                   sol_id = i
            elif self.population[i].fitness > self.population[sol_id].fitness:
                sol_id = i
        return self.population[sol_id]

    def crossover(self, arg):
        cur_tail = 1
        for i in range(len(self.population)):
            mdl = self.population[i]
            n = max(0, int(math.ceil(cur_tail * param.max_population * param.magic_value)))

            for i in range(n):
                rnd_id = random.randint(0, len(self.population)-1)
                self.population.append(mdl.crossover(self.population[rnd_id], arg))

            cur_tail *= (1 - param.magic_value)

    def selection(self):
        self.sort_population()
        self.population = self.population[:param.max_population]

    def mutation(self, arg):
        for i in range(len(self.population)):
            if random.random() < param.mut_chance:                      # Ещё одно значение для настройки
                self.population.append(self.population[i].mutation(arg))

    def sort_population(self):
        self.population = sorted(self.population, key=lambda x: -x.fitness)

    def next_model(self, arg):
        if self.cur_live_bot == self.max_live_bot:
            self.population[self.cur_bot_id].fitness /= self.max_live_bot
            self.cur_live_bot = 1
        else:
            self.cur_live_bot += 1
            return

        print(self.cur_bot_id, 'бот изучен с резом -', self.population[self.cur_bot_id].fitness)
        for i in range(self.cur_bot_id+1, len(self.population)):
            self.cur_bot_id = i
            self.population[i].fitness = 0
            return

        print('Эпоха', self.epoch)
        print("Best result = ", self.get_best().fitness)
        self.epoch += 1
        self.selection()
        self.crossover(arg)
        self.mutation(arg)
        self.count_sum(arg)

        self.cur_bot_id = 0
        self.population[0].fitness = 0

    def count_sum(self, arg):
        body = [np.zeros_like(self.population[0].body[i]) for i in range(2)]
        for mdl in self.population:
            for i in range(2):
                body[i] = body[i] + mdl.body[i]
        body = [body[i] / len(self.population) for i in range(2)]
        self.sum_population = body

    def end_game(self, arg):
        bot = self.population[self.cur_bot_id]
        differ = sum(np.sum((self.sum_population[i] - bot.body[i])**2) for i in range(2))
        if (self.epoch//self.shift_between_era) % 2 == 1:
            # + Отличие от других

            print(differ)
            #print(bot.apm)
            #self.population[self.cur_bot_id].fitness += min(arg.stats.count - bot.apm*param.apm_scale + differ*param.differ_scale,
            #                                               self.population[self.cur_bot_id].fitness)
            self.population[self.cur_bot_id].fitness += arg.stats.count - bot.apm*param.apm_scale + differ*param.differ_scale
        else:
            # Без отличия от других
            #print(bot.apm)
            print(differ)
            #self.population[self.cur_bot_id].fitness = min(arg.stats.count - bot.apm*param.apm_scale,
            #                                               self.population[self.cur_bot_id].fitness)
            self.population[self.cur_bot_id].fitness += arg.stats.count - bot.apm*param.apm_scale
        bot.apm = 0

        self.next_model(arg)

    def move(self, arg):
        self.population[self.cur_bot_id].move(arg)

    def load_prev_session(self, arg):
        stats_db = shelve.open('db/population_db')

        self.population = stats_db.get('population', self.population)
        self.cur_bot_id = stats_db.get('cur_bot_id', 0)
        self.cur_live_bot = stats_db.get('cur_live_bot', 0)
        self.epoch = stats_db.get('epoch', 0)
        self.count_sum(arg)

        stats_db.close()

    def save_cur_session(self, arg):
        stats_db = shelve.open('db/population_db')

        stats_db['population'] = self.population
        stats_db['cur_bot_id'] = self.cur_bot_id
        stats_db['cur_live_bot'] = self.cur_live_bot
        stats_db['epoch'] = self.epoch

        stats_db.close()
