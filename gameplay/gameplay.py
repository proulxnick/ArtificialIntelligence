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

    green = 0
    red = 0
    for i in board:
        if i.color == 'green':
            green += 1
        elif i.color == 'red':
            red += 1

    if green > 18:
        diff = green - 18
        x = 0
        for tile in board:
            if tile.color == 'green' and not x > diff:
                tile.color = 'red'
            x += 1

    elif red > 18:
        diff = red - 18
        x = 0
        for tile in board:
            if tile.color == 'red' and not x > diff:
                tile.color = 'green'
            x += 1

    return board


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


# 'player' is a string denoting the color of the current player making a move at this instance
def successor_processing(board, player, node):
    json_path = 'C:\Users\Nick\PycharmProjects\ArtificialIntelligence\index_config\index_config.json'
    with open(json_path) as data_file:
        indexing_params = json.load(data_file)
    x_sums = [4, 10, 18, 26, 34, 42, 48]
    y_sums = [1, 5, 11, 19, 27, 35, 43, 49]
    i = 0  # indexing value
    for piece in board:
        if not piece.color == 'None':
            stack = piece.height  # for control - need to make multiple moves with stacks while splitting the stack
            while stack > 0:  # move N, S, E, or W all possible combos
                # move up
                new_board = copy_list(board)
                move_up_index = indexing_params["indexes"][str(i + 1)]["up"][str(stack)]
                sum_stack_heights = stack + int(new_board[int(move_up_index) - 1].height)
                difference = 0  # will be number of pieces captured in a move
                if sum_stack_heights > 5:
                    difference = sum_stack_heights - 5
                    sum_stack_heights = 5

                # create new game piece and place on board
                game_piece = GamePiece()
                game_piece.color = piece.color
                game_piece.height = sum_stack_heights
                empty_game_piece = GamePiece()

                new_board[i] = empty_game_piece
                new_board[int(move_up_index)] = game_piece

                # create new node and save the board as state and difference as number of pieces captured
                new_node = Node()
                new_node.state = new_board
                new_node.pieces_captured = difference
                new_node.parent = node
                new_node.depth = node.depth + 1

                node.children.append(new_node)

                stack -= 1
        i += 1


def print_board(board):
    x_sums = [4, 10, 18, 26, 34, 42, 48]
    i = 1  # for x axis
    j = 1  # for y axis
    print '  ',
    for piece in board:
        print piece.color,
        if i in x_sums:
            print ''

        if i in x_sums:
            j += 1
            if j == 2 or j == 7:
                print ' ',
            if j == 8:
                print '  ',
        i += 1


# to be called at top level
def main():
    json_path = 'C:\Users\Nick\PycharmProjects\ArtificialIntelligence\index_config\index_config.json'
    with open(json_path) as data_file:
        indexing_params = json.load(data_file)
    # x = str(indexing_params["indexes"]["1"]["hi"])
    board = initiate_board()
    print_board(board)

# top level code
if __name__ == '__main__':
    main()
