import sys
import pygame

pygame.init()


# Game settings
misere: bool = False
dimension: int = 3

# Pygame constants
SCREEN = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
pygame.display.set_caption("Tic-Tac-Toe")
FONT = pygame.font.SysFont(None, 36)
FPS = 60

# Display settings - Check update_dimensions()
WIDTH, HEIGHT = SCREEN.get_size()
CELL_SIZE = (min(WIDTH, HEIGHT) - 2) // dimension
WIDTH_OFFSET = WIDTH // 2 if WIDTH > HEIGHT else 0
HEIGHT_OFFSET = HEIGHT // 2 if HEIGHT > WIDTH else 0

# Colors
BG = (24, 24, 24)
DARK_BG = (12, 12, 12)
LINE = (23, 145, 135)
X_COLOR = (229, 24, 20)
O_COLOR = (19, 128, 13)
MSG_COLOR = (33, 56, 214)

# State
show_menu = False
board = [[None for _ in range(dimension)] for _ in range(dimension)]
turn = 'O'
game_over = False
winner = None

# Handle window resizing

def update_dimensions():
    global WIDTH
    global HEIGHT
    global CELL_SIZE
    global WIDTH_OFFSET
    global HEIGHT_OFFSET
    WIDTH, HEIGHT = SCREEN.get_size()
    CELL_SIZE = (min(WIDTH, HEIGHT) - 2) // dimension
    WIDTH_OFFSET = (WIDTH - HEIGHT) // 2 if WIDTH > HEIGHT else 0
    HEIGHT_OFFSET = (HEIGHT - WIDTH) // 2 if HEIGHT > WIDTH else 0

# Drawing pipeline

def draw_background():
    SCREEN.fill(BG)

def darken_hovered_cell():
    x, y = pygame.mouse.get_pos()
    col = (x - WIDTH_OFFSET) // (CELL_SIZE + 1)
    row = (y - HEIGHT_OFFSET) // (CELL_SIZE + 1)
    if 0 <= row < dimension and 0 <= col < dimension and board[row][col] is None:
        pygame.draw.rect(SCREEN, DARK_BG, (WIDTH_OFFSET + col * (CELL_SIZE + 1), HEIGHT_OFFSET + row * (CELL_SIZE + 1), CELL_SIZE, CELL_SIZE))

def draw_grid():
    for i in range(1, dimension):
        pygame.draw.line(SCREEN, LINE, (WIDTH_OFFSET, i * CELL_SIZE + (i - 1) + HEIGHT_OFFSET), (WIDTH_OFFSET + dimension * CELL_SIZE + dimension - 1, i * CELL_SIZE + i - 1 + HEIGHT_OFFSET), 1)
        pygame.draw.line(SCREEN, LINE, (i * CELL_SIZE + WIDTH_OFFSET + i - 1, HEIGHT_OFFSET), (i * CELL_SIZE + WIDTH_OFFSET + i - 1, HEIGHT_OFFSET + dimension * CELL_SIZE + dimension - 1), 1)

def draw_x():
    for i in range(dimension):
        for j in range(dimension):
            if board[i][j] == 'X':
                x = WIDTH_OFFSET + j * CELL_SIZE + j
                y = HEIGHT_OFFSET + i * CELL_SIZE + i
                pygame.draw.line(SCREEN, X_COLOR, (x + 10, y + 10), (x + CELL_SIZE - 1 - 10, y + CELL_SIZE - 1 - 10), 3)
                pygame.draw.line(SCREEN, X_COLOR, (x + CELL_SIZE - 1 - 10, y + 10), (x + 10, y + CELL_SIZE - 1 - 10), 3)

def draw_o():
    for i in range(dimension):
        for j in range(dimension):
            if board[i][j] == 'O':
                x = WIDTH_OFFSET + j * CELL_SIZE + j
                y = HEIGHT_OFFSET + i * CELL_SIZE + i
                pygame.draw.aacircle(SCREEN, O_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 3)

def draw():
    update_dimensions()
    draw_background()
    darken_hovered_cell()
    draw_grid()
    draw_x()
    draw_o()
    pygame.display.flip()

# Handle game logic

def mark_cell(cell):
    global board, turn, game_over, winner
    row, col = cell
    board[row][col] = turn
    result = check_winner()
    if result:
        winner = result
        game_over = True
    swap_turn()

def reset_game():
    global board, turn, game_over, winner
    board = [[None for _ in range(dimension)] for _ in range(dimension)]
    turn = 'O'
    game_over = False
    winner = None

def swap_turn():
    global turn
    turn = 'O' if turn == 'X' else 'X'

def handle_click(pos):
    x, y = pos
    col = (x - WIDTH_OFFSET) // (CELL_SIZE + 1)
    row = (y - HEIGHT_OFFSET) // (CELL_SIZE + 1)
    if 0 <= row < dimension and 0 <= col < dimension and board[row][col] is None:
        return row, col
    return None

def check_winner():
    # Check rows and columns
    for i in range(dimension):
        if all(board[i][j] is not None for j in range(dimension)):
            if misere:
                return 'O' if turn == 'X' else 'X'
            return turn
        if all(board[j][i] is not None for j in range(dimension)):
            if misere:
                return 'O' if turn == 'X' else 'X'
            return turn

    # Check diagonals
    if all(board[i][i] is not None for i in range(dimension)):
        if misere:
            return 'O' if turn == 'X' else 'X'
        return turn
    if all(board[i][dimension - 1 - i] is not None for i in range(dimension)):
        if misere:
            return 'O' if turn == 'X' else 'X'
        return turn

    return None

# Main loop

def main():
    global game_over, winner
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and not show_menu:
                    pos = event.pos
                    cell = handle_click(pos)
                    if cell:
                        mark_cell(cell)
        draw()
        clock.tick(FPS+1)

if __name__ == "__main__":
    main()
