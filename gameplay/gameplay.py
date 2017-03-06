import random


class GamePiece:

    def __init__(self):
        self.height = 0  # for the number of pieces stacked
        self.color = 'empty'


class Node:

    def __init__(self):
        self.state = list()
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible child nodes dynamically and append to list
        self.heuristic_value = 0


def initiate_board():
    board = list()
    options = ['red', 'green']
    forbidden_indexes = [1, 2, 3, 4, 11, 18, 19, 26, 27,
                         34, 35, 42, 49, 50, 51, 52]
    i = 1
    j = 0  # number of red game pieces used
    k = 0  # number of green game pieces used
    while i <= 52:
        if i in forbidden_indexes:
            game_piece = GamePiece()  # create a generic empty board element
            board.append(game_piece)
        else:
            color = random.choice(options)  # random choice of red or green piece to randomize the initial state
            if color == 'red' and not j >= 18 \
               or color == 'green' and k >= 18:
                game_piece = GamePiece()  # create game piece and append it to list
                game_piece.height = 1
                game_piece.color = 'red'
                board.append(game_piece)
                j += 1
            elif color == 'green' and not k >= 18 \
                    or color == 'red' and j >= 18:
                game_piece = GamePiece()  # create game piece and append it to list
                game_piece.height = 1
                game_piece.color = 'green'
                board.append(game_piece)
                k += 1
        i += 1
    return board


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


def successor_processing(board):
    pass


def print_board(board):
    x_sums = [4, 10, 18, 26, 34, 42, 48]
    i = 1
    for piece in board:
        print piece.color,
        if i in x_sums:
            print ''
        i += 1


# to be called at top level
def main():
    board = initiate_board()
    print_board(board)

# top level code
if __name__ == '__main__':
    main()
