import sys
import pygame

pygame.init()


# Game settings
misere: bool = False
dimension: int = 3

# Pygame constants
SCREEN = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
WIDTH, HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Tic-Tac-Toe")
FONT = pygame.font.SysFont(None, 36)
FPS = 60

# Display settings
CELL_SIZE = min(WIDTH, HEIGHT) // dimension

# Colors
BG = (24, 24, 24)
LINE = (23, 145, 135)
X_COLOR = (19, 128, 13)
O_COLOR = (229, 24, 20)
MSG_COLOR = (33, 56, 214)

# State
show_menu = True
board = [[None for _ in range(dimension)] for _ in range(dimension)]
turn = 'X'
game_over = False

def update_dimensions():
    global WIDTH
    global HEIGHT
    global CELL_SIZE
    WIDTH, HEIGHT = SCREEN.get_size()
    CELL_SIZE = min(WIDTH, HEIGHT) // dimension

def draw_background():
    SCREEN.fill(BG)

def draw_grid():
    for i in range(1, dimension):
        pygame.draw.line(SCREEN, LINE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        pygame.draw.line(SCREEN, LINE, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)

def draw():
    update_dimensions()
    draw_background()
    draw_grid()
    pygame.display.flip()

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        draw()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
