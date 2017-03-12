import random
import json
import sys


class InvalidMoveException(Exception):

    def __init__(self, message):
        self.message = message


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
        self.min_max_value = 0


def start_game():
    board = list()
    options = ['1', '2']
    forbidden_indexes = [1, 2, 3, 4, 11, 18, 19, 26, 27,
                         34, 35, 42, 49, 50, 51, 52]

    i = 1  # index
    j = 0
    k = 1
    while i <= 52:
        if i not in forbidden_indexes:
            game_piece = GamePiece()
            game_piece.player = options[j]
            game_piece.height = 1
            board.append(game_piece)
            if k == 2 and j == 1:
                j = 0
                k = 1
            elif k == 2 and j == 0:
                j = 1
                k = 1
            else:
                k += 1
        else:
            game_piece = GamePiece()
            board.append(game_piece)

        i += 1
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


def min_play(node):
    if node.pieces_captured >= 8:
        return node.state, node.player
    new_node = successor_processing('2', node)
    moves = new_node.children
    best_score = float('inf')
    best_move = None
    for move in moves:
        next_state = move.state
        score = max_play(next_state)
        if score < best_score:
            best_move = move
            best_score = score

    if best_move is None:
        raise InvalidMoveException('No possible move -- Exiting')
    else:
        return best_move


def max_play(node):
    if node.pieces_captured >= 8:
        return node.state, node.player
    new_node = successor_processing('2', node)
    moves = new_node.children
    best_score = float('-inf')
    best_move = None
    for move in moves:
        next_state = move.state
        score = min_play(next_state)
        if score > best_score:
            best_move = move
            best_score = score

    if best_move is None:
        raise InvalidMoveException('No possible move -- Exiting')
    else:
        return best_move


def min_max_heuristic(board):
    count = 0

    for piece in board:
        if piece.player == '1':
            count += 1

    return count


def count_player_pieces(board):
    player_1 = 0
    player_2 = 0
    for piece in board:
        if piece.player == '1':
            player_1 += 1
        elif piece.player == '2':
            player_2 += 1

    return player_1, player_2


def min_max(node):
    path_to_goal = list()
    # stack = list()
    # node = Node()
    path_to_goal.append(node)
    total_captured = node.pieces_captured
    player_1_total = 18
    player_2_total = 18
    winner = ''
    total_moves = 0

    i = 0
    # total_captured >= 18
    while player_1_total > 0 and player_2_total > 0:
        if i % 2 == 0:
            new_node = successor_processing('2', node)
            player = '2'
        else:
            new_node = successor_processing('1', node)
            player = '1'

        for node in new_node.children:
            node.heuristic_value = min_max_heuristic(node.state)

        alpha = float('inf')
        beta = float('-inf')

        if player == '1':  # this is the max -- use the beta value
            for node in new_node.children:
                if node.heuristic_value > beta:  # max
                    beta = node.heuristic_value
        else:
            for node in new_node.children:
                if node.heuristic_value < alpha:  # min
                    alpha = node.heuristic_value

        if alpha == float('inf'):
            new_node.min_max_value = beta
        else:
            new_node.min_max_value = alpha

        for node in new_node.children:
            if node.heuristic_value == new_node.min_max_value:
                path_to_goal.append(node)
                total_captured += node.pieces_captured
                player_1_total, player_2_total = count_player_pieces(node.state)
                total_moves = node.depth
                break

        node = path_to_goal[-1]
        i += 1

    if player_1_total > player_2_total:
        winner = 'Player 1'
    else:
        winner = 'Player 2'

    return path_to_goal, winner, total_moves, total_captured


def mini_max(node):
    board = node.state
    player_1_total = 0
    player_2_total = 0
    winner = None

    depth = 0
    while depth <= 6:
        if depth % 2 == 0:
            new_node = successor_processing('2', node)
            player = '2'
        else:
            new_node = successor_processing('1', node)
            player = '1'

        for child in new_node.children:
            if player == '1':
                new_child_node = successor_processing('2', child)
            else:
                new_child_node = successor_processing('1', child)

        minimum = float('inf')
        for node in new_node.children:
            node.heuristic_value = min_max_heuristic(node.state)
            if node.heuristic_value < minimum:
                minimum = node.heuristic_value
        depth += 1

    print 'breakpoint'


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


def print_path(path_to_goal):
    for node in path_to_goal:
        print '\n'
        print_board(node.state)
        print '\n'


# to be called at top level
def main():
    print '\n\nThe initial board state is:\n'
    board = start_game()
    print '_______________\n'
    print_board(board)
    print '\n_______________\n'

    root = Node()
    root.state = board
    mini_max(root)
    # path_to_goal, winner, total_moves, total_captures = min_max(root)
    # print_path(path_to_goal)
    # print '\nThe game is over, ' + winner + ' wins!'
    # print 'Total moves: ' + str(total_moves)
    # print 'Total captures ' + str(total_captures)

# top level code
if __name__ == '__main__':
    main()
