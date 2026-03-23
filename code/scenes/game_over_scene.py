from __future__ import annotations

import pygame

from code.const import C_PANEL, C_PANEL_BORDER, C_TEXT, C_SKY, FONT_NAME, WIN_HEIGHT, WIN_WIDTH
from code.scenes.base_scene import BaseScene


class GameOverScene(BaseScene):
    def __init__(self, game, score: int) -> None:
        super().__init__(game)
        self.score = score
        self.title_font = pygame.font.SysFont(FONT_NAME, 52, bold=True)
        self.text_font = pygame.font.SysFont(FONT_NAME, 28)
        self.small_font = pygame.font.SysFont(FONT_NAME, 22)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from code.scenes.game_scene import GameScene

                self.next_scene = GameScene(self.game)
            elif event.key == pygame.K_ESCAPE:
                from code.scenes.menu_scene import MenuScene

                self.next_scene = MenuScene(self.game)

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(C_SKY)
        panel = pygame.Rect(220, 140, 520, 230)
        pygame.draw.rect(screen, C_PANEL, panel, border_radius=20)
        pygame.draw.rect(screen, C_PANEL_BORDER, panel, width=2, border_radius=20)

        title = self.title_font.render('Game Over', True, C_TEXT)
        screen.blit(title, title.get_rect(center=(WIN_WIDTH // 2, 195)))

        score_text = self.text_font.render(f'Pontuação final: {self.score}', True, C_TEXT)
        best_text = self.small_font.render(f'Recorde da sessão: {self.game.best_score}', True, C_TEXT)
        replay_text = self.small_font.render('ENTER - jogar novamente | ESC - voltar ao menu', True, C_TEXT)

        screen.blit(score_text, score_text.get_rect(center=(WIN_WIDTH // 2, 245)))
        screen.blit(best_text, best_text.get_rect(center=(WIN_WIDTH // 2, 285)))
        screen.blit(replay_text, replay_text.get_rect(center=(WIN_WIDTH // 2, 330)))
