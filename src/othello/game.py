import pygame
from othello import consts
from othello.board import Board
from othello import board_encoding_helper as helper

class Game:
  # inits the game with a window and a board
  def __init__(self, window) -> None:
    self.window = window
    self.board = Board()
    self.turn = consts.BLACK_PLAYER

  # check if the game is over
  def is_over(self) -> bool:
    return helper.is_over(self.board.black_cells, self.board.white_cells)

  # check if the move is valid
  def can_move(self, x, y) -> bool:
    if not helper.is_inside(x, y):
      return False
    target = self.board.black_cells
    if self.turn == consts.BLACK_PLAYER:
      target = self.board.white_cells
    # check if the cell is empty
    if not helper.is_empty(self.board.black_cells | self.board.white_cells, x, y):
      return False
    # if it is, we should find if it has at least one neighbor that belongs to the other player
    return helper.encode_cell(x, y) & helper.get_possible_moves(target, self.board.black_cells | self.board.white_cells) > 0
  
  # check if the player can not make a move
  def can_not_make_a_move(self) -> bool:
    cells = self.board.black_cells
    if self.turn == consts.BLACK_PLAYER:
      cells = self.board.white_cells
    return helper.get_possible_moves(cells, self.board.black_cells | self.board.white_cells) == 0

  # apply the move to the board
  def apply_move(self, x, y) -> None:
    if x is not None and y is not None:
      self.board.white_cells, self.board.black_cells = helper.apply_move(self.board.white_cells, self.board.black_cells, x, y, self.turn)
    self.turn = not self.turn
    if self.can_not_make_a_move():
      self.turn = not self.turn

  # draws the board
  def update_board(self, window) -> None:
    self.board.draw_board(window, self.turn)
    pygame.display.update()

  # get the score of the game
  def get_score(self) -> tuple:
    white_cells = bin(self.board.white_cells).count('1')
    black_cells = bin(self.board.black_cells).count('1')
    return white_cells, black_cells