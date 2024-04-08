from othello import consts

# function to return a bitmask only containing cell (i, j)
def encode_cell(x, y) -> int:
  return consts.POWS[x][y]

# checks if the cell (i, j) is empty
def is_empty(board, i, j) -> bool:
  return encode_cell(i, j) & board == 0

# check if (i, j) is inside the board
def is_inside(i, j) -> bool:
  return i >= 0 and j >= 0 and i < consts.ROWS and j < consts.COLUMNS

# gets oposide direction of (dx, dy)
def get_oposide_direction(dx, dy) -> tuple:
  return -dx, -dy

# returns the number of set bits in the mask
def popcount(mask) -> int:
  return mask.bit_count()

# get the winner of the game
# returns None in case of a draw
def get_winner(white_cells, black_cells) -> bool:
  if popcount(white_cells) > popcount(black_cells):
    return consts.WHITE_PLAYER
  elif popcount(white_cells) < popcount(black_cells):
    return consts.BLACK_PLAYER
  return None

# check if from cell (x, y) by going in direction (dx, dy) we can attack the opponent
def is_attacking(x, y, dx, dy, opponent, attacker) -> bool:
  while is_inside(x, y) and (opponent & encode_cell(x, y)) > 0:
    x, y = x + dx, y + dy
  return is_inside(x, y) and (attacker & encode_cell(x, y)) > 0

# get the possible moves for the player
def get_possible_moves(target, occupied) -> int:
  possible_cells = 0
  for (i, j) in iterate_over_active_cell(target):
    # add the neighbors of the cell
    for dx, dy in consts.DIRECTIONS:
      x, y = i + dx, j + dy
      oposite_dx, oposide_dy = get_oposide_direction(dx, dy)
      if is_inside(x, y) and (encode_cell(x, y) & occupied) == 0: 
        if is_attacking(i, j, oposite_dx, oposide_dy, target, occupied ^ target):
          possible_cells |= encode_cell(x, y)
  return possible_cells

# function to calculate the neighbors of the player
def get_neighbours(opponent, board) -> int:
  answer = 0
  for (i, j) in iterate_over_active_cell(opponent):
    for dx, dy in consts.DIRECTIONS:
      x, y = i + dx, j + dy
      if is_inside(x, y) and (encode_cell(x, y) & board) == 0:
        answer |= encode_cell(x, y)
  return answer

# function to count the number of occupied corners
def count_corners(mask) -> int:
  return popcount(mask & consts.CORNERS_MASK)

# check if the game is over
def is_over(white_cells, black_cells) -> bool:
  if white_cells == 0 or black_cells == 0:
    return True
  board = white_cells | black_cells
  answer = board == 2 * consts.POWS[consts.ROWS - 1][consts.COLUMNS - 1] - 1
  # check if neither player can make a move
  moves_white = get_possible_moves(white_cells, white_cells | black_cells)
  moves_black = get_possible_moves(black_cells, white_cells | black_cells)
  return answer or (moves_white == 0 and moves_black == 0)

# decode a bitmask and return the cell (i, j)
def decode(cell) -> tuple:
  return consts.POWS_LOOKUP[cell]

# iterate over the active cells of the mask
def iterate_over_active_cell(mask) -> tuple:
  # should get the lsb and decode it
  while mask > 0:
    cell = mask & -mask
    yield decode(cell)
    mask &= mask - 1
  return (None, None)

# adjust the board after the move (i, j) was made by player
def adjust_cells(white_cells, black_cells, i, j, player) -> tuple:
  # assume the move is made by white
  attacker, opponent = white_cells, black_cells
  swapped = False
  if player == consts.BLACK_PLAYER:
    attacker, opponent = opponent, attacker
    swapped = True
  
  to_change = 0
  # given that the move was made at (i, j), we know we should only check the neighbors
  for (dx, dy) in consts.CAPTURE_DIRECTIONS:
    x, y = i + dx, j + dy
    if not is_inside(x, y) or (opponent & encode_cell(x, y)) == 0:
      continue
    # (x, y) is the opponent's cell, we should extend to find the other end of the path
    path_code = encode_cell(x, y)
    x_end, y_end = x + dx, y + dy
    while is_inside(x_end, y_end) and (opponent & encode_cell(x_end, y_end)) > 0:
      path_code |= encode_cell(x_end, y_end)
      x_end, y_end = x_end + dx, y_end + dy
    if not is_inside(x_end, y_end) or (attacker & encode_cell(x_end, y_end)) == 0:
      continue
    # now we know we found a valid path
    to_change |= path_code

  # at the end, just update the bitmasks
  new_white_cells = white_cells ^ to_change | encode_cell(i, j)
  new_black_cells = black_cells ^ to_change
  if swapped:
    new_white_cells = white_cells ^ to_change
    new_black_cells = black_cells ^ to_change | encode_cell(i, j)
  return new_white_cells, new_black_cells

# applies the move (i, j) made by player to the board
def apply_move(white_cells, black_cells, i, j, player) -> tuple:
  position = encode_cell(i, j)
  if player == consts.WHITE_PLAYER:
    white_cells |= position
  else:
    black_cells |= position
  return adjust_cells(white_cells, black_cells, i, j, player)
  