import pygame, time
import sys
import math
# BOARD AND SQUARE SIZES
BOARD_WIDTH = 540
BOARD_HEIGHT = 600
SQUARE_SIZE = 60

# Initialize PyGame essential components
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("comicsans", 55)

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
GRAY = (129, 129, 129)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SOLVER_SPEED = 100


# Convert mouse position coordinates(x, y) to square coordinates(line, column)
def convert_coordinates(x, y):
    if x % 60 == 0:
        if y % 60 == 0:
            x_converted = int(x / 60)
            y_converted = int(y / 60)
            return x_converted, y_converted
        else:
            x_converted = int(x / 60)
            y_converted = math.floor(y / 60)
            return x_converted, y_converted
    else:
        if y % 60 == 0:
            x_converted = math.floor(x / 60)
            y_converted = int(y / 60)
            return x_converted, y_converted
        else:
            x_converted = math.floor(x / 60)
            y_converted = math.floor(y / 60)
            return x_converted, y_converted


class Sudoku:

    def __init__(self, window, values):
        self.board = window
        self.grid_values = values
        self.selected_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.rect_x = 0
        self.rect_y = 0

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
        self.draw_grid_values()

    # draw a number in the board
    def draw_number(self, n, x, y, color):
        if 0 <= x <= 8 and 0 <= y <= 8:
            if n == '0':
                number = font.render(n, True, WHITE, WHITE)
                rect = number.get_rect()
                rect.center = (30 + 60 * x, 30 + 60 * y)
                self.board.blit(number, rect)
            else:
                number = font.render(n, True, color)
                rect = number.get_rect()
                rect.center = (30 + 60 * x, 30 + 60 * y)
                self.board.blit(number, rect)

    def draw_grid_values(self):
        for x in range(0, 9):
            for y in range(0, 9):
                if self.grid_values[y][x].value != 0:
                    self.draw_number(str(self.grid_values[y][x].value), x, y, BLACK)

    def update_grid(self, number, x, y):
        sqr = self.grid_values[y][x]
        sqr.update_number(number)

    def draw_selected_square(self, x, y):
        if 0 <= x <= 8 and 0 <= y <= 8:
            new_select_rect = pygame.rect.Rect(60 * x, 60 * y, 60, 60)
            # draw selected square
            pygame.draw.rect(self.board, (255, 0, 0), rect=new_select_rect, width=3)
            self.selected_rect = new_select_rect
            self.rect_x = x
            self.rect_y = y

    # Draw number in the current selected square
    def sketch_number(self, number):
        if self.grid_values[self.rect_y][self.rect_x] != number and 0 <= self.rect_x <= 8 and 0 <= self.rect_y <= 8:
            self.update_grid(number, self.rect_x, self.rect_y)
            self.draw_number(str(number), self.rect_x, self.rect_y, BLACK)

    # Redraw the sudoku board with user's new values
    def redraw_board(self):
        self.draw_Board()
        # draw selected rectangle
        pygame.draw.rect(self.board, (255, 0, 0), self.selected_rect, width=3)

    def has_empty(self):
        for y in range(0, 9):
            for x in range(0, 9):
                if self.grid_values[y][x].is_empty():
                    return [x, y]
        return None

    # Check if number is valid
    def is_valid(self, number, x, y):
        # check row
        for y1 in range(0, 9):
            if self.grid_values[y1][x].value == number:
                return False

        # check line
        for x1 in range(0, 9):
            if self.grid_values[y][x1].value == number:
                return False

        # check major square
        major_square_x = math.floor(x / 3)
        major_square_y = math.floor(y / 3)
        for x1 in range(major_square_x * 3, major_square_x * 3 + 3):
            for y1 in range(major_square_y * 3, major_square_y * 3 + 3):
                if self.grid_values[y1][x1].value == number:
                    return False
        # Valid move
        return True

    # Sudoku Solver with backtracking algorithm
    def auto_solve(self):
        pos = self.has_empty()
        if pos is None:

            # Make all squares non modifiable
            for x in range(0, 9):
                for y in range(0, 9):
                    self.grid_values[y][x].update_modifiable(False)

            return True
        else:
            x = pos[0]
            y = pos[1]

        for number in range(1, 10):
            if self.is_valid(number, x, y):
                self.update_grid(number, x, y)
                self.draw_number(str(number), x, y, BLACK)
                pygame.draw.rect(self.board, GREEN, pygame.rect.Rect(60 * x, 60 * y, 60, 60), width=5)
                pygame.display.update()
                pygame.event.pump()
                pygame.time.delay(SOLVER_SPEED)

                if self.auto_solve():
                    return True

                pygame.draw.rect(self.board, RED, pygame.rect.Rect(60 * x, 60 * y, 60, 60), width=5)
                self.update_grid(0, x, y)

                self.draw_number('0', x, y, WHITE)
                pygame.display.update()
                pygame.event.pump()
                pygame.time.delay(SOLVER_SPEED)

        return False

