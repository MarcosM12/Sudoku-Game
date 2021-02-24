import pygame
from pygame.locals import *
import sys
import math

pygame.init()  # Initialize PyGame video components
pygame.font.init()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
GRAY = (129, 129, 129)

font = pygame.font.SysFont("comicsans", 55)

# BOARD AND SQUARE SIZES
BOARD_SIZE = (540, 600)
BOARD_WIDTH = 540
SQUARE_SIZE = 60

# FPS
FPS = pygame.time.Clock()
FPS_value = 60


def convert_coordinates(x, y):
    if x % 60 == 0:
        if y % 60 == 0:
            x_converted = 60 * (x / 60)
            y_converted = 60 * (y / 60)
            return x_converted, y_converted
        else:
            x_converted = 60 * (x / 60)
            y_converted = 60 * math.floor(y / 60)
            return x_converted, y_converted
    else:
        if y % 60 == 0:
            x_converted = 60 * math.floor(x / 60)
            y_converted = 60 * (y / 60)
            return x_converted, y_converted
        else:
            x_converted = 60 * math.floor(x / 60)
            y_converted = 60 * math.floor(y / 60)
            return x_converted, y_converted


class Sudoku:

    def __init__(self, board):
        self.board = board

    def draw_Board(self):
        # Fill background
        self.board.fill((255, 255, 255))
        # minor lines
        for x in range(0, BOARD_WIDTH + SQUARE_SIZE, SQUARE_SIZE):
            pygame.draw.line(self.board, color=GRAY, start_pos=(x, 0), end_pos=(x, BOARD_WIDTH))

        for y in range(0, BOARD_WIDTH + SQUARE_SIZE, SQUARE_SIZE):
            pygame.draw.line(self.board, color=GRAY, start_pos=(0, y), end_pos=(BOARD_WIDTH, y))

        # major lines
        for x in range(0, BOARD_WIDTH + SQUARE_SIZE, SQUARE_SIZE):
            if x % 9 == 0 and (x != 0 and x != BOARD_WIDTH):
                pygame.draw.line(self.board, color=BLACK, start_pos=(x, 0), end_pos=(x, BOARD_WIDTH), width=2)
        for y in range(0, BOARD_WIDTH + SQUARE_SIZE, SQUARE_SIZE):
            if y % 9 == 0:
                pygame.draw.line(self.board, color=BLACK, start_pos=(0, y), end_pos=(BOARD_WIDTH, y), width=2)

    def draw_number(self, n, x, y):
        number = font.render(n, True, GRAY)
        rect = number.get_rect()
        new_x, new_y = convert_coordinates(x, y)
        rect.center = (30 + new_x, 30 + new_y)
        self.board.blit(number, rect)

    def draw_square(self, x, y):
        new_x, new_y = convert_coordinates(x, y)
        # draw selected square
        pygame.draw.rect(self.board, (255, 0, 0), rect=(new_x, new_y, 60, 60), width=3)

    def run(self):
        self.draw_Board()

        while True:

            # self.draw_number("2")
            # event handling, gets all event from the event queue
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.draw_Board()
                    (x, y) = pygame.mouse.get_pos()
                    self.draw_square(x, y)
                    (x, y) = pygame.mouse.get_pos()
                    self.draw_number("3", x, y)
                    print(x, y)
                # Exit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # Refresh display content
            FPS.tick(FPS_value)


if __name__ == "__main__":
    board = pygame.display.set_mode(BOARD_SIZE)
    pygame.display.set_caption('Sudoku Solver')  # Window Title
    sudoku = Sudoku(board)
    sudoku.run()
