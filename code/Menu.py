import sys

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.Const import C_WHITE, C_YELLOW, MENU_OPTION, WIN_WIDTH, C_BROWN


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./asset/MenuBg.png").convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load("./asset/Menu.wav")
        pygame.mixer_music.set_volume(0.35)
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Cat Jump", C_YELLOW, ((WIN_WIDTH / 2), 78))
            self.menu_text(20, "Pule obstáculos e pegue moedas", C_BROWN, ((WIN_WIDTH / 2), 114))
            self.menu_text(16, "ESPAÇO / SETA CIMA para pular", C_WHITE, ((WIN_WIDTH / 2), 144))
            self.menu_text(16, "ENTER para escolher a opção", C_WHITE, ((WIN_WIDTH / 2), 170))

            for i, option in enumerate(MENU_OPTION):
                color = C_YELLOW if i == menu_option else C_WHITE
                self.menu_text(24, option, color, ((WIN_WIDTH / 2), 208 + 34 * i))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size, bold=True)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
