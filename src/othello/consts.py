import pygame

# window dimensions
WIDTH = 400
HEIGHT = 400

# board dimensions
ROWS = COLUMNS = 8

# square and piece dimensions
DELTA = 4
INIT_SQUARE_SIZE = WIDTH // COLUMNS
SQUARE_SIZE = INIT_SQUARE_SIZE - DELTA
RADIUS = SQUARE_SIZE / 3

# colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (206, 134, 57)
BROWN = (140, 69, 16)
PINK = (255, 204, 255)