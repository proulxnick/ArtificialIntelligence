import random
import json


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
        self.pieces_captured = 0


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


# 'player' is a string denoting the color of the current player making a move at this instance
def successor_processing(board, player):
    json_path = 'C:\Users\Nick\PycharmProjects\ArtificialIntelligence\index_config\index_config.json'
    with open(json_path) as data_file:
        indexing_params = json.load(data_file)
    x_sums = [4, 10, 18, 26, 34, 42, 48]
    y_sums = [1, 5, 11, 19, 27, 35, 43, 49]

    i = 0  # indexing value
    j = 1  # corresponding x-axis value
    k = 1  # corresponding y-axis value
    for piece in board:
        if piece.color == 'empty':
            continue
        elif piece.color == 'green':
            stack = piece.height  # for control - need to make multiple moves with stacks while splitting the stack
            while stack > 0:
                # move up for all possible stack sizes
                if stack == 5 and k == 6 \
                   and 7 > j > 2 \
                   or stack == 5 and k == 7 \
                   or stack == 5 and k == 8:
                    game_piece = GamePiece()
                    game_piece.color = 'green'
                    game_piece.height = stack


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
    json_path = 'C:\Users\Nick\PycharmProjects\ArtificialIntelligence\index_config\index_config.json'
    with open(json_path) as data_file:
        indexing_params = json.load(data_file)
    x = str(indexing_params["indexes"]["1"]["hi"])
    board = initiate_board()
    print_board(board)

# top level code
if __name__ == '__main__':
    main()
