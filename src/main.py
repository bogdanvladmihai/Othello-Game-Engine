import pygame
from othello import consts
from othello.board import Board

# function to create the game window and run the game
def main():
  # initialize the game window
  window = pygame.display.set_mode((consts.WIDTH + consts.OFFSET, consts.HEIGHT + consts.OFFSET))
  pygame.display.set_caption("Othello")
  board = Board()
  running = True
  while running:
    # check for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        pass
    # update the new board
    board.draw_board(window, consts.WHITE_PLAYER)
    pygame.display.update()

  pygame.quit()

if __name__ == "__main__":
  main()