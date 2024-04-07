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

# get the possible moves for the player
def get_possible_moves(target, occupied) -> int:
  possible_cells = 0
  for i in range(consts.ROWS):
    for j in range(consts.COLUMNS):
      # check if the cell is occupied by the current player
      if (encode_cell(i, j) & target) > 0:
        # add the neighbors of the cell
        for dx, dy in consts.DIRECTIONS:
          x, y = i + dx, j + dy
          if is_inside(x, y) and (encode_cell(x, y) & occupied) == 0:
            possible_cells |= encode_cell(x, y)
  return possible_cells

# iterate over the active cells of the mask
def iterate_over_active_cell(mask) -> tuple:
  pass

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
  