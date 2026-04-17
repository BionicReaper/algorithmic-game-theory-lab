import ctypes
import sys
import pygame

pygame.init()


# Game settings
misere: bool = False
dimension: int = 3
use_ai: bool = False

# Pygame constants
SCREEN = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
pygame.display.set_caption("Tic-Tac-Toe")
FONT = pygame.font.SysFont(None, 36)
FPS = 60

# Display settings - Check update_dimensions()
WIDTH, HEIGHT = SCREEN.get_size()
CELL_SIZE = (min(WIDTH, HEIGHT) - 2) // dimension
WIDTH_OFFSET = (WIDTH - HEIGHT) // 2 if WIDTH > HEIGHT else 0
HEIGHT_OFFSET = (HEIGHT - WIDTH) // 2 if HEIGHT > WIDTH else 0

# Colors
BG = (24, 24, 24)
DARK_BG = (12, 12, 12)
LIGHT_BG_O = (48, 72, 48)
LIGHT_BG_X = (72, 48, 48)
LINE = (23, 145, 135)
X_COLOR = (229, 24, 20)
O_COLOR = (19, 128, 13)
MSG_COLOR = (33, 56, 214)

# State
show_menu = True
show_winner_popup = False
board = [[None for _ in range(dimension)] for _ in range(dimension)]
turn = 'O'
game_over = False
winner = None

