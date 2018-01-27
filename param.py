from settings import Settings
import math
import numpy as np

settings = Settings()

apm_scale = 0
differ_scale = 1
side_penalty = 0.1

mut_chance = 0.05
max_population = 20
magic_value = 0.30

width_box, height_box = 80, 80
w_n = math.ceil(settings.ga_width/width_box)
h_n = math.ceil(settings.ga_height/height_box)

left_side = np.arange(0.0, settings.ga_width, width_box)
right_side = left_side + width_box
top_side = np.arange(0, settings.ga_height, height_box)
bottom_side = top_side + height_box

hidden_n = 5
