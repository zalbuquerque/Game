from __future__ import annotations

import pygame

from code.const import (
    C_PLAYER,
    C_TEXT_LIGHT,
    GRAVITY,
    GROUND_Y,
    JUMP_STRENGTH,
    MAX_FALL_SPEED,
    PLAYER_SPEED,
)
from code.entity import Entity


class Player(Entity):
    def __init__(self) -> None:
        rect = pygame.Rect(120, GROUND_Y - 64, 46, 64)
        super().__init__('Player', rect)
        self.velocity_y = 0.0
        self.on_ground = True
        self.jump_buffer = 0

    def jump(self) -> None:
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self, pressed_keys: pygame.key.ScancodeWrapper | None = None) -> None:
        if pressed_keys:
            if pressed_keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= PLAYER_SPEED
            if pressed_keys[pygame.K_d] and self.rect.right < 960:
                self.rect.x += PLAYER_SPEED

        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        self.rect.y += int(self.velocity_y)

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, C_PLAYER, self.rect, border_radius=10)
        eye = pygame.Rect(self.rect.x + 28, self.rect.y + 16, 8, 8)
        pygame.draw.rect(surface, C_TEXT_LIGHT, eye, border_radius=4)
