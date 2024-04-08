# window dimensions
WIDTH = 400
HEIGHT = 400
OFFSET = 20

# board dimensions
ROWS = COLUMNS = 8

# square and piece dimensions
DELTA = 4
INIT_SQUARE_SIZE = WIDTH // COLUMNS
SQUARE_SIZE = INIT_SQUARE_SIZE - DELTA
RADIUS = SQUARE_SIZE / 3
HIGHLIGHT_RADIUS = RADIUS // 2

# starting white and black cells
STARTING_WHITE_CELLS = [(3, 3), (4, 4)]
STARTING_BLACK_CELLS = [(3, 4), (4, 3)]

# colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (206, 134, 57)
BROWN = (140, 69, 16)
PINK = (255, 102, 255, 100)

# player encoding
WHITE_PLAYER = False
BLACK_PLAYER = True

# directions
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
CAPTURE_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# powers of two + masks
POWS = [[1 << (i * COLUMNS + j) for j in range(COLUMNS)] for i in range(ROWS)]
POWS_LOOKUP = {(1 << (i * COLUMNS + j)): (i, j) for i in range(ROWS) for j in range(COLUMNS)}
CORNERS_MASK = POWS[0][0] | POWS[0][COLUMNS - 1] | POWS[ROWS - 1][0] | POWS[ROWS - 1][COLUMNS - 1]

# font size + gameplay
FONT_SIZE = 50
FONT_TIME = 30
BUTTON_FONT_SIZE = 36
WAIT_TO_SEE_THE_MOVE = 500
WAIT_GAME_OVER = 2000

# game dificulty
DIFICULTY_EASY = 0
DIFICULTY_MEDIUM = 1
DIFICULTY_HARD = 2
EASY_DEPTH = 3
MEDIUM_DEPTH = 4
HARD_DEPTH = 6

# evaluation consts
INF = POWS[ROWS - 1][COLUMNS - 1] * 2
EARLY_GAME_THRESHOLD = 14
LATE_GAME_THRESHOLD = 50
STATIC_WEIGHTS_BOARD = [
  [99, -8, 8, 6, 6, 8, -8, 99],
  [-8, -24, -4, -3, -3, -4, -24, -8],
  [8, -4, 7, 4, 4, 7, -4, 8],
  [6, -3, 4, 0, 0, 4, -3, 6],
  [6, -3, 4, 0, 0, 4, -3, 6],
  [8, -4, 7, 4, 4, 7, -4, 8],
  [-8, -24, -4, -3, -3, -4, -24, -8],
  [99, -8, 8, 6, 6, 8, -8, 99]
]
STABILIZER = 100

# constants for the evaluation function - early game
E1 = 1.3
E2 = 1
E3 = 0.5
E4 = 0.5
# constants for the evaluation function - mid game
M1 = 1.8
M2 = 1.7
M3 = 1.2
M4 = 1
# constants for the evaluation function - late game
L1 = 2.1
L2 = 1.5
L3 = 1.2
L4 = 1

# eval function types
WEIGHTED_BOARD = False
MOBILITY_BASED = True