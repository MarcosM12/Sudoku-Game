import pygame, time
import sys
import math
import Square as sq
import SudokuGame

# BOARD AND SQUARE SIZES
BOARD_SIZE = (540, 600)
BOARD_WIDTH = 540
BOARD_HEIGHT = 600
SQUARE_SIZE = 60

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


def main():
    FPS = pygame.time.Clock()
    FPS_value = 60
    board = pygame.display.set_mode(BOARD_SIZE)
    pygame.display.set_caption('Sudoku Solver')  # Window Title
    # Initialize values in the board
    new_grid = [[0 for j in range(0, 9)] for i in range(0, 9)]
    for square_x in range(0, 9):  # 0, 1, 2, 3, ...,8
        for square_y in range(0, 9):
            if grid[square_y][square_x] != 0:
                new_grid[square_y][square_x] = sq.Square(square_x, square_y, grid[square_y][square_x], False)
            else:
                new_grid[square_y][square_x] = sq.Square(square_x, square_y, 0, True)

    sudoku = SudokuGame.Sudoku(board, new_grid)
    sudoku.draw_Board()
    new_game = False
    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # Press mouse button to put a number in a square
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse cursor position
                (x, y) = pygame.mouse.get_pos()
                # Convert X and Y coordinates to square position (line, column)
                new_x, new_y = SudokuGame.convert_coordinates(x, y)
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
                    sudoku.draw_Board()
                    sudoku.auto_solve()

                if event.key == pygame.K_LALT:
                    new_game = True

                if event.key == pygame.K_BACKSPACE:
                    if sudoku.grid_values[sudoku.rect_y][sudoku.rect_x] != 0:
                        sudoku.update_grid(0, sudoku.rect_x, sudoku.rect_y)
                        sudoku.draw_number('0', sudoku.rect_x, sudoku.rect_y, (255, 255, 255))

        if new_game is False:
            sudoku.redraw_board()  # redraw board and grid values
            FPS.tick(FPS_value)
            pygame.display.update()  # Refresh display content
        else:
            main()


main()
