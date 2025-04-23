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
        base_dir = dirname(
            dirname(abspath(__file__))
        )  # Moves two levels up (from /code to project root)
        self.sound_dir = join(base_dir, "sound")
        self.graphics_dir = join(base_dir, "graphics")

        # Prepare shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for _ in range(3)]

        # Initialise components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score(graphics_dir=self.graphics_dir)
        self.preview = Preview(graphics_dir=self.graphics_dir)

        # Load music
        music_path = join(self.sound_dir, "music.wav")
        if not os.path.exists(music_path):
            raise FileNotFoundError(f"Missing sound file: {music_path}")
        self.music = pygame.mixer.Sound(music_path)
        self.music.set_volume(0.05)
        self.music.play(-1)

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draw components
            self.display_surface.fill(GRAY)
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    main = Main()
    main.run()
