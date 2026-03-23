from __future__ import annotations

from abc import ABC, abstractmethod
import pygame


class Entity(ABC):
    def __init__(self, name: str, rect: pygame.Rect):
        self.name = name
        self.rect = rect
        self.alive = True

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError
