class BridgeCrossException(Exception):

    def __init__(self, message):
        # use as class exception for situational exception handling
        self.message = message


class Runner:

    def __init__(self, run_time):
        self.run_time = run_time


class State:

    def __init__(self, left_num, torch, right_num, run_time):
        # each Node will have a state of this format
        self.runners_left = left_num
        self.torch = torch
        self.runners_right = right_num
        self.run_time = run_time

    def is_at_goal(self):
        # check if the state is equal to the goal
        if self.runners_left == 0 \
           and self.torch == 'Right' \
           and self.runners_right > 0:
            return True
        else:
            return False


class Node:

    def __init__(self):
        self.state = None
        self.parent = None
        self.depth = 0
        self.children = list()  # to be used to create possible child nodes dynamically and append to list


# only hard coded for testing
def initiate_runners():
    left_side = list()
    right_side = list()
    torch = 'Left'

    total_runners = input('Enter number of runners: ')
    i = 1  # for control in while loop

    # get the run times of all the runners the user wants to create
    while i <= total_runners:
        new_runner_time = input('Enter run time of runner number ' + str(i) + ': ')
        runner = Runner(new_runner_time)
        left_side.append(runner)
        i += 1

    # initialize the root state and create a new root node with that state
    left_num = len(left_side)
    right_num = len(right_side)
    initial_state = State(left_num, torch, right_num, 0)
    node = Node()
    node.depth = 0
    node.parent = None
    node.state = initial_state
    run_time = node.state.run_time

    return left_side, torch, right_side, node, run_time, total_runners


def path_exists(path_list, new_node):
    # this is a method to check if the state of the given node exists in the given path
    is_old_state = False

    for node in path_list:
        if new_node.state.runners_left == node.state.runners_left \
           and new_node.state.runners_right == node.state.runners_right \
           and new_node.state.torch == node.state.torch:
            is_old_state = True
            break

    return is_old_state


def heuristic_1():
    # the goal of this heuristic function is to return the node in the
    # list passed in that has the slowest overall runtime
    pass


def heuristic_2():
    # the goal of this heuristic function is to add the runtime of each
    # node to its depth and return the cheapest option
    pass


def successor_processing(state, old_node, left_runners, right_runners):
    if state.is_at_goal():
        return 'Already at goal!'

    elif state.torch == 'Left':
        if len(left_runners) > 1:
            # while len(left_runners) > 1:
            # move 2 runners at a time across the bridge
            i = 0
            # while i < len(left_runners) - 1:
            for node in left_runners:
                if i < len(left_runners) - 1:
                    j = 1  # index one after the first runner chosen by above loop
                    while j < len(left_runners):
                        new_state = State(state.runners_left - 2, 'Right', state.runners_right + 2,
                                          max(node.run_time, left_runners[j].run_time))

                        # set attributes of new node and move runners accordingly
                        new_node = Node()
                        new_node.state = new_state
                        new_node.parent = old_node
                        new_node.depth = old_node.depth + 1
                        old_node.children.append(new_node)
                        j += 1
                # remove the first in the list
                right_runners.append(node)
                left_runners.remove(node)
                i += 1

        if len(left_runners) == 1:
            # maybe for some reason there is less than 2 people and need to bring only one to right
            new_state = State(state.runners_left - 1, 'Right',
                              state.runners_right + 1, left_runners[0].run_time)

            # set attributes of new node and move runners accordingly
            new_node = Node
            new_node.state = new_state
            new_node.parent = old_node
            new_node.depth = old_node.depth + 1
            old_node.children.append(new_node)
            right_runners.append(left_runners[0])
            left_runners.remove(left_runners[0])

        return old_node, left_runners, right_runners

    elif state.torch == 'Right':
        for runner in right_runners:
            new_state = State(state.runners_left + 1, 'Left',
                              state.runners_right - 1, runner.run_time)

            # set attributes of new node and move runners accordingly
            new_node = Node()
            new_node.state = new_state
            new_node.parent = old_node
            new_node.depth = old_node.depth + 1
            old_node.children.append(new_node)
            left_runners.append(right_runners[0])
            right_runners.remove(right_runners[0])

        return old_node, left_runners, right_runners

    else:
        raise BridgeCrossException('Invalid torch placement')


