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
WHITE_PLAYER = True
BLACK_PLAYER = False

# directions
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
CAPTURE_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# powers of two
POWS = [[1 << (i * COLUMNS + j) for j in range(COLUMNS)] for i in range(ROWS)]

# font size
FONT_SIZE = 50
BUTTON_FONT_SIZE = 36

# game dificulty
DIFICULTY_EASY = 0
DIFICULTY_MEDIUM = 1
DIFICULTY_HARD = 2
EASY_DEPTH = 3
MEDIUM_DEPTH = 4
HARD_DEPTH = 5 # hope this is not too optimistic
