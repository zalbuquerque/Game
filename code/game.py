from __future__ import annotations

import pygame

from code.const import FPS, GAME_TITLE, WIN_HEIGHT, WIN_WIDTH
from code.scenes.menu_scene import MenuScene


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.best_score = 0
        self.current_scene = MenuScene(self)

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.flip()

            if self.current_scene.next_scene is not None:
                self.current_scene = self.current_scene.next_scene

        pygame.quit()
