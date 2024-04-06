import pygame
import numpy as np
from othello import consts

class Board:
  # inits the board with no cells occupied
  def __init__(self) -> None:
    # black_cells represent the cells that the black player has occupied. Same for white_cells
    # we will store the cells as a bitmask.
    self.black_cells = 1
    self.white_cells = 354444

  # draws the board on the window
  def draw_board(self, window) -> None:
    # draw a ROW x COLUMN grid
    for i in range(consts.ROWS):
      for j in range(consts.COLUMNS):
        # draw a square at (i, j)
        self.draw_cell(window, i, j, consts.BROWN)
    # draw the occupied cells
    for i in range(consts.ROWS):
      for j in range(consts.COLUMNS):
        # check if the cell is occupied by either player
        if (self.black_cells & (1 << (i * consts.COLUMNS + j))) > 0:
          self.draw_piece(window, i, j, consts.BLACK)
        elif (self.white_cells & (1 << (i * consts.COLUMNS + j))) > 0:
          self.draw_piece(window, i, j, consts.WHITE)
  
  # draw a cell at (i, j)
  def draw_cell(self, window, i, j, color) -> None:
    # calculate the top left corner of the cell
    x = consts.INIT_SQUARE_SIZE * j
    y = consts.INIT_SQUARE_SIZE * i
    # always set the background color first
    window.fill(consts.BACKGROUND, (x, y, consts.INIT_SQUARE_SIZE, consts.INIT_SQUARE_SIZE))
    # then draw the square
    x += consts.DELTA // 2
    y += consts.DELTA // 2
    window.fill(color, (x, y, consts.SQUARE_SIZE, consts.SQUARE_SIZE))

  # draw a piece at (i, j)
  def draw_piece(self, window, i, j, color) -> None:
    # calculate the center of the cell
    x = consts.INIT_SQUARE_SIZE * j + consts.INIT_SQUARE_SIZE // 2
    y = consts.INIT_SQUARE_SIZE * i + consts.INIT_SQUARE_SIZE // 2
    # draw the piece
    pygame.draw.circle(window, color, (x, y), consts.RADIUS)
