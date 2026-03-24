import sys

import pygame

from code.Const import MENU_OPTION, WIN_HEIGHT, WIN_WIDTH
from code.Level import Level
from code.Menu import Menu
from code.Score import Score


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cat Jump")
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        score = Score(self.window)

        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                level = Level(self.window)
                final_score = level.run()
                score.save(final_score)
            elif menu_return == MENU_OPTION[1]:
                score.show()
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                sys.exit()
