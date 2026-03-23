from __future__ import annotations

from code.entities.coin import Coin
from code.entities.obstacle import Obstacle
from code.entities.player import Player


class CollisionSystem:
    @staticmethod
    def resolve(player: Player, obstacles: list[Obstacle], coins: list[Coin]) -> tuple[bool, int]:
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                return True, 0

        collected = 0
        for coin in coins:
            if coin.alive and player.rect.colliderect(coin.rect):
                coin.alive = False
                collected += 25

        return False, collected
