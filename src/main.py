import pygame
from othello import consts
from othello.board import Board
from othello import board_encoding_helper as helper

# function to calulcate the cell from the mouse position
def calculate_cell(pos) -> tuple:
  x, y = pos
  x -= consts.OFFSET // 2
  y -= consts.OFFSET // 2
  return y // consts.INIT_SQUARE_SIZE, x // consts.INIT_SQUARE_SIZE

# check if the move is valid
def can_move(board, x, y, turn) -> bool:
  target = board.white_cells
  if turn == consts.BLACK_PLAYER:
    target = board.black_cells
  # check if the cell is empty
  if not helper.is_empty(board.black_cells | board.white_cells, x, y):
    return False
  # if it is, we should find if it has at least one neighbor that belongs to the current player
  has_at_least_one_neighbor = False
  for (dx, dy) in consts.DIRECTIONS:
    x_new, y_new = x + dx, y + dy
    if helper.is_inside(x_new, y_new) and (helper.encode_cell(x_new, y_new) & target) > 0:
      has_at_least_one_neighbor = True
      break
  return has_at_least_one_neighbor

# check if the player can not make a move
def can_not_make_a_move(board, turn) -> bool:
  cells = board.white_cells
  if turn == consts.BLACK_PLAYER:
    cells = board.black_cells
  return helper.get_possible_moves(cells, board.black_cells | board.white_cells) == 0

# function to create the game window and run the game
def main():
  # initialize the game window
  window = pygame.display.set_mode((consts.WIDTH + consts.OFFSET, consts.HEIGHT + consts.OFFSET))
  pygame.display.set_caption("Othello")
  board = Board()
  turn = consts.WHITE_PLAYER
  running = True
  while running:
    # check if the game is over
    if board.white_cells | board.black_cells == (1 << consts.ROWS * consts.COLUMNS) - 1:
      # count the number of pieces for each player
      white_cells = bin(board.white_cells).count("1")
      black_cells = bin(board.black_cells).count("1")
      # I should print the winner in a new pygame window
      # TODO: print the winner
      break

    # check if the player can move
    if can_not_make_a_move(board, turn):
      turn = not turn
      continue

    # check for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # get the cell from the mouse position and check if it is a valid move
        pos = pygame.mouse.get_pos()
        (x, y) = calculate_cell(pos)
        if can_move(board, x, y, turn):
          board.make_move(x, y, turn)
          turn = not turn
          break
    # update the new board
    board.draw_board(window, turn)
    pygame.display.update()

  pygame.quit()

if __name__ == "__main__":
  main()