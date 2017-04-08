import random


class BadStateException(Exception):

    def __init__(self, message):
        self.message = message


class Node:

    def __init__(self):
        self.state = list()
        self.parent = None
        self.depth = 0
        self.children = list()
        self.heuristic_value = 0


# to be called at top level
def main():
    pass

# top level code
if __name__ == '__main__':
    main()
