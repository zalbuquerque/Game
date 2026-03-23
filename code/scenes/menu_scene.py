from __future__ import annotations

import pygame

from code.const import C_PANEL, C_PANEL_BORDER, C_TEXT, C_TEXT_LIGHT, C_SKY, FONT_NAME, GAME_TITLE, WIN_HEIGHT, WIN_WIDTH
from code.scenes.base_scene import BaseScene


class MenuScene(BaseScene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.title_font = pygame.font.SysFont(FONT_NAME, 58, bold=True)
        self.text_font = pygame.font.SysFont(FONT_NAME, 28)
        self.small_font = pygame.font.SysFont(FONT_NAME, 22)
        self.blink = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from code.scenes.game_scene import GameScene

                self.next_scene = GameScene(self.game)
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False

    def update(self) -> None:
        self.blink = (self.blink + 1) % 60

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(C_SKY)

        title = self.title_font.render(GAME_TITLE, True, C_TEXT)
        title_rect = title.get_rect(center=(WIN_WIDTH // 2, 95))
        screen.blit(title, title_rect)

        subtitle = self.text_font.render('Demo jogável de plataforma 2D', True, C_TEXT)
        screen.blit(subtitle, subtitle.get_rect(center=(WIN_WIDTH // 2, 150)))

        panel = pygame.Rect(185, 205, 590, 210)
        pygame.draw.rect(screen, C_PANEL, panel, border_radius=20)
        pygame.draw.rect(screen, C_PANEL_BORDER, panel, width=2, border_radius=20)

        lines = [
            'Controles:',
            'ENTER - Iniciar jogo',
            'SPACE / W / SETA PARA CIMA - Pular',
            'A e D - Mover para esquerda e direita',
            'ESC - Sair',
            'Objetivo: desviar dos obstáculos e coletar moedas.',
        ]

        for index, text in enumerate(lines):
            surf = self.small_font.render(text, True, C_TEXT)
            screen.blit(surf, (220, 235 + index * 28))

        if self.blink < 30:
            prompt = self.text_font.render('Pressione ENTER para jogar', True, C_TEXT_LIGHT)
            prompt_bg = pygame.Rect(310, 450, 340, 46)
            pygame.draw.rect(screen, C_TEXT, prompt_bg, border_radius=14)
            screen.blit(prompt, prompt.get_rect(center=prompt_bg.center))