# Checkbox Rects
scaling = min(WIDTH, HEIGHT) / 600
checkbox_rects = {
    "misere": pygame.Rect(WIDTH // 2 - 100 * scaling, HEIGHT // 2 - 30 * scaling, 20 * scaling, 20 * scaling),
    "3x3": pygame.Rect(WIDTH // 2 - 100 * scaling, HEIGHT // 2 + 10 * scaling, 20 * scaling, 20 * scaling),
    "4x4": pygame.Rect(WIDTH // 2 - 100 * scaling, HEIGHT // 2 + 50 * scaling, 20 * scaling, 20 * scaling),
    "vs_ai": pygame.Rect(WIDTH // 2 - 100 * scaling, HEIGHT // 2 + 90 * scaling, 20 * scaling, 20 * scaling)
}

# Startbutton Rect
start_button_rect = pygame.Rect(WIDTH // 2 - 100 * scaling, HEIGHT // 2 + 140 * scaling, 200 * scaling, 40 * scaling)

# Handle window resizing

def update_dimensions():
    global WIDTH
    global HEIGHT
    global CELL_SIZE
    global WIDTH_OFFSET
    global HEIGHT_OFFSET
    global FONT
    global scaling
    global start_button_rect

    # Update screen related dimensions
    WIDTH, HEIGHT = SCREEN.get_size()
    CELL_SIZE = (min(WIDTH, HEIGHT) - 2) // dimension
    WIDTH_OFFSET = (WIDTH - HEIGHT) // 2 if WIDTH > HEIGHT else 0
    HEIGHT_OFFSET = (HEIGHT - WIDTH) // 2 if HEIGHT > WIDTH else 0

    # Update font size based on new dimensions
    FONT = pygame.font.SysFont(None, int(min(WIDTH, HEIGHT) / 600 * 36))

    # Update checkbox and button positions
    scaling = min(WIDTH, HEIGHT) / 600
    checkbox_rects["misere"] = pygame.Rect(WIDTH_OFFSET + 200 * scaling, HEIGHT_OFFSET + 100 * scaling, 20 * scaling, 20 * scaling)
    checkbox_rects["3x3"] = pygame.Rect(WIDTH_OFFSET + 200 * scaling, HEIGHT_OFFSET + 220 * scaling, 20 * scaling, 20 * scaling)
    checkbox_rects["4x4"] = pygame.Rect(WIDTH_OFFSET + 300 * scaling, HEIGHT_OFFSET + 220 * scaling, 20 * scaling, 20 * scaling)
    checkbox_rects["vs_ai"] = pygame.Rect(WIDTH_OFFSET + 200 * scaling, HEIGHT_OFFSET + 340 * scaling, 20 * scaling, 20 * scaling)
    start_button_rect = pygame.Rect(WIDTH_OFFSET + 200 * scaling, HEIGHT_OFFSET + 460 * scaling, 200 * scaling, 40 * scaling)

# Drawing pipeline

# Game drawing functions

def draw_background():
    SCREEN.fill(BG)

def darken_hovered_cell():
    if(game_over or show_menu):
        return
    x, y = pygame.mouse.get_pos()
    col = (x - WIDTH_OFFSET) // (CELL_SIZE + 1)
    row = (y - HEIGHT_OFFSET) // (CELL_SIZE + 1)
    if 0 <= row < dimension and 0 <= col < dimension and board[row][col] is None:
        pygame.draw.rect(SCREEN, DARK_BG, (WIDTH_OFFSET + col * (CELL_SIZE + 1), HEIGHT_OFFSET + row * (CELL_SIZE + 1), CELL_SIZE, CELL_SIZE))

def lighten_winning_cells():
    if (not game_over) or (winner is None):
        return
    WINNER_BG = LIGHT_BG_O if winner == 'O' else LIGHT_BG_X
    # Highlight winning cells
    for i in range(dimension):
        if all(board[i][j] is not None for j in range(dimension)):
            pygame.draw.rect(SCREEN, WINNER_BG, (WIDTH_OFFSET, HEIGHT_OFFSET + i * (CELL_SIZE + 1), dimension * CELL_SIZE + 2, CELL_SIZE))
            return
        if all(board[j][i] is not None for j in range(dimension)):
            pygame.draw.rect(SCREEN, WINNER_BG, (WIDTH_OFFSET + i * (CELL_SIZE + 1), HEIGHT_OFFSET, CELL_SIZE, dimension * CELL_SIZE + 2))
            return
    if all(board[i][i] is not None for i in range(dimension)):
        for i in range(dimension):
            pygame.draw.rect(SCREEN, WINNER_BG, (WIDTH_OFFSET + i * (CELL_SIZE + 1), HEIGHT_OFFSET + i * (CELL_SIZE + 1), CELL_SIZE, CELL_SIZE))
        return
    if all(board[i][dimension - 1 - i] is not None for i in range(dimension)):
        for i in range(dimension):
            pygame.draw.rect(SCREEN, WINNER_BG, (WIDTH_OFFSET + (dimension - 1 - i) * (CELL_SIZE + 1), HEIGHT_OFFSET + i * (CELL_SIZE + 1), CELL_SIZE, CELL_SIZE))
        return

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

def show_winner_popup_if_needed():
    global show_winner_popup
    if game_over and show_winner_popup:
        if sys.platform.startswith("win"):
            try:
                ctypes.windll.user32.MessageBoxW(0, f"{winner} wins!\nAfter pressing OK, press R to restart or ESC to quit to menu.", "Game Over", 0)
            except Exception:
                pass
        show_winner_popup = False

def draw_game():
    darken_hovered_cell()
    lighten_winning_cells()
    draw_grid()
    draw_x()
    draw_o()
    pygame.display.flip()
    show_winner_popup_if_needed()

# Menu drawing functions

def render_checkbox(label, value):
    checkbox_rect = checkbox_rects[label.lower().replace(" ", "_")]
    pos = (checkbox_rect.x, checkbox_rect.y)
    pygame.draw.rect(SCREEN, LINE, checkbox_rect, 2)
    if value:
        pygame.draw.line(SCREEN, LINE, (pos[0] + 4 * scaling, pos[1] + 10 * scaling), (pos[0] + 8 * scaling, pos[1] + 16 * scaling), 2)
        pygame.draw.line(SCREEN, LINE, (pos[0] + 8 * scaling, pos[1] + 16 * scaling), (pos[0] + 16 * scaling, pos[1] + 4 * scaling), 2)
    text = FONT.render(label, True, MSG_COLOR)
    SCREEN.blit(text, (pos[0] + 30 * scaling, pos[1]))
    return checkbox_rect

def render_start_button():
    text = FONT.render("Start Game", True, MSG_COLOR)
    pygame.draw.rect(SCREEN, LINE, start_button_rect, 2)
    # Center text in button
    text_rect = text.get_rect(center=start_button_rect.center)
    SCREEN.blit(text, text_rect)

def draw_menu():
    render_checkbox("Misere", misere)
    render_checkbox("3x3", dimension == 3)
    render_checkbox("4x4", dimension == 4)
    render_checkbox("Vs AI", use_ai)
    render_start_button()
    pygame.display.flip()

# Main draw function

def draw():
    update_dimensions()
    draw_background()
    if show_menu:
        draw_menu()
    else:
        draw_game()

# Handle menu logic

def handle_click_menu(pos):
    global misere, dimension, use_ai, show_menu
    if checkbox_rects["misere"].collidepoint(pos):
        misere = not misere
    elif checkbox_rects["3x3"].collidepoint(pos):
        dimension = 3
        reset_game()
    elif checkbox_rects["4x4"].collidepoint(pos):
        dimension = 4
        reset_game()
    elif checkbox_rects["vs_ai"].collidepoint(pos):
        use_ai = not use_ai
    elif start_button_rect.collidepoint(pos):
        reset_game()
        show_menu = False

# Handle game logic

def mark_cell(cell):
    global board, turn, game_over, winner, show_winner_popup
    row, col = cell
    board[row][col] = turn
    result = check_winner()
    if result:
        winner = result
        game_over = True
        show_winner_popup = True
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

def handle_click_board(pos):
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
    global game_over, winner, show_menu
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not show_menu:
                        show_menu = True
                    else:
                        running = False
                elif event.key == pygame.K_r:
                    reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and not show_menu:
                    pos = event.pos
                    cell = handle_click_board(pos)
                    if cell:
                        mark_cell(cell)
                elif show_menu:
                    pos = event.pos
                    handle_click_menu(pos)
        draw()
        clock.tick(FPS+1)

if __name__ == "__main__":
    main()
