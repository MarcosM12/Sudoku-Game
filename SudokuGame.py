import pygame, time
import sys
import math
import Square as sq

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

# Initial values to display in the board
grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# BOARD AND SQUARE SIZES
BOARD_SIZE = (540, 600)
BOARD_WIDTH = 540
BOARD_HEIGHT = 600
SQUARE_SIZE = 60

# FPS
FPS = pygame.time.Clock()
FPS_value = 60


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


def initialize_grid(grid_values):
    new_grid = grid_values
    for square_x in range(0, 9):  # 0, 1, 2, 3, ...,8
        for square_y in range(0, 9):
            if grid_values[square_y][square_x] != 0:
                new_grid[square_y][square_x] = sq.Square(square_x, square_y, grid[square_y][square_x], False)
            else:
                new_grid[square_y][square_x] = sq.Square(square_x, square_y, 0, True)

    return new_grid


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

    def draw_number(self, n, x, y, color):
        if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT - 60:
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
        if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT - 60:
            new_select_rect = pygame.rect.Rect(60 * x, 60 * y, 60, 60)
            # draw selected square
            pygame.draw.rect(self.board, (255, 0, 0), rect=new_select_rect, width=3)
            self.selected_rect = new_select_rect
            self.rect_x = x
            self.rect_y = y

    # draw a number in the board
    def sketch_number(self, number):
        if self.grid_values[self.rect_y][self.rect_x] != number:
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

    def auto_solve(self):
        self.draw_Board()
        Pos = self.has_empty()
        if Pos is None:
            return True
        else:
            x = Pos[0]
            y = Pos[1]

        for number in range(1, 10):
            if self.is_valid(number, x, y):
                self.update_grid(number, x, y)
                self.draw_number(str(number), x, y, BLACK)
                pygame.draw.rect(self.board, GREEN, pygame.rect.Rect(60 * x, 60 * y, 60, 60), width=5)
                pygame.display.flip()
                pygame.event.pump()
                pygame.time.delay(300)

                if self.auto_solve():
                    return True

                pygame.draw.rect(self.board, RED, pygame.rect.Rect(60 * x, 60 * y, 60, 60), width=5)
                self.update_grid(0, x, y)
                self.draw_number('0', x, y, BLACK)
                pygame.display.flip()
                pygame.event.pump()
                pygame.time.delay(300)

        return False


if __name__ == "__main__":
    board = pygame.display.set_mode(BOARD_SIZE)
    pygame.display.set_caption('Sudoku Solver')  # Window Title
    new_grid = initialize_grid(grid)
    sudoku = Sudoku(board, new_grid)
    sudoku.draw_Board()

    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # Press mouse button to put a number in a square
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse cursor position
                (x, y) = pygame.mouse.get_pos()
                # Convert X and Y coordinates to square position (line, column)
                new_x, new_y = convert_coordinates(x, y)
                sudoku.draw_selected_square(new_x, new_y)

            # Exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sudoku.sketch_number(1)
                if event.key == pygame.K_2:
                    sudoku.sketch_number(2)
                if event.key == pygame.K_3:
                    sudoku.sketch_number(3)
                if event.key == pygame.K_4:
                    sudoku.sketch_number(4)
                if event.key == pygame.K_5:
                    sudoku.sketch_number(5)
                if event.key == pygame.K_6:
                    sudoku.sketch_number(6)
                if event.key == pygame.K_7:
                    sudoku.sketch_number(7)
                if event.key == pygame.K_8:
                    sudoku.sketch_number(8)
                if event.key == pygame.K_9:
                    sudoku.sketch_number(9)
                if event.key == pygame.K_KP1:
                    sudoku.sketch_number(1)
                if event.key == pygame.K_KP2:
                    sudoku.sketch_number(2)
                if event.key == pygame.K_KP3:
                    sudoku.sketch_number(3)
                if event.key == pygame.K_KP4:
                    sudoku.sketch_number(4)
                if event.key == pygame.K_KP5:
                    sudoku.sketch_number(5)
                if event.key == pygame.K_KP6:
                    sudoku.sketch_number(6)
                if event.key == pygame.K_KP7:
                    sudoku.sketch_number(7)
                if event.key == pygame.K_KP8:
                    sudoku.sketch_number(8)
                if event.key == pygame.K_KP9:
                    sudoku.sketch_number(9)

                if event.key == pygame.K_SPACE:
                    sudoku.auto_solve()
                    print("done")

        sudoku.redraw_board()  # redraw board and grid values
        FPS.tick(FPS_value)
        pygame.display.update()  # Refresh display content
