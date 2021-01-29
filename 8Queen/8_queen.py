import random
import math


def init_brd():
    board = []
    for x in range(num_q):
        board.append(random.randint(0, num_q-1))
    return board


def cost(state):
    hit = 0
    for i in range(num_q):
        for j in range(i + 1, num_q):
            if state[i] == state[j]:
                hit += 1
            if abs(state[i] - state[j]) == (j - i):
                hit += 1
    return hit


def simulated_annealing():
    solution = False
    current = init_brd()
    hits = cost(current)
    t = init_temp
    # cooling rate
    sch = 0.01

    while t > 0:
        successor = current.copy()
        col = random.randint(0, num_q - 1)
        row = random.randint(0, num_q - 1)
        successor[col] = row
        hits_1 = cost(successor)
        delta = hits_1 - hits
        # check if the neighbor is better or the propability is bigger then random prop
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / t):
            current = successor.copy()
            hits = cost(current)
            t -= sch
        if hits == 0:
            solution = True
            print_board(current)
            break
    if solution is False:
        print_board(current)
        print("Failed")


def print_board(board):
    for col in range(num_q):
        for row in range(num_q):
            if board[col] == row:
                print("Q", end="  ")
            else:
                print("-", end="  ")
        print()
    print()


def main():
    global num_q, init_temp
    num_q = int(input("Please enter number of Queens => "))
    init_temp = int(input("Please enter initial Temperature => "))
    simulated_annealing()


if __name__ == "__main__":
    main()
