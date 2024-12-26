import pygame # type: ignore
import random

# Initialize Pygame
pygame.init()

# Set up game constants
GRID_SIZE = 4
GRID_WIDTH = 600
GRID_HEIGHT = 600
TILE_SIZE = GRID_WIDTH // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_TILE_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)
TEXT_COLOR = (255, 255, 255)

# Tile colors based on value
tile_colors = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Set up display
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption('2048')

# Font setup
font = pygame.font.SysFont("arial", 55)

def draw_board(board):
    screen.fill(BACKGROUND_COLOR)

    # Draw the tiles
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            tile = board[r][c]
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            # Draw background of the tile
            pygame.draw.rect(screen, tile_colors.get(tile, EMPTY_TILE_COLOR), (x, y, TILE_SIZE, TILE_SIZE))

            if tile != 0:
                # Draw the text on the tile
                text_surface = font.render(str(tile), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

    pygame.display.flip()

def new_tile():
    """Generate a new tile at a random empty position."""
    tile_value = random.choice([2, 4])
    empty_positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if empty_positions:
        r, c = random.choice(empty_positions)
        board[r][c] = tile_value

def compress(board):
    """Move all non-zero tiles to the left."""
    new_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        fill_position = 0
        for c in range(GRID_SIZE):
            if board[r][c] != 0:
                new_board[r][fill_position] = board[r][c]
                fill_position += 1
    return new_board

def merge(board):
    """Merge tiles that are the same in one row."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if board[r][c] == board[r][c + 1] and board[r][c] != 0:
                board[r][c] *= 2
                board[r][c + 1] = 0
    return compress(board)

def rotate(board):
    """Rotate the grid 90 degrees clockwise."""
    return [[board[GRID_SIZE - 1 - c][r] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]

def move_left(board):
    """Perform a move to the left, merging tiles where possible."""
    return merge(compress(board))

def move_right(board):
    """Perform a move to the right."""
    return move_left(rotate(rotate(board)))

def move_up(board):
    """Perform a move up."""
    return move_left(rotate(rotate(rotate(board))))

def move_down(board):
    """Perform a move down."""
    return move_left(rotate(board))

def game_over(board):
    """Check if no more moves are possible (i.e., game over)."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if board[r][c] == board[r][c + 1] or board[r][c] == 0:
                return False
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 1):
            if board[r][c] == board[r + 1][c] or board[r][c] == 0:
                return False
    return True

# Main game loop
def main():
    global board
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    new_tile()
    new_tile()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_board = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    new_board = move_right(board)
                elif event.key == pygame.K_UP:
                    new_board = move_up(board)
                elif event.key == pygame.K_DOWN:
                    new_board = move_down(board)
                else:
                    new_board = board

                if new_board != board:
                    board = new_board
                    new_tile()
                
                if game_over(board):
                    print("Game Over!")
                    pygame.quit()
                    return

        draw_board(board)
        clock.tick(15)

if __name__ == '__main__':
    main()
