import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (238, 238, 210)
BROWN = (118, 150, 86)

# Mapping of piece symbols to image file names
PIECE_IMAGES = {
    "r": "brook.png", "n": "bknight.png", "b": "bbishop.png", "q": "bqueen.png", "k": "bking.png", "p": "bpawn.png",
    "R": "wrook.png", "N": "wknight.png", "B": "wbishop.png", "Q": "wqueen.png", "K": "wking.png", "P": "wpawn.png"
}

# Board state
board = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "q", "k", "b", "n", "r"]
]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# Load piece images
piece_images = {}
for piece, filename in PIECE_IMAGES.items():
    path = os.path.join("pieces", filename)
    piece_images[piece] = pygame.image.load(path)
    piece_images[piece] = pygame.transform.scale(piece_images[piece], (SQUARE_SIZE, SQUARE_SIZE))

# Selected piece tracking
selected_piece = None
selected_pos = None

def draw_board():
    """Draws the chessboard."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    """Draws chess pieces using images."""
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def is_valid_move(piece, start, end , movement_count):
    """Basic movement validation (Can be expanded with proper chess rules)."""
    row1, col1 = start
    row2, col2 = end

    # Prevent placing on the same spot
    if (row1, col1) == (row2, col2):
        return False

    # Prevent moving on a piece of the same color
    if board[row2][col2] and board[row1][col1].isupper() == board[row2][col2].isupper():
        return False
    #making the movement one by one 
    if board[row1][col1].isupper() and movement_count%2==1:
        return False
    if not board[row1][col1].isupper() and movement_count%2==0:
        return False
    

    #pawn legal move 
    if piece =="P" and end[0]-start[0]!=1:
        print(start[0],end[0])
        return False
    if piece =="p" and start[0]-end[0]!=1:
        print(start[0],end[0])
        return False

    return True  # Allow all moves for now (can be expanded)

def main():
    """Main loop to display the board and handle movement."""
    global selected_piece, selected_pos

    running = True
    movment_count = 0

    while running:
        screen.fill((0, 0, 0))  # Clear screen
        draw_board()
        draw_pieces()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if board[row][col]:  # If there's a piece, select it
                    selected_piece = board[row][col]
                    selected_pos = (row, col)

            elif event.type == pygame.MOUSEBUTTONUP and selected_piece:
                x, y = pygame.mouse.get_pos()
                new_row, new_col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if is_valid_move(selected_piece, selected_pos, (new_row, new_col),movment_count):
                    # Move piece
                    print(selected_piece,selected_pos)
                    board[selected_pos[0]][selected_pos[1]] = ""
                    board[new_row][new_col] = selected_piece
                    movment_count +=1 
                    print(movment_count)
                # Reset selection
                selected_piece = None
                selected_pos = None

    pygame.quit()

if __name__ == "__main__":
    main()
