import pygame

from pygame.sprite import Sprite

class Label(Sprite):
    def __init__(self, arg, static_text, call_func):
        self.screen = arg.screen
        self.screen_rect = arg.screen.get_rect()
        self.ai_settings = arg.settings

        self.left_space = arg.left_space
        self.top_space = arg.top_space

        self.static_text = static_text
        self.func_text = call_func

        self.text_color = (230, 230, 130)
        self.font = pygame.ftfont.SysFont(None, 32)
        self.prep_text()

    def prep_text(self):
        text = '{0}{1}'.format(self.static_text, self.func_text())

        self.text_image = self.font.render(text, True, self.text_color)
        self.image_rect = self.text_image.get_rect()
        self.image_rect.top = self.top_space
        self.image_rect.left = self.left_space

    def update(self):
        self.prep_text()

    def blit(self):
        self.screen.blit(self.text_image, self.image_rect)