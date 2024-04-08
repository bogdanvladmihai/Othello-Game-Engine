import othello.consts as consts
import othello.board_encoding_helper as helper
from functools import cache
from othello.consts import E1, E2, E3, E4, M1, M2, M3, M4, L1, L2, L3, L4

class Engine:
  # function to init the engine with a side and a depth
  # note that black tries to maximize the score, while white tries to minimize it
  def __init__(self, side, depth, eval_function) -> None:
    self.side = side
    self.depth = depth
    self.eval_function = eval_function
  
  # function to just get any move
  def get_any_move(self, white_cells, black_cells) -> tuple:
    target = white_cells
    if self.side == consts.WHITE_PLAYER:
      target = black_cells
    possible_moves = helper.get_possible_moves(target, white_cells | black_cells)
    return helper.iterate_over_active_cell(possible_moves).__next__()

  # function to check if the game is in the early game
  def is_early_game(self, white_cells, black_cells) -> bool:
    return helper.popcount(white_cells | black_cells) < consts.EARLY_GAME_THRESHOLD

  # function to check if the game is in a late state
  def is_end_game(self, white_cells, black_cells) -> bool:
    return helper.popcount(white_cells | black_cells) > consts.LATE_GAME_THRESHOLD

  # function to calculate mobility of a given position
  def calculate_mobility(self, white_cells, black_cells) -> float:
    black_mobility = helper.popcount(helper.get_possible_moves(white_cells, white_cells | black_cells))
    white_mobility = helper.popcount(helper.get_possible_moves(black_cells, white_cells | black_cells))
    if black_mobility + white_mobility == 0:
      return 0
    return consts.STABILIZER * (black_mobility - white_mobility) / (black_mobility + white_mobility)

  # function to calculate potential mobility of a given position
  def calculate_potential_mobility(self, white_cells, black_cells) -> float:
    black_potential = helper.popcount(helper.get_neighbours(white_cells, white_cells | black_cells))
    white_potential = helper.popcount(helper.get_neighbours(black_cells, white_cells | black_cells))
    if black_potential + white_potential == 0:
      return 0
    return consts.STABILIZER * (black_potential - white_potential) / (black_potential + white_potential)

  # function to calculate the score based on the corners
  def calculate_corners(self, white_cells, black_cells) -> float:
    black_corners = helper.count_corners(black_cells)
    white_corners = helper.count_corners(white_cells)
    if black_corners + white_corners == 0:
      return 0
    return consts.STABILIZER * (black_corners - white_corners) / (black_corners + white_corners)

  # function to evaluate the board in the early game
  # the evaluation is mainly based on the number of pieces, using evaporation
  # more about the evaluation function can be found in evaluation.tex
  def eval_early_game(self, white_cells, black_cells) -> float:
    coin_parity = consts.STABILIZER * (helper.popcount(white_cells) - helper.popcount(black_cells)) / (helper.popcount(white_cells | black_cells))
    mobility = self.calculate_mobility(white_cells, black_cells)
    potential_mobility = self.calculate_potential_mobility(white_cells, black_cells)
    corners = self.calculate_corners(white_cells, black_cells)
    # coin_parity, mobility, potential_mobility, corners
    return E1 * coin_parity + E2 * mobility + E3 * potential_mobility + E4 * corners

  # function to evaluate the board in the mid game
  # the evaluation function is not based on evaporation anymore
  # more about the evaluation function can be found in evaluation.tex
  def eval_mid_game(self, white_cells, black_cells) -> int:
    coin_parity = consts.STABILIZER * (helper.popcount(black_cells) - helper.popcount(white_cells)) / (helper.popcount(white_cells | black_cells))
    mobility = self.calculate_mobility(white_cells, black_cells)
    potential_mobility = self.calculate_potential_mobility(white_cells, black_cells)
    corners = self.calculate_corners(white_cells, black_cells)
    # mobility, corners, potential_mobility, coin_parity
    return M1 * mobility + M2 * corners + M3 * potential_mobility + M4 * coin_parity

  # function to evaluate the board in the late game
  # the evaluation function is now more foccused on the number of pieces
  # more about the evaluation function can be found in evaluation.tex
  def eval_end_game(self, white_cells, black_cells) -> int:
    coin_parity = consts.STABILIZER * (helper.popcount(black_cells) - helper.popcount(white_cells)) / (helper.popcount(white_cells | black_cells))
    mobility = self.calculate_mobility(white_cells, black_cells)
    potential_mobility = self.calculate_potential_mobility(white_cells, black_cells)
    corners = self.calculate_corners(white_cells, black_cells)
    # corners, coin_parity, mobility, potential_mobility
    return L1 * corners + L2 * coin_parity + L3 * mobility + L4 * potential_mobility

  # function to evaluate the board using static evaluation
  # the evaluation function is based on the board weights
  def static_eval(self, white_cells, black_cells) -> float:
    if helper.is_over(white_cells, black_cells):
      # get the winner
      winner = helper.get_winner(white_cells, black_cells)
      if winner is None:
        return 0
      elif winner == consts.BLACK_PLAYER:
        return consts.INF + 1
      return -consts.INF - 1
    # get the score. black tries to maximize it, while white tries to minimize it
    score = 0
    for (i, j) in helper.iterate_over_active_cell(black_cells):
      score += consts.STATIC_WEIGHTS_BOARD[i][j]
    for (i, j) in helper.iterate_over_active_cell(white_cells):
      score -= consts.STATIC_WEIGHTS_BOARD[i][j]
    return score

  # function to evaluate the board based on the number of placed discs
  def eval_board_by_discs(self, white_cells, black_cells) -> float:
    if self.is_early_game(white_cells, black_cells):
      return self.eval_early_game(white_cells, black_cells)
    elif self.is_end_game(white_cells, black_cells):
      return self.eval_end_game(white_cells, black_cells)
    return self.eval_mid_game(white_cells, black_cells)

  # function to evaluate the board. determines the evaluation function to use based on the game state
  def eval_board(self, white_cells, black_cells) -> float:
    return self.static_eval(white_cells, black_cells)

  # helper function for the minimax algorithm
  # trying to maximize the score (knowing that the current player is black)
  @cache
  def minimax_maximize(self, white_cells, black_cells, depth, alpha, beta) -> tuple:
    best_score = -consts.INF
    best_move = (None, None)
    moves = helper.get_possible_moves(white_cells, white_cells | black_cells)
    if moves == 0:
      return self.minimax(white_cells, black_cells, depth - 1, alpha, beta, False)
    for (i, j) in helper.iterate_over_active_cell(moves):
      new_white_cells, new_black_cells = helper.apply_move(white_cells, black_cells, i, j, consts.BLACK_PLAYER)
      score, _ = self.minimax(new_white_cells, new_black_cells, depth - 1, alpha, beta, False)
      if score > best_score:
        best_score = score
        best_move = (i, j)
      alpha = max(alpha, best_score)
      if alpha >= beta:
        break
    return best_score, best_move
  
  # helper function for the minimax algorithm
  # trying to minimze the score (knowing that the current player is white)
  @cache
  def minimax_minimize(self, white_cells, black_cells, depth, alpha, beta) -> tuple:
    best_score = consts.INF
    best_move = (None, None)
    moves = helper.get_possible_moves(black_cells, white_cells | black_cells)
    if moves == 0:
      return self.minimax(white_cells, black_cells, depth - 1, alpha, beta, True)
    for (i, j) in helper.iterate_over_active_cell(moves):
      new_white_cells, new_black_cells = helper.apply_move(white_cells, black_cells, i, j, consts.WHITE_PLAYER)
      score, _ = self.minimax(new_white_cells, new_black_cells, depth - 1, alpha, beta, True)
      if score < best_score:
        best_score = score
        best_move = (i, j)
      beta = min(beta, best_score)
      if alpha >= beta:
        break
    return best_score, best_move

  # function to get the best move for the engine using minimax + alpha-beta pruning
  # return value: (score, (x, y)), where (x, y) is the move that gets the score
  @cache
  def minimax(self, white_cells, black_cells, depth, alpha, beta, maximizing_player) -> tuple:
    # check if we reached a leaf node
    if depth == 0 or helper.is_over(white_cells, black_cells):
      if self.eval_function == consts.MOBILITY_BASED:
        return self.eval_board_by_discs(white_cells, black_cells), (None, None)
      return self.eval_board(white_cells, black_cells), (None, None)
    if maximizing_player:
      return self.minimax_maximize(white_cells, black_cells, depth, alpha, beta)
    else:
      return self.minimax_minimize(white_cells, black_cells, depth, alpha, beta) 
      
  # function to get the best move for the engine
  def get_move(self, white_cells, black_cells) -> tuple:
    _, (x, y) = self.minimax(white_cells, black_cells, self.depth, -consts.INF - 1, consts.INF + 1, self.side)
    return x, y