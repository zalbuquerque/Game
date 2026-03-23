from __future__ import annotations

import pygame

from code.const import C_PANEL, C_PANEL_BORDER, C_TEXT, FONT_NAME


class Hud:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont(FONT_NAME, 26, bold=True)
        self.small_font = pygame.font.SysFont(FONT_NAME, 18)

    def draw(self, screen: pygame.Surface, score: int, best_score: int) -> None:
        panel = pygame.Rect(18, 18, 220, 78)
        pygame.draw.rect(screen, C_PANEL, panel, border_radius=14)
        pygame.draw.rect(screen, C_PANEL_BORDER, panel, width=2, border_radius=14)

        score_surf = self.font.render(f'Pontos: {score}', True, C_TEXT)
        best_surf = self.small_font.render(f'Recorde da sessão: {best_score}', True, C_TEXT)
        screen.blit(score_surf, (34, 34))
        screen.blit(best_surf, (34, 66))
