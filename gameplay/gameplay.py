import random
import json
import sys


class GamePiece:

    def __init__(self):
        self.height = 0  # for the number of pieces stacked
        self.player = '0'  # denote an empty GamePiece by no player (a piece with player '0')


class Node:

    def __init__(self):
        self.state = list()
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible child nodes dynamically and append to list
        self.heuristic_value = 0
        self.pieces_captured = 0  # will be determined by # of left over pieces between 2 stacks > 5


def initiate_board():
    board = list()
    options = ['1', '2']
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
            player = random.choice(options)  # random choice of red or green piece to randomize the initial state
            if player == '1' and not j >= 18 \
               or player == '2' and k >= 18:
                game_piece = GamePiece()  # create game piece and append it to list
                game_piece.height = 1
                game_piece.player = '1'
                board.append(game_piece)
                j += 1
            elif player == '2' and not k >= 18 \
                    or player == '1' and j >= 18:
                game_piece = GamePiece()  # create game piece and append it to list
                game_piece.height = 1
                game_piece.player = '2'
                board.append(game_piece)
                k += 1
        i += 1

    # if the randomized board has extra of either player - swap until equal
    green = 0
    red = 0
    for i in board:
        if i.player == '2':
            green += 1
        elif i.player == '1':
            red += 1

    if green > 18:
        diff = green - 18
        x = 0
        for tile in board:
            if tile.player == '2' and not x > diff:
                tile.player = '1'
            x += 1

    elif red > 18:
        diff = red - 18
        x = 0
        for tile in board:
            if tile.player == '1' and not x > diff:
                tile.player = '2'
            x += 1

    return board


def copy_list(old_list):
    # used to copy contents of one list and create another list

    new_list = list()
    for i in old_list:
        new_list.append(i)

    return new_list


# 'player' is a string denoting the current player making a move at this instance
def successor_processing(player, node):
    json_path = 'C:\Users\Nick\PycharmProjects\ArtificialIntelligence\index_config\index_config.json'
    with open(json_path) as data_file:
        indexing_params = json.load(data_file)

    i = 0  # indexing value
    for piece in node.state:
        if piece.player == player:
            stack = piece.height  # for control - need to make multiple moves with stacks while splitting the stack

            # move up
            while stack > 0:
                new_board = copy_list(node.state)
                move_index = indexing_params["indexes"][str(i + 1)]["up"][str(stack)]
                sum_stack_heights = stack + int(new_board[int(move_index) - 1].height)
                difference = 0  # will be number of pieces captured in a move
                if sum_stack_heights > 5:
                    difference = sum_stack_heights - 5
                    sum_stack_heights = 5

                # create new game piece and place on board
                game_piece = GamePiece()
                game_piece.player = piece.player
                game_piece.height = sum_stack_heights
                empty_game_piece = GamePiece()

                new_board[i] = empty_game_piece
                new_board[int(move_index) - 1] = game_piece

                # create new node and save the board as state and difference as number of pieces captured
                new_node = Node()
                new_node.state = new_board
                new_node.pieces_captured = difference
                new_node.parent = node
                new_node.depth = node.depth + 1

                node.children.append(new_node)
                stack -= 1

            stack = piece.height  # for control - need to make multiple moves with stacks while splitting the stack

            # move down
            while stack > 0:
                new_board = copy_list(node.state)
                move_index = indexing_params["indexes"][str(i + 1)]["down"][str(stack)]
                sum_stack_heights = stack + int(new_board[int(move_index) - 1].height)
                difference = 0  # will be number of pieces captured in a move
                if sum_stack_heights > 5:
                    difference = sum_stack_heights - 5
                    sum_stack_heights = 5

                # create new game piece and place on board
                game_piece = GamePiece()
                game_piece.player = piece.player
                game_piece.height = sum_stack_heights
                empty_game_piece = GamePiece()

                new_board[i] = empty_game_piece
                new_board[int(move_index) - 1] = game_piece

                # create new node and save the board as state and difference as number of pieces captured
                new_node = Node()
                new_node.state = new_board
                new_node.pieces_captured = difference
                new_node.parent = node
                new_node.depth = node.depth + 1

                node.children.append(new_node)
                stack -= 1

            stack = piece.height  # for control - need to make multiple moves with stacks while splitting the stack

            # move left
            while stack > 0:
                new_board = copy_list(node.state)
                move_index = indexing_params["indexes"][str(i + 1)]["left"][str(stack)]
                sum_stack_heights = stack + int(new_board[int(move_index) - 1].height)
                difference = 0  # will be number of pieces captured in a move
                if sum_stack_heights > 5:
                    difference = sum_stack_heights - 5
                    sum_stack_heights = 5

                # create new game piece and place on board
                game_piece = GamePiece()
                game_piece.player = piece.player
                game_piece.height = sum_stack_heights
                empty_game_piece = GamePiece()

                new_board[i] = empty_game_piece
                new_board[int(move_index) - 1] = game_piece

                # create new node and save the board as state and difference as number of pieces captured
                new_node = Node()
                new_node.state = new_board
                new_node.pieces_captured = difference
                new_node.parent = node
                new_node.depth = node.depth + 1

                node.children.append(new_node)
                stack -= 1

            stack = piece.height  # for control - need to make multiple moves with stacks while splitting the stack

            # move right
            while stack > 0:
                new_board = copy_list(node.state)
                move_index = indexing_params["indexes"][str(i + 1)]["right"][str(stack)]
                sum_stack_heights = stack + int(new_board[int(move_index) - 1].height)
                difference = 0  # will be number of pieces captured in a move
                if sum_stack_heights > 5:
                    difference = sum_stack_heights - 5
                    sum_stack_heights = 5

                # create new game piece and place on board
                game_piece = GamePiece()
                game_piece.player = piece.player
                game_piece.height = sum_stack_heights
                empty_game_piece = GamePiece()

                new_board[i] = empty_game_piece
                new_board[int(move_index) - 1] = game_piece

                # create new node and save the board as state and difference as number of pieces captured
                new_node = Node()
                new_node.state = new_board
                new_node.pieces_captured = difference
                new_node.parent = node
                new_node.depth = node.depth + 1

                node.children.append(new_node)
                stack -= 1
        i += 1
    return node  # this node will hold all the new states created for all of it's child nodes


def print_board(board):
    x_sums = [4, 10, 18, 26, 34, 42, 48]
    i = 1  # for x axis
    j = 1  # for y axis
    print '   ',
    for piece in board:
        print piece.player,
        if i in x_sums:
            print ''

        if i in x_sums:
            j += 1
            if j == 2 or j == 7:
                print ' ',
            if j == 8:
                print '   ',
        i += 1


# to be called at top level
def main():
    print '\n\nThe initial board state is:\n'
    board = initiate_board()
    print '_______________\n'
    print_board(board)
    print '\n_______________\n'

    root = Node()
    root.state = board

    new_node = successor_processing('1', root)
    for node in new_node.children:
        print '\n'
        print_board(node.state)

# top level code
if __name__ == '__main__':
    main()
