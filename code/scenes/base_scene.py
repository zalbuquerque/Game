from __future__ import annotations

from abc import ABC, abstractmethod
import pygame


class BaseScene(ABC):
    def __init__(self, game) -> None:
        self.game = game
        self.next_scene = None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
