import pygame, sys, time
import Square as sq
import SudokuGame
import math

# BOARD AND SQUARE SIZES
BOARD_SIZE = (540, 600)

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
# Colors
GRAY = (129, 129, 129)
BLACK = (0, 0, 0)

FPS = pygame.time.Clock()
FPS_value = 60

font = pygame.font.SysFont("comicsans", 55)


def clean_board():
    # Initialize values in the board
    new_grid = [[0 for j in range(0, 9)] for i in range(0, 9)]

    for sq_x in range(0, 9):  # 0, 1, 2, 3, ...,8
        for sq_y in range(0, 9):
            if grid[sq_y][sq_x] != 0:
                new_grid[sq_y][sq_x] = sq.Square(sq_x, sq_y, grid[sq_y][sq_x], False)
            else:
                new_grid[sq_y][sq_x] = sq.Square(sq_x, sq_y, 0, True)
    return new_grid


def main():
    new_game = False
    elapsed_time = 0
    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, 1000)
    board = pygame.display.set_mode(BOARD_SIZE)
    pygame.display.set_caption('Sudoku Solver')  # Window Title

    sudoku = SudokuGame.Sudoku(board, clean_board())
    sudoku.draw_Board()
    start_ticks = time.time()  # starter tick
    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == timer:
                elapsed_time = round(time.time() - start_ticks)

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
                    sudoku.insert_number(1)
                if event.key == pygame.K_2:
                    sudoku.insert_number(2)
                if event.key == pygame.K_3:
                    sudoku.insert_number(3)
                if event.key == pygame.K_4:
                    sudoku.insert_number(4)
                if event.key == pygame.K_5:
                    sudoku.insert_number(5)
                if event.key == pygame.K_6:
                    sudoku.insert_number(6)
                if event.key == pygame.K_7:
                    sudoku.insert_number(7)
                if event.key == pygame.K_8:
                    sudoku.insert_number(8)
                if event.key == pygame.K_9:
                    sudoku.insert_number(9)
                if event.key == pygame.K_KP1:
                    sudoku.insert_number(1)
                if event.key == pygame.K_KP2:
                    sudoku.insert_number(2)
                if event.key == pygame.K_KP3:
                    sudoku.insert_number(3)
                if event.key == pygame.K_KP4:
                    sudoku.insert_number(4)
                if event.key == pygame.K_KP5:
                    sudoku.insert_number(5)
                if event.key == pygame.K_KP6:
                    sudoku.insert_number(6)
                if event.key == pygame.K_KP7:
                    sudoku.insert_number(7)
                if event.key == pygame.K_KP8:
                    sudoku.insert_number(8)
                if event.key == pygame.K_KP9:
                    sudoku.insert_number(9)

                if event.key == pygame.K_SPACE:
                    # Remake the whole board with initial values
                    sudoku = SudokuGame.Sudoku(board, clean_board())
                    sudoku.draw_Board()
                    sudoku.auto_solve()

                if event.key == pygame.K_LALT:
                    new_game = True

                if event.key == pygame.K_BACKSPACE:
                    if sudoku.grid[sudoku.rect_y][sudoku.rect_x] != 0:
                        sudoku.update_grid(0, sudoku.rect_x, sudoku.rect_y)
                        sudoku.draw_number('0', sudoku.rect_x, sudoku.rect_y, (255, 255, 255))

        if new_game is False:
            sudoku.redraw_board(elapsed_time)  # redraw board and grid values
            FPS.tick(FPS_value)
            pygame.display.update()  # Refresh display content
        else:
            main()


main()
