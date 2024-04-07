import pygame
import othello.consts as consts
from othello.game import Game
import othello.board_encoding_helper as helper

class Engine:
  # function to init the engine with a side and a depth
  def __init__(self, side, depth) -> None:
    self.side = side
    self.depth = depth

  # function to get the best move for the engine
  def get_move(self, white_cells, black_cells) -> tuple:
    # TODO
    target = white_cells
    if self.side == consts.WHITE_PLAYER:
      target = black_cells
    possible_moves = helper.get_possible_moves(target, white_cells | black_cells)

    def any(possible_moves):
      for i in range(consts.ROWS):
        for j in range(consts.COLUMNS):
          if (1 << (i * consts.COLUMNS + j)) & possible_moves > 0:
            return (i, j)
      return None, None

    return any(possible_moves)