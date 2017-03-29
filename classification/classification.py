import random


class Tree:

    def __init__(self):
        self.traits = list()


class Trait:  # the nodes that make up the tree

    def __init__(self):
        self.value = 0  # the trait number (1-10)
        self.parent = None  # which trait this node depends on
        self.depth = 0
        self.probability = 0.0


def generate_class_tree():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(values)
    tree = Tree()

    i = 0
    depth = 0
    while i < len(values):
        trait = Trait()
        trait.value = values[i]
        trait.depth = depth
        tree.traits.append(trait)
        if 7 >= i > 1:
            trait.parent = values[i - 2]
        elif i > 0:
            trait.parent = values[i - 1]

        if i == 0 or i % 2 == 0 or i >= 7:
            depth += 1
        i += 1

    return tree


# to be called at top level
def main():
    tree = generate_class_tree()
    for trait in tree.traits:
        print str(trait.value) + ' -- ' + str(trait.depth) + ' -- ' + str(trait.parent)

# top level code
if __name__ == '__main__':
    main()
