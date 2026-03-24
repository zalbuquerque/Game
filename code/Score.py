import sys
from datetime import datetime

import pygame
from pygame import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN, Rect, Surface
from pygame.font import Font

from code.Const import C_WHITE, C_YELLOW, PLAYER_NAME_SIZE, SCORE_POS
from code.DBProxy import DBProxy


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load("./asset/ScoreBg.png").convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.game_over_surf = pygame.image.load("./asset/GameOverBg.png").convert_alpha()
        self.game_over_rect = self.game_over_surf.get_rect(left=0, top=0)

    def save(self, final_score: int):
        pygame.mixer_music.load("./asset/Score.wav")
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy("DBScore")
        name = ""

        while True:
            self.window.blit(source=self.game_over_surf, dest=self.game_over_rect)
            self.score_text(42, "FIM DE JOGO", C_YELLOW, SCORE_POS["Title"])
            self.score_text(20, f"Score final: {final_score}", C_WHITE, SCORE_POS["Subtitle"])
            self.score_text(18, f"Digite seu nome ({PLAYER_NAME_SIZE} letras)", C_WHITE, SCORE_POS["Label"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    db_proxy.close()
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == PLAYER_NAME_SIZE:
                        db_proxy.save({"name": name.upper(), "score": final_score, "date": get_formatted_date()})
                        db_proxy.close()
                        self.show()
                        return
                    if event.key == K_ESCAPE:
                        db_proxy.close()
                        return
                    if event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif event.unicode.isalpha() and len(name) < PLAYER_NAME_SIZE:
                        name += event.unicode.upper()

            self.score_text(28, name or "____", C_YELLOW, SCORE_POS["Name"])
            pygame.display.flip()

    def show(self):
        pygame.mixer_music.load("./asset/Score.wav")
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy("DBScore")
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(42, "TOP 10 SCORE", C_YELLOW, SCORE_POS["Title"])
            self.score_text(18, "ESC para voltar", C_WHITE, SCORE_POS["Subtitle"])
            self.score_text(20, "NOME   SCORE     DATA", C_YELLOW, SCORE_POS["Label"])

            for index, player_score in enumerate(list_score):
                _, name, score, date = player_score
                self.score_text(18, f"{name:<4}   {score:05d}   {date}", C_WHITE, SCORE_POS[index])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return

            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size, bold=True)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