def breadth_first():
    # initialize the root state and create a new root node with that state
    left_side, torch, right_side, node, run_time, total_runners = initiate_runners()

    path_to_goal = list()
    path_to_goal.append(node)

    while not node.state.is_at_goal():
        # initialize the root state and create a new root node with that state
        node, left_side, right_side = successor_processing(node.state,
                                                           node,
                                                           left_side,
                                                           right_side)
        # save the slowest run_time across bridge
        cheapest_run_time = 0
        curr_node = Node()
        for each_node in node.children:
            if not path_exists(path_to_goal, each_node):
                if cheapest_run_time == 0 \
                   or each_node.state.run_time < cheapest_run_time:
                    cheapest_run_time = each_node.state.run_time
                    curr_node = each_node  # current node now has cheapest run time at it's depth

        # append the node with the cheapest crossing time to the final path to the goal state
        path_to_goal.append(curr_node)
        run_time += curr_node.state.run_time
        node = curr_node  # get successors / fringe from the cheapest node at this state

    print '\nBreadth-first search chosen'
    return path_to_goal, run_time


def depth_first():
    # initialize the root state and create a new root node with that state
    left_side, torch, right_side, node, run_time, total_runners = initiate_runners()

    path_to_goal = list()
    path_to_goal.append(node)
    stack = list()  # use a stack for dfs
    already_processed = False

    while not node.state.is_at_goal():
        if not already_processed:
            node, left_side, right_side = successor_processing(node.state,
                                                               node,
                                                               left_side,
                                                               right_side)
            already_processed = True
            stack.extend(node.children)  # add the children to the top of the stack

        curr_node = stack.pop()  # take the latest child addition as current node
        if not path_exists(path_to_goal, curr_node):
            already_processed = False
            path_to_goal.append(curr_node)
            run_time += curr_node.state.run_time
            node = curr_node  # use this current node to get it's successors / fringe

    print '\nDepth-first search chosen'
    return path_to_goal, run_time


def a_star():
    # initialize the root state and create a new root node with that state
    left_side, torch, right_side, node, run_time, total_runners = initiate_runners()

    path_to_goal = list()
    path_to_goal.append(node)

    while not node.state.is_at_goal():
        # initialize the root state and create a new root node with that state
        node, left_side, right_side = successor_processing(node.state,
                                                           node,
                                                           left_side,
                                                           right_side)
        # save the slowest run_time across bridge
        cheapest_run_time = 0
        curr_node = Node()
        for each_node in node.children:
            if not path_exists(path_to_goal, each_node):
                if cheapest_run_time == 0 \
                        or each_node.state.run_time < cheapest_run_time:
                    cheapest_run_time = each_node.state.run_time
                    curr_node = each_node  # current node now has cheapest run time at it's depth

        # append the node with the cheapest crossing time to the final path to the goal state
        path_to_goal.append(curr_node)
        run_time += curr_node.state.run_time
        node = curr_node  # get successors / fringe from the cheapest node at this state


def print_path():
    # path, run_time = breadth_first()
    path, run_time = depth_first()
    # path, run_time = a_star()
    i = 0
    print '\n'
    for node in path:
        print 'Move: ' + str(i)
        print str(node.state.runners_left) + ',  ' + node.state.torch + ',  ' + str(node.state.runners_right)
        print 'Crossing Time: ' + str(node.state.run_time) + '\n'
        i += 1

    print 'Done!'
    print 'Total Time Elapsed: ' + str(run_time)


# to be called at top level
def main():
    print_path()


# top level code
if __name__ == '__main__':
    main()
