from __future__ import annotations

import pygame

from code.collision import CollisionSystem
from code.const import (
    C_GRASS,
    C_GROUND,
    C_SKY,
    EVENT_SCORE_TICK,
    EVENT_SPAWN_COIN,
    EVENT_SPAWN_OBSTACLE,
    GROUND_Y,
)
from code.entity_factory import EntityFactory
from code.hud import Hud
from code.scenes.base_scene import BaseScene


class GameScene(BaseScene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.player = EntityFactory.create('Player')
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.hud = Hud()
        self.parallax_x = 0

        pygame.time.set_timer(EVENT_SPAWN_OBSTACLE, 1450)
        pygame.time.set_timer(EVENT_SPAWN_COIN, 2100)
        pygame.time.set_timer(EVENT_SCORE_TICK, 200)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                self.player.jump()
            elif event.key == pygame.K_ESCAPE:
                from code.scenes.menu_scene import MenuScene

                self._stop_timers()
                self.next_scene = MenuScene(self.game)
        elif event.type == EVENT_SPAWN_OBSTACLE:
            self.obstacles.append(EntityFactory.create('Obstacle'))
        elif event.type == EVENT_SPAWN_COIN:
            self.coins.append(EntityFactory.create('Coin'))
        elif event.type == EVENT_SCORE_TICK:
            self.score += 5
            if self.score > self.game.best_score:
                self.game.best_score = self.score

    def update(self) -> None:
        self.parallax_x = (self.parallax_x + 4) % 120
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        for obstacle in self.obstacles:
            obstacle.update()
        for coin in self.coins:
            coin.update()

        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.alive]
        self.coins = [coin for coin in self.coins if coin.alive]

        player_hit, bonus = CollisionSystem.resolve(self.player, self.obstacles, self.coins)
        self.score += bonus
        if self.score > self.game.best_score:
            self.game.best_score = self.score

        if player_hit:
            self._stop_timers()
            from code.scenes.game_over_scene import GameOverScene

            self.next_scene = GameOverScene(self.game, self.score)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(C_SKY)
        self._draw_cloud_bands(screen)
        self._draw_ground(screen)

        for coin in self.coins:
            coin.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        self.player.draw(screen)
        self.hud.draw(screen, self.score, self.game.best_score)

    def _draw_cloud_bands(self, screen: pygame.Surface) -> None:
        for base_x in range(-120, 1080, 180):
            x = base_x - self.parallax_x
            pygame.draw.ellipse(screen, (255, 255, 255), (x, 85, 80, 28))
            pygame.draw.ellipse(screen, (255, 255, 255), (x + 35, 72, 85, 34))

    def _draw_ground(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, C_GRASS, (0, GROUND_Y - 10, 960, 12))
        pygame.draw.rect(screen, C_GROUND, (0, GROUND_Y, 960, 110))
        for x in range(-40, 1000, 45):
            offset = (x - self.parallax_x * 2) % 1040 - 40
            pygame.draw.line(screen, (141, 110, 99), (offset, GROUND_Y + 18), (offset + 20, GROUND_Y + 18), 3)

    @staticmethod
    def _stop_timers() -> None:
        pygame.time.set_timer(EVENT_SPAWN_OBSTACLE, 0)
        pygame.time.set_timer(EVENT_SPAWN_COIN, 0)
        pygame.time.set_timer(EVENT_SCORE_TICK, 0)
