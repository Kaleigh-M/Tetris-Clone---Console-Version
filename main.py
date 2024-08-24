import random
import os
import msvcrt
import time


BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tetromino shapes
TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'Z': [[1, 1, 0],
          [0, 1, 1]]
}


def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# Print the game board
def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print("\nMove: w (rotate), a (left), s (down), d (right), q (quit)")

# check collision of Tetromino with board
def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            try:
                if cell and board[y + off_y][x + off_x]:
                    return True
            except IndexError:
                return True
    return False

# add a Tetromino to the board
def join_matrixes(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = cell
    return board

# Rotate the Tetromino shape
def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

# Handle user input
def get_key():
    if msvcrt.kbhit():
        return msvcrt.getch().decode('utf-8')
    return None

# Clear complete lines
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    new_board = [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_board
    return new_board, lines_cleared

def main():
    board = create_board()
    shape = random.choice(list(TETROMINOS.values()))
    offset = (3, 0)
    drop_time = time.time()
    delay = 0.5

    while True:
        board_copy = [row[:] for row in board]
        board_copy = join_matrixes(board_copy, shape, offset)
        print_board(board_copy)

        key = get_key()

        if key:
            if key == 'q':
                break
            elif key == 'w':
                rotated_shape = rotate(shape)
                if not check_collision(board, rotated_shape, offset):
                    shape = rotated_shape
            elif key == 'a':
                new_offset = (offset[0] - 1, offset[1])
                if not check_collision(board, shape, new_offset):
                    offset = new_offset
            elif key == 's':
                new_offset = (offset[0], offset[1] + 1)
                if not check_collision(board, shape, new_offset):
                    offset = new_offset
            elif key == 'd':
                new_offset = (offset[0] + 1, offset[1])
                if not check_collision(board, shape, new_offset):
                    offset = new_offset

        if time.time() - drop_time > delay:
            drop_time = time.time()
            new_offset = (offset[0], offset[1] + 1)
            if not check_collision(board, shape, new_offset):
                offset = new_offset
            else:
                board = join_matrixes(board, shape, offset)
                board, _ = clear_lines(board)
                shape = random.choice(list(TETROMINOS.values()))
                offset = (3, 0)
                if check_collision(board, shape, offset):
                    print_board(board)
                    print("Game Over")
                    break

        time.sleep(0.1)

if __name__ == "__main__":
    main()
