import pygame

from queue import Queue
from enums import avrM, avr_diffM, arv_dist_pointM

class Timemanager:
    def __init__(self):
        self.length_of_log = 100
        self.storage = Queue()

        self.sing_ups_size = 0
        self.sing_ups = list()

    def sing_up(self, name1, name2, description):
        self.sing_ups_size += 1
        self.sing_ups.append((name1, name2, 0, 0, 0, description, 0))

    def write_down(self, name):
        if self.storage.size == self.length_of_log:
            self.storage.pop()

        self.storage.push((name, pygame.time.get_ticks()))

    def get_sibscriber(self, description, relative=False, get_count=False):
        for item in self.sing_ups:
            if item[5] == description:
                if not get_count:
                    if not relative:
                        # print(item[4])
                        return item[4]
                    else:
                        return item[4] / self.get_full_time()
                else:
                    # print(item[6])
                    return item[6]
        
        raise RuntimeError("Не существует подписки с таким именем: ", description)

    def get_full_time(self):
        return self.storage.front()[1] - self.storage.tail()[1]

    def update_sing_ups(self):

        notes = [item for item in self.storage]
        # sing_up = [name1, name2, name_iter, first_time, sum_time, description, count]
        self.sing_ups = [[item[0], item[1], 0, 0, 0, item[5], 0] for item in self.sing_ups]
        full_time = notes[-1][1] - notes[0][1]

        for note in notes:
            for sing_up in self.sing_ups:
                name_id = sing_up[2]
                note_name, note_time = note

                if note_name == sing_up[name_id]:
                    if name_id == 0:
                        sing_up[2] = 1
                        sing_up[3] = note_time
                    else:
                        sing_up[2] = 0
                        sing_up[6] += 1
                        sing_up[4] += note_time - sing_up[3]
            