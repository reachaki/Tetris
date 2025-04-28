from settings import *
from sys import exit
from os.path import join, dirname, abspath
import pygame
import os

# components
from game import Game
from score import Score
from preview import Preview

from random import choice


class Main:
    def __init__(self):
        # Initialise pygame
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")

        # Base directory setup for assets
        base_dir = dirname(dirname(abspath(__file__)))
        self.sound_dir = join(base_dir, "sound")
        self.graphics_dir = join(base_dir, "graphics")

        # Game states
        self.states = {"start": True, "playing": False, "game_over": False}

        # Prepare shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for _ in range(3)]

        # Initialise components
        self.set_game_over = lambda: self.set_game_over_state()
        self.game = Game(self.get_next_shape, self.update_score, self.set_game_over)
        self.score = Score(graphics_dir=self.graphics_dir)
        self.preview = Preview(graphics_dir=self.graphics_dir)

        # Font for start/game over screens
        font_path = join(self.graphics_dir, "Russo_One.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 40)
            self.small_font = pygame.font.Font(font_path, 30)
        else:
            self.font = pygame.font.SysFont("Arial", 40)
            self.small_font = pygame.font.SysFont("Arial", 30)

        # Load music
        music_path = join(self.sound_dir, "music.wav")
        if os.path.exists(music_path):
            self.music = pygame.mixer.Sound(music_path)
            self.music.set_volume(0.05)
        else:
            self.music = None

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def set_game_over_state(self):
        self.states["playing"] = False
        self.states["game_over"] = True
        if self.music:
            self.music.stop()

    def draw_start_screen(self):
        self.display_surface.fill(GRAY)

        # Title
        title = self.font.render("TETRIS", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.display_surface.blit(title, title_rect)

        # Start instruction
        instruction = self.small_font.render("Press SPACE to Start", True, WHITE)
        instruction_rect = instruction.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        self.display_surface.blit(instruction, instruction_rect)

    def draw_game_over_screen(self):
        self.display_surface.fill(GRAY)

        # Game over text
        game_over = self.font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        )
        self.display_surface.blit(game_over, game_over_rect)

        # Score display
        score_text = self.small_font.render(f"Score: {self.score.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface.blit(score_text, score_rect)

        # Restart instruction
        instruction = self.small_font.render("Press SPACE to Restart", True, WHITE)
        instruction_rect = instruction.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3)
        )
        self.display_surface.blit(instruction, instruction_rect)

    def reset_game(self):
        self.next_shapes = [choice(list(TETROMINOS.keys())) for _ in range(3)]
        self.game = Game(self.get_next_shape, self.update_score, self.set_game_over)
        self.score = Score(graphics_dir=self.graphics_dir)
        if self.music:
            self.music.play(-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.states["start"]:
                            self.states["start"] = False
                            self.states["playing"] = True
                            if self.music:
                                self.music.play(-1)
                        elif self.states["game_over"]:
                            self.states["game_over"] = False
                            self.states["playing"] = True
                            self.reset_game()

            # Draw appropriate screen based on game state
            if self.states["start"]:
                self.draw_start_screen()
            elif self.states["playing"]:
                self.display_surface.fill(GRAY)
                self.game.run()
                self.score.run()
                self.preview.run(self.next_shapes)
            elif self.states["game_over"]:
                self.draw_game_over_screen()

            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    main = Main()
    main.run()
