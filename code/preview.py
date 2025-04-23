from settings import *
from pygame.image import load
from os import path
import pygame


class Preview:
    def __init__(self, graphics_dir):
        # General display setup
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION)
        )
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - PADDING, PADDING))

        # Preload shape images using the provided graphics_dir
        self.shape_surfaces = {}
        for shape in TETROMINOS.keys():
            image_path = path.join(graphics_dir, f"{shape}.png")
            if not path.exists(image_path):
                raise FileNotFoundError(
                    f"Missing image for shape '{shape}': {image_path}"
                )
            self.shape_surfaces[shape] = load(image_path).convert_alpha()

        # Vertical space per piece
        self.increment_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces.get(shape)
            if shape_surface:
                x = self.surface.get_width() / 2
                y = self.increment_height / 2 + i * self.increment_height
                rect = shape_surface.get_rect(center=(x, y))
                self.surface.blit(shape_surface, rect)

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
