import sys
import pygame
import numpy as np

pygame.init()
# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Proportions and sizes
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WINNER = 3

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe by Khoi')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_line(color = WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, start_pos=(0, SQUARE_SIZE *i), end_pos = (WIDTH, SQUARE_SIZE *i), width= LINE_WIDTH)
        pygame.draw.line(screen, color, start_pos=(SQUARE_SIZE *i, 0), end_pos = (SQUARE_SIZE *i, HEIGHT), width= LINE_WIDTH)

def draw_figures(color = GRAY):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 2: # AI
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 1: # Player 1
                pygame.draw.line(screen, color, start_pos=(col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), end_pos=(col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), width=CROSS_WIDTH)
                pygame.draw.line(screen, color, start_pos=(col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), end_pos=(col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), width=CROSS_WIDTH)
def mark_square(row, col, player):
    board[row][col] = player
def available_square(row, col):
    return board[row][col] == 0
def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for i in range(BOARD_ROWS):
        if all(check_board[i, :] == player): return True # Kiểm tra hàng i
        if all(check_board[:, i] == player): return True # Kiểm tra cột i
    if all(np.diagonal(check_board) == player): return True
    if all(np.diagonal(np.fliplr(check_board)) == player): return True
    return False


def restart_game():
    screen.fill(BLACK)
    draw_line()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return 1
    elif check_win(1, minimax_board):
        return -1
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return move

draw_line()
player = 1
game_over = False

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            if available_square(int(mouseY // SQUARE_SIZE), int(mouseX // SQUARE_SIZE)):
                mark_square(int(mouseY // SQUARE_SIZE), int(mouseX // SQUARE_SIZE), player)
                if check_win(player):
                    game_over = True
                player = 2
                draw_figures()

                if not game_over:
                    best_move()
                    if check_win(2):
                        game_over = True
                    player = player %2 +1
                    if is_board_full():
                        game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                player = 1
                game_over = False
    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_line(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_line(RED)
        else:
            draw_line(GRAY)
            draw_figures()

    pygame.display.update()
        