import pygame
from othello import consts
from othello.game import Game
import engine
import menu

# function to calulcate the cell from the mouse position
def calculate_cell(pos) -> tuple:
  x, y = pos
  x -= consts.OFFSET // 2
  y -= consts.OFFSET // 2
  return y // consts.INIT_SQUARE_SIZE, x // consts.INIT_SQUARE_SIZE

# function to print the winner and end the game
def end_game(white_cells, black_cells, window):
  window.fill(consts.BACKGROUND)
  font = pygame.font.Font(None, consts.FONT_SIZE)
  winner_color = consts.PINK
  if white_cells > black_cells:
    text = font.render("White wins!", True, consts.WHITE)
    winner_color = consts.WHITE
  elif black_cells > white_cells:
    text = font.render("Black wins!", True, consts.BLACK)
    winner_color = consts.BLACK
    white_cells, black_cells = black_cells, white_cells
  else:
    text = font.render("It's a tie!", True, consts.PINK)
  # just print the winner and the score at the end
  text_rect = text.get_rect(center = (consts.WIDTH // 2, consts.HEIGHT // 2))
  final_score = font.render(f"{white_cells} - {black_cells}", True, winner_color)
  final_score_rect = final_score.get_rect(center = (consts.WIDTH // 2, consts.HEIGHT // 2 + consts.FONT_SIZE))
  window.blit(final_score, final_score_rect)
  window.blit(text, text_rect)
  pygame.display.update()
  # wait for the user to close the window
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

# function to run the game
def run_game(window, game_engine, engine_player) -> None:
  game = Game(window)
  running = True
  while running:
    # check if the game is over
    if game.is_over():
      (white_cells, black_cells) = game.get_score()
      end_game(white_cells, black_cells, window)
      break
    # check if it is the engine's turn
    if game.turn == engine_player:
      (x, y) = game_engine.get_move(game.board.white_cells, game.board.black_cells)
      game.apply_move(x, y)
      continue
    # check for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # get the cell from the mouse position and check if it is a valid move
        pos = pygame.mouse.get_pos()
        (x, y) = calculate_cell(pos)
        if game.can_move(x, y):
          game.apply_move(x, y)
          break
    # update the new board
    game.update_board(window)

# function to create the window and run the menu+game
def main():
  pygame.init()
  # initialize the game window
  window = pygame.display.set_mode((consts.WIDTH + consts.OFFSET, consts.HEIGHT + consts.OFFSET))
  pygame.display.set_caption("Othello")
  user_menu = menu.Menu(window)
  side, depth = user_menu.get_game_settings()
  game_engine = engine.Engine(not side, depth)
  run_game(window, game_engine, not side)
  pygame.quit()

if __name__ == "__main__":
  main()