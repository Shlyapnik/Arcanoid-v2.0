import pygame
import pygame.ftfont

class Button:
    def __init__(self, arg, screen, surface, pos, text, func):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.surface = surface
        self.pos = pos

        self.selected = False

        self.text = text
        self.active_color = (255, 230, 230)
        self.nonactive_color = (180, 160, 180)

        self.func = func

        self.font = pygame.ftfont.SysFont(None, 32)

        self.prep_msg(arg)

    def prep_msg(self, arg):
        active_state_text = self.font.render(self.text, True, self.active_color)

        if not arg.wide_button_flag:
            self.active_image = pygame.image.load('images/new/active_button 150x60.png')
        else:
            self.active_image = pygame.image.load('images/new/active_button 200x40.png')
        temp_rect = active_state_text.get_rect()
        temp_rect.centerx = self.active_image.get_rect().width//2
        temp_rect.centery = self.active_image.get_rect().height//2
        self.active_image.blit(active_state_text, temp_rect)

        nonactive_state_text = self.font.render(self.text, True, self.nonactive_color)

        if not arg.wide_button_flag:
            self.nonactive_image = pygame.image.load('images/new/nonactive_button 150x60.png')
        else:
            self.nonactive_image = pygame.image.load('images/new/nonactive_button 200x40.png')
        self.nonactive_image.blit(nonactive_state_text, temp_rect)

    def update(self, cursor_pos):
        pass

    def set_selected(self, selected):
        self.selected = selected

    def blit(self):
        if self.surface:
            self.surface.fill((0, 0, 0), self.surface.get_rect())
            self.surface.set_colorkey((0, 0, 0))

            if self.selected:
                self.surface.blit(self.active_image, (0, 0))
            else:
                self.surface.blit(self.nonactive_image, (0, 0))
            self.screen.blit(self.surface, self.pos)
        else:
            if self.selected:
                self.screen.blit(self.active_image, self.pos)
            else:
                self.screen.blit(self.nonactive_image, self.pos)
