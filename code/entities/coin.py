from __future__ import annotations

import random
import pygame

from code.const import C_COIN, GROUND_Y, SCROLL_SPEED, WIN_WIDTH
from code.entity import Entity


class Coin(Entity):
    def __init__(self) -> None:
        y = random.choice((GROUND_Y - 40, GROUND_Y - 95, GROUND_Y - 145))
        rect = pygame.Rect(WIN_WIDTH + random.randint(50, 150), y, 24, 24)
        super().__init__('Coin', rect)

    def update(self) -> None:
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.alive = False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(surface, C_COIN, self.rect)
