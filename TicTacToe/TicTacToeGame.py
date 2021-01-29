import pygame
import math
from math import inf

pygame.init()

# Screen
WIDTH = 500
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_pic = pygame.transform.scale(
    pygame.image.load("Images/x.png"), (150, 150))
O_pic = pygame.transform.scale(
    pygame.image.load("Images/o.png"), (150, 150))

# Fonts
END_FONT = pygame.font.SysFont('Arial', 40)


def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def grid_init():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing board array
    brd = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(brd)):
        for j in range(len(brd[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre
            brd[i][j] = (x, y, '', True)

    return brd


def emptyCells(brd):
    empty = []
    for i in range(3):
        for j in range(3):
            if brd[i][j][3] == True:
                empty.append([i, j])
    return empty


def click(brd, turn):

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(brd)):
        for j in range(len(brd[i])):
            x, y, char, can_play = brd[i][j]
            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
            print([x, y, m_x, m_y, dis])

            # If it's X's turn
            if turn == 1:

                # If it's inside the square
                if dis < WIDTH // ROWS // 2 and can_play:
                    images.append((x, y, X_pic))
                    brd[i][j] = (x, y, 1, False)
                    return

            # If it's O's turn
            elif turn == -1:
                if len(emptyCells(brd)) % 2 == 1 and choice == 1:
                    return
                if len(emptyCells(brd)) % 2 == 0 and choice == 2:
                    return
                result = Position(
                    AlphaBetaMM(brd, len(emptyCells(brd)), -inf, inf, -1))
                images.append((result[0], result[1], O_pic))
                if result[2] == i and result[3] == j and can_play:
                    brd[result[2]][result[3]] = (
                        result[0], result[1], -1, False)
                    return


# Check if someone has won
def who_won(brd):

    win_states = [[brd[0][0][2], brd[0][1][2], brd[0][2][2]],
                  [brd[1][0][2], brd[1][1][2], brd[1][2][2]],
                  [brd[2][0][2], brd[2][1][2], brd[2][2][2]],
                  [brd[0][0][2], brd[1][0][2], brd[2][0][2]],
                  [brd[0][1][2], brd[1][1][2], brd[2][1][2]],
                  [brd[0][2][2], brd[1][2][2], brd[2][2][2]],
                  [brd[0][0][2], brd[1][1][2], brd[2][2][2]],
                  [brd[0][2][2], brd[1][1][2], brd[2][0][2]]]

    if [1, 1, 1] in win_states:
        #display_message("X has won!")
        return 1

    elif [-1, -1, -1] in win_states:
        #display_message("O has won!")
        return -1

    return False


def has_drawn(brd):
    for i in range(3):
        for j in range(3):
            if brd[i][j][2] == '':
                return False

    display_message("Draw")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    if content[0] == 'X':
        end_text = END_FONT.render(content, 1, RED)
    elif content[0] == 'O':
        end_text = END_FONT.render(content, 1, BLUE)
    elif content[0] == 'D':
        end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) //
                        2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() //
                         2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def getScore(brd):
    if who_won(brd) == 1:
        return 10

    elif who_won(brd) == -1:
        return -10

    else:
        return 0


def AlphaBetaMM(brd, depth, alpha, beta, player):
    row = -1
    col = -1
    if depth == 0 or who_won(brd) == 1 or who_won(brd) == -1:
        return [row, col, getScore(brd)]
    else:
        for cell in emptyCells(brd):
            brd[cell[0]][cell[1]] = (
                PosXY(cell[1]), PosXY(cell[0]), player, False)
            score = AlphaBetaMM(brd, depth - 1, alpha, beta, -player)
            if player == 1:
                # X is the max player
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]

            else:
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            brd[cell[0]][cell[1]] = (
                PosXY(cell[1]), PosXY(cell[0]), '', True)

            if alpha >= beta:
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]


def Position(pos):
    dis_to_cen = WIDTH // ROWS // 2
    y = dis_to_cen * (2 * pos[0] + 1)
    x = dis_to_cen * (2 * pos[1] + 1)
    return [x, y, pos[0], pos[1]]


def PosXY(pos):
    dis_to_cen = WIDTH // ROWS // 2
    x = dis_to_cen * (2 * pos + 1)
    return x


def main():
    global images, draw, choice
    images = []
    draw = False

    run = True

    choice = int(input("You want to go first or second?(1/2)"))

    brd = grid_init()
    if(choice == 1):
        print('')
    else:
        click(brd, -1)
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click(brd, 1)
                click(brd, -1)
                print(emptyCells(brd))
                print(brd)

        render()

        if who_won(brd) == 1 or who_won(brd) == -1 or has_drawn(brd):
            if who_won(brd) == 1:
                display_message("X has won!")
            elif who_won(brd) == -1:
                display_message("O has won!")
            run = False


while True:
    if __name__ == '__main__':
        main()
