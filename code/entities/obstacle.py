from __future__ import annotations

import random
import pygame

from code.const import C_OBSTACLE, GROUND_Y, SCROLL_SPEED, WIN_WIDTH
from code.entity import Entity


class Obstacle(Entity):
    def __init__(self) -> None:
        width = random.choice((28, 36, 44))
        height = random.choice((46, 58, 74))
        rect = pygame.Rect(WIN_WIDTH + random.randint(0, 100), GROUND_Y - height, width, height)
        super().__init__('Obstacle', rect)

    def update(self) -> None:
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.alive = False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, C_OBSTACLE, self.rect, border_radius=8)
