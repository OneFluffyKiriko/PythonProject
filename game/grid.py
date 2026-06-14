import pygame

from utils.settings import (
    GRID_COLOR,
    GRID_SIZE,
    PATH_COLOR,
    PATH_OUTLINE_COLOR
)

class Grid:
    

    def __init__(self, width, height, path_tiles=None, grid_size=GRID_SIZE):

        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.cols = (width + self.grid_size - 1) // self.grid_size
        self.rows = (height + self.grid_size - 1) // self.grid_size
        self.occupied = set()
        self.path = []
        self.path_tiles = set()
        self.set_path(path_tiles or [])

    def set_path(self, path_tiles):

        self.path = list(path_tiles)
        self.path_tiles = set(path_tiles)

    def get_path_points(self):

        tile_centers = [
            self.grid_to_world(gx, gy, clamp=True)
            for gx, gy in self.path
        ]

        if not tile_centers:
            return []

        start_point = (0, tile_centers[0][1])
        end_point = (self.width, tile_centers[-1][1])

        return [
            start_point,
            *tile_centers,
            end_point
        ]

    def world_to_grid(self, pos):

        x, y = pos

        return (
            x // self.grid_size,
            y // self.grid_size
        )

    def grid_to_world(self, gx, gy, clamp=False):

        x = gx * self.grid_size + self.grid_size // 2
        y = gy * self.grid_size + self.grid_size // 2

        if clamp:
            x = max(0, min(self.width, x))
            y = max(0, min(self.height, y))

        return (
            x,
            y
        )

    def can_place(self, gx, gy):

        return (
            (gx, gy) not in self.occupied
            and
            (gx, gy) not in self.path_tiles
        )

    def place(self, gx, gy):

        self.occupied.add((gx, gy))

    def draw(self, screen, width, height):

        path_points = self.get_path_points()

        if len(path_points) >= 2:
            pygame.draw.lines(
                screen,
                PATH_OUTLINE_COLOR,
                False,
                path_points,
                self.grid_size + 6
            )

            pygame.draw.lines(
                screen,
                PATH_COLOR,
                False,
                path_points,
                self.grid_size
            )
        elif len(path_points) == 1:
            pygame.draw.circle(
                screen,
                PATH_OUTLINE_COLOR,
                path_points[0],
                self.grid_size // 2 + 3
            )
            pygame.draw.circle(
                screen,
                PATH_COLOR,
                path_points[0],
                self.grid_size // 2
            )

        for x in range(0, width, self.grid_size):
            pygame.draw.line(
                screen,
                GRID_COLOR,
                (x, 0),
                (x, height)
            )

        for y in range(0, height, self.grid_size):
            pygame.draw.line(
                screen,
                GRID_COLOR,
                (0, y),
                (width, y)
            )
