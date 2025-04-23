from settings import *
import pygame
import os
from os.path import join


class Score:
    def __init__(self, graphics_dir):
        self.display_surface = pygame.display.get_surface()
        font_path = join(graphics_dir, "Russo_One.ttf")

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.font = pygame.font.Font(font_path, 30)

        # Scores
        self.lines = 0
        self.score = 0
        self.level = 1

        # Surface
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION)
        )
        self.rect = self.surface.get_rect(
            bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING)
        )

    def draw_text(self, text, y, color=WHITE):
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(self.surface.get_width() / 2, y))
        self.surface.blit(text_surf, text_rect)

    def run(self):
        self.surface.fill(GRAY)
        self.draw_text("LINES", 30)
        self.draw_text(str(self.lines), 60)
        self.draw_text("SCORE", 120)
        self.draw_text(str(self.score), 150)
        self.draw_text("LEVEL", 210)
        self.draw_text(str(self.level), 240)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
