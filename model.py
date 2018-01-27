import pygame
import numpy as np
import param
import math
import time
import settings

infinity = 10**9

class Model:
    def __init__(self, arg):
        self.fitness = 0
        self.max_reward = -1
        self.body = [None, None]
        self.n_w = math.ceil(arg.settings.ga_width/param.width_box)
        self.n_h = math.ceil(arg.settings.ga_height/param.height_box)
        self.n_square = self.n_w * self.n_h

        self.wanna_left = False
        self.wanna_right = False
        self.apm = 0

    def move(self, arg):
        arg.ball.throw()

        input_data = self.make_input_vector(arg)
        input_data = np.concatenate((np.array([1.0, 20*arg.ball.velocity[0], 20*arg.ball.velocity[1]],float).flatten(),
                                     input_data.flatten()))
        input_data = np.dot(input_data, self.body[0])
        input_data = np.tanh(input_data)

        input_data = np.concatenate((np.array(1.0, float).flatten(), input_data.flatten()))
        input_data = np.dot(input_data, self.body[1])
        #print(input_data)
        input_data = np.tanh(input_data)


        if math.fabs(input_data[1]) > 0.1:
            if input_data[1] > 0:
                arg.platform.moving_left = False
                arg.platform.moving_right = True
                if self.wanna_left:
                    self.apm += 1
            else:
                arg.platform.moving_left = True
                arg.platform.moving_right = False
                if self.wanna_right:
                    self.apm += 1
            self.wanna_left = arg.platform.moving_left
            self.wanna_right = arg.platform.moving_right
        else:
            arg.platform.moving_left = False
            arg.platform.moving_right = False

    def make_input_vector(self, arg):
        sol = np.zeros((param.w_n, param.h_n))

        for item in arg.blocks.sprites():
            sol[item.intersected] = 1

        # self.dfs(arg.ball.rect, sol, arg.ball.rect.centerx//param.width_box, arg.ball.rect.centery//param.height_box, -10)
        # self.dfs(arg.platform.rect, sol, arg.platform.rect.centerx // param.width_box,
        #          arg.platform.rect.centery // param.height_box, 10)
        sol[arg.platform.make_intersected(arg)] = 10
        sol[arg.ball.make_intersected(arg)] = -10

        sol = sol.transpose()
        #print(sol)
        return sol

    def dfs(self, rect, sol, x, y, value):
        if x < 0 or x >= param.w_n:
            return
        if y < 0 or y >= param.h_n:
            return
        if sol[x, y] != 0:
            return
        v = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        if (param.left_side[x] < rect.right and param.right_side[x] > rect.left and
            param.top_side[y] < rect.bottom and param.bottom_side[y] > rect.top):
            sol[x, y] = value
            for vec in v:
                self.dfs(rect, sol, x+vec[0], y+vec[1], value)
        else:
            return


    def crossover(self, other, arg):
        sol = Model(arg)

        for i in range(2):
            a, b = self.body[i], other.body[i]
            r = np.random.rand(np.array(a.shape).prod()).reshape(a.shape)
            #print(r)
            sel = r < 0.5                                                            # Настраиваемое значение
            sol.body[i] = np.where(sel, a, a + (b - a)*np.random.rand())*0.99

        return sol

    def mutation(self, arg):
        sol = Model(arg)

        for i in range(2):
            a = self.body[i].copy()
            r = np.random.rand(np.array(a.shape).prod()).reshape(a.shape)
            sel = r < 0.3                                                          # Настраиваемое значение
            sol.body[i] = np.where(sel, a * (np.random.rand()*6 - 3), a)

            # r = np.random.rand(np.array(a.shape).prod()).reshape(a.shape)
            # sel = r < 0.1  # Настраиваемое значение
            # sol.body[i] = np.where(sel, a * (1.2), a)

        return sol

    def init_random(self):
        self.body[0] = np.random.random([self.n_square+1+2, param.hidden_n]) - 0.5
        self.body[1] = np.random.random([param.hidden_n+1, 3]) - 0.5

    def __str__(self):
        return str(self.body[0]) + '\n' + str(self.body[1])
        #return str(self.body[1])

    def __add__(self, other):
        return self.crossover(other)
