import pygame
from othello import consts

class Menu:
  # inits the menu with a window
  def __init__(self, window) -> None:
    self.window = window

  # gets the side to play
  def get_side(self) -> bool:
    self.window.fill(consts.BACKGROUND)
    # draw 2 buttons, one for white and one for black
    font = pygame.font.Font(None, consts.BUTTON_FONT_SIZE)
    info_font = pygame.font.Font(None, consts.FONT_SIZE)
    choose_text = info_font.render("Choose your side", True, consts.BROWN)
    choose_rect = choose_text.get_rect(center = (consts.WIDTH // 2, consts.HEIGHT // 4))
    self.window.blit(choose_text, choose_rect)
    white_rect = self.plot_button(font, "White", consts.WHITE, (consts.WIDTH // 2, consts.HEIGHT // 2))
    black_rect = self.plot_button(font, "Black", consts.BLACK, (consts.WIDTH // 2, consts.HEIGHT // 2 + consts.FONT_SIZE))
    pygame.display.update()
    # wait for the user to click on a button
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()
          if white_rect.collidepoint(pos):
            return consts.WHITE_PLAYER
          elif black_rect.collidepoint(pos):
            return consts.BLACK_PLAYER

  # gets the dificulty of the game
  def dificulty(self, color) -> int:
    self.window.fill(consts.BACKGROUND)
    # draw 3 buttons, one for each dificulty
    font = pygame.font.Font(None, consts.BUTTON_FONT_SIZE)
    info_font = pygame.font.Font(None, consts.FONT_SIZE)
    easy_rect = self.plot_button(font, "Easy", color, (consts.WIDTH // 2, consts.HEIGHT // 2))
    medium_rect = self.plot_button(font, "Medium", color, (consts.WIDTH // 2, consts.HEIGHT // 2 + consts.FONT_SIZE))
    hard_rect = self.plot_button(font, "Hard", color, (consts.WIDTH // 2, consts.HEIGHT // 2 + 2 * consts.FONT_SIZE))
    choose_text = info_font.render("Choose the dificulty", True, consts.BROWN)
    choose_rect = choose_text.get_rect(center = (consts.WIDTH // 2, consts.HEIGHT // 2 - consts.FONT_SIZE))
    self.window.blit(choose_text, choose_rect)
    pygame.display.update()
    # wait for the user to click on a button
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()
          if easy_rect.collidepoint(pos):
            return consts.DIFICULTY_EASY
          elif medium_rect.collidepoint(pos):
            return consts.DIFICULTY_MEDIUM
          elif hard_rect.collidepoint(pos):
            return consts.DIFICULTY_HARD
          
  # plots a button with the given text, color and position
  def plot_button(self, font, text, color, pos) -> pygame.Rect:
    button = font.render(text, True, color)
    rect = button.get_rect(center = pos)
    self.window.blit(button, rect)
    return rect

  # gets the game settings from the user
  def get_game_settings(self) -> tuple:
    side = self.get_side()
    color = consts.WHITE if side == consts.WHITE_PLAYER else consts.BLACK
    dificulty = self.dificulty(color)
    if dificulty == consts.DIFICULTY_EASY:
      depth = consts.EASY_DEPTH
    elif dificulty == consts.DIFICULTY_MEDIUM:
      depth = consts.MEDIUM_DEPTH
    else:
      depth = consts.HARD_DEPTH
    return side, depth