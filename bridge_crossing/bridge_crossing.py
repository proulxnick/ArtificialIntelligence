class Runner:
    def __init__(self, run_time):
        self.run_time = run_time


class State:
    def __init__(self, left_num, torch, right_num):
        self.runners_left = left_num
        self.torch = torch
        self.runners_right = right_num
        self.parent = None

    def is_at_goal(self):
        if self.runners_left == 0 \
           and self.torch == 'Right':
            return True
        else:
            return False

    def is_valid_cross(self):
        if 0 <= self.runners_left <= 6 \
           and 0 <= self.runners_right <= 6:
            return True
        else:
            return False


def process_crossing(state, left_runners, right_runners):
    child_nodes = list()
    while not state.is_at_goal():
        if state.torch == 'Left':  # the torch is on the left -- must cross right
            # moving two runners to the right
            new_state = State(state.runners_left - 2, 'Right', state.runners_right + 2)
            if new_state.is_valid_cross():
                new_state.parent = state
                child_nodes.append(new_state)

        else:  # the torch is on the right -- must cross left
            # have one person bring the torch back to the left
            new_state = State(state.runners_left + 1, 'Left', state.runners_right - 1)
            if new_state.is_valid_cross():
                new_state.parent = state
                child_nodes.append(new_state)

    return child_nodes


# only hard coded for testing
def initiate_crossing():

    left_side = list()
    right_side = list()
    torch = 'Left'

    # define the runners
    r1 = Runner(4)
    r2 = Runner(6)
    r3 = Runner(8)
    r4 = Runner(10)
    r5 = Runner(12)
    r6 = Runner(14)

    left_side.append(r1)
    left_side.append(r2)
    left_side.append(r3)
    left_side.append(r4)
    left_side.append(r5)
    left_side.append(r6)

    return left_side, torch, right_side


def main():
    left_runners, torch, right_runners = initiate_crossing()
    left_len = len(left_runners)
    right_len = len(right_runners)
    state = State(left_len, 'Left', right_len)
    print process_crossing(state, left_runners, right_runners)


if __name__ == '__main__':
    main()
