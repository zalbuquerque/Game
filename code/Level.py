import random
import sys

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.Background import Background
from code.Const import C_BLACK, C_BROWN, C_GREEN, C_RED, C_WHITE, COIN_SCORE, FPS, GROUND_Y, WIN_HEIGHT, WIN_WIDTH


class Level:
    def __init__(self, window: Surface):
        self.window = window
        self.backgrounds = self._load_backgrounds()
        self.obstacle_ground_offset = 5
        self.player_surf = pygame.image.load("./asset/Player1.png").convert_alpha()
        self.player_surf = pygame.transform.smoothscale(self.player_surf, (72, 56))
        self.player_rect = self.player_surf.get_rect(left=88, bottom=GROUND_Y)
        self.player_mask = pygame.mask.from_surface(self.player_surf)
        self.player_velocity_y = 0.0
        self.gravity = 0.68
        self.jump_strength = -13.2

        self.obstacle_surfaces = self._load_obstacle_surfaces()
        self.obstacles: list[dict] = []
        self.coins: list[dict] = []

        self.base_speed = 5.2
        self.distance_score = 0.0
        self.coin_score = 0
        self.spawn_obstacle_timer = 0
        self.next_obstacle_spawn = random.randint(65, 110)
        self.spawn_coin_timer = 0
        self.next_coin_spawn = random.randint(90, 150)

    def run(self) -> int:
        pygame.mixer_music.load("./asset/Level1.wav")
        pygame.mixer_music.set_volume(0.25)
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw(clock)

            if self._check_collision():
                pygame.mixer_music.stop()
                return self.score

    @property
    def score(self) -> int:
        return int(self.distance_score) + self.coin_score

    def _load_backgrounds(self) -> list[Background]:
        backgrounds = []
        for index in range(7):
            backgrounds.append(Background(f"Level1Bg{index}", (0, 0)))
            backgrounds.append(Background(f"Level1Bg{index}", (WIN_WIDTH, 0)))
        return backgrounds

    def _load_obstacle_surfaces(self) -> list[Surface]:
        enemy_1 = pygame.image.load("./asset/Enemy1.png").convert_alpha()
        enemy_2 = pygame.image.load("./asset/Enemy2.png").convert_alpha()
        return [
            pygame.transform.smoothscale(enemy_1, (72, 48)),
            pygame.transform.smoothscale(enemy_2, (92, 58)),
        ]

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if self.player_rect.bottom >= GROUND_Y:
                    self.player_velocity_y = self.jump_strength

    def _update(self):
        self.distance_score += 0.32
        current_speed = self.base_speed + min(4.5, self.distance_score / 180)

        for background in self.backgrounds:
            background.move()

        self.player_velocity_y += self.gravity
        self.player_rect.y += round(self.player_velocity_y)
        if self.player_rect.bottom >= GROUND_Y:
            self.player_rect.bottom = GROUND_Y
            self.player_velocity_y = 0

        self.spawn_obstacle_timer += 1
        if self.spawn_obstacle_timer >= self.next_obstacle_spawn:
            self.spawn_obstacle_timer = 0
            self.next_obstacle_spawn = random.randint(55, 105)
            surf = random.choice(self.obstacle_surfaces)
            rect = surf.get_rect(
                left=WIN_WIDTH + random.randint(0, 40),
                bottom=GROUND_Y + self.obstacle_ground_offset,
            )
            self.obstacles.append(
                {
                    "surf": surf,
                    "rect": rect,
                    "speed": current_speed,
                    "mask": pygame.mask.from_surface(surf),
                }
            )

        self.spawn_coin_timer += 1
        if self.spawn_coin_timer >= self.next_coin_spawn:
            self.spawn_coin_timer = 0
            self.next_coin_spawn = random.randint(85, 150)
            radius = 10
            coin_rect = Rect(WIN_WIDTH + random.randint(20, 80), random.randint(145, GROUND_Y - 48), radius * 2, radius * 2)
            self.coins.append({"rect": coin_rect, "speed": current_speed, "radius": radius})

        for obstacle in self.obstacles:
            obstacle["rect"].x -= round(obstacle["speed"])
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle["rect"].right > -10]

        for coin in self.coins:
            coin["rect"].x -= round(coin["speed"])
        self.coins = [coin for coin in self.coins if coin["rect"].right > -10]

        collected = []
        for coin in self.coins:
            if self._player_hitbox().colliderect(coin["rect"]):
                collected.append(coin)
                self.coin_score += COIN_SCORE
        self.coins = [coin for coin in self.coins if coin not in collected]

    def _check_collision(self) -> bool:
        for obstacle in self.obstacles:
            offset = (
                obstacle["rect"].left - self.player_rect.left,
                obstacle["rect"].top - self.player_rect.top,
            )
            if self.player_mask.overlap(obstacle["mask"], offset):
                return True
        return False

    def _player_hitbox(self) -> Rect:
        return Rect(
            self.player_rect.left + 12,
            self.player_rect.top + 10,
            self.player_rect.width - 24,
            self.player_rect.height - 14,
        )

    def _draw(self, clock):
        for background in self.backgrounds:
            self.window.blit(source=background.surf, dest=background.rect)

        ground_rect = Rect(0, GROUND_Y, WIN_WIDTH, WIN_HEIGHT - GROUND_Y)
        pygame.draw.rect(self.window, C_BROWN, ground_rect)
        pygame.draw.rect(self.window, C_GREEN, Rect(0, GROUND_Y, WIN_WIDTH, 6))

        for coin in self.coins:
            pygame.draw.circle(self.window, (255, 214, 10), coin["rect"].center, coin["radius"])
            pygame.draw.circle(self.window, C_WHITE, coin["rect"].center, coin["radius"], 2)

        for obstacle in self.obstacles:
            self.window.blit(source=obstacle["surf"], dest=obstacle["rect"])

        self.window.blit(source=self.player_surf, dest=self.player_rect)

        self.level_text(20, f"Score: {self.score}", C_WHITE, (12, 10))
        self.level_text(18, f"Moedas: {self.coin_score}", C_WHITE, (12, 36))
        self.level_text(16, "Pule com ESPAÇO ou SETA CIMA", C_BROWN, (12, 62))
        self.level_text(14, f"FPS: {clock.get_fps():.0f}", C_RED, (12, 86))
        pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size, bold=True)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
