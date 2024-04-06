import pygame
from othello import consts
from othello import board_encoding_helper as helper

class Board:
  # inits the board with no cells occupied
  def __init__(self) -> None:
    # black_cells represent the cells that the black player has occupied. Same for white_cells
    # we will store the cells as a bitmask.
    self.black_cells = self.white_cells = 0
    for i, j in consts.STARTING_BLACK_CELLS:
      self.black_cells |= helper.encode_cell(i, j)
    for i, j in consts.STARTING_WHITE_CELLS:
      self.white_cells |= helper.encode_cell(i, j)

  # draws the board on the window
  def draw_board(self, window, player) -> None:
    window.fill(consts.BACKGROUND)
    # draw a ROW x COLUMN grid
    for i in range(consts.ROWS):
      for j in range(consts.COLUMNS):
        # draw a square at (i, j)
        self.draw_cell(window, i, j, consts.BROWN)
    # draw the occupied cells
    for i in range(consts.ROWS):
      for j in range(consts.COLUMNS):
        # check if the cell is occupied by either player
        if (self.black_cells & helper.encode_cell(i, j)) > 0:
          self.draw_piece(window, i, j, consts.BLACK)
        elif (self.white_cells & helper.encode_cell(i, j)) > 0:
          self.draw_piece(window, i, j, consts.WHITE)
    # highlight the legal moves
    self.highlight_legal_moves(window, player)
  
  # draw a cell at (i, j)
  def draw_cell(self, window, i, j, color) -> None:
    # calculate the top left corner of the cell
    x = consts.INIT_SQUARE_SIZE * j + consts.OFFSET // 2 + consts.DELTA // 2
    y = consts.INIT_SQUARE_SIZE * i + consts.OFFSET // 2 + consts.DELTA // 2
    # then draw the square
    window.fill(color, (x, y, consts.SQUARE_SIZE, consts.SQUARE_SIZE))

  # draw a piece at (i, j)
  def draw_piece(self, window, i, j, color, radius = consts.RADIUS) -> None:
    # calculate the center of the cell
    x = consts.INIT_SQUARE_SIZE * j + consts.INIT_SQUARE_SIZE // 2 + consts.OFFSET // 2
    y = consts.INIT_SQUARE_SIZE * i + consts.INIT_SQUARE_SIZE // 2 + consts.OFFSET // 2
    # draw the piece
    pygame.draw.circle(window, color, (x, y), radius)

  # calculates the legal moves for the player and highlights them
  def highlight_legal_moves(self, window, player) -> None:
    target = self.white_cells
    if player == consts.BLACK_PLAYER:
      target = self.black_cells
    possible_cells = helper.get_possible_moves(target, self.black_cells | self.white_cells)
    self.add_highlight(window, possible_cells)

  # highlights the cells in the bitmask
  def add_highlight(self, window, cells) -> None:
    for i in range(consts.ROWS):
      for j in range(consts.COLUMNS):
        # check if the cell is in the bitmask
        if cells & helper.encode_cell(i, j) > 0:
          self.draw_piece(window, i, j, consts.PINK, consts.HIGHLIGHT_RADIUS)