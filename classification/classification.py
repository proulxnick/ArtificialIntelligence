import random


class Tree:

    def __init__(self):
        self.traits = list()


class Trait:  # the nodes that make up the tree

    def __init__(self):
        self.value = 0  # the trait number (1-10)
        self.parent = None  # which trait this node depends on
        self.parent_index = None
        self.depth = 0
        self.probability = 0.0
        self.parent_probability = 0.0


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
            trait.parent_index = i - 2
        elif i > 0:
            trait.parent = values[i - 1]
            trait.parent_index = i - 1

        if i == 0 or i % 2 == 0 or i >= 7:
            depth += 1
        i += 1

    return tree


def generate_probabilities(tree):
    probability_dict = dict()

    for trait in tree.traits:
        trait.probability = round(random.random(), 2)
        probability_dict[trait.value] = trait.probability  # match for dependant children

    return tree, probability_dict


def generate_vector_data(tree, probability_dict):
    vector_list = list()

    i = 1
    while i <= 2000:
        data_list = list()
        j = 0
        for trait in tree.traits:
            if j == 0:
                data_list.append(int(random.choice('01')))
            else:
                parent_index = trait.parent_index
                parent_probability = probability_dict[trait.parent]
                random_value = round(random.random(), 2)

                if data_list[parent_index] == 0:
                    if random_value <= parent_probability:
                        data_list.append(0)
                    else:
                        data_list.append(1)

                elif data_list[parent_index] == 1:
                    if random_value >= parent_probability:
                        data_list.append(0)
                    else:
                        data_list.append(1)

            j += 1
        i += 1
        vector_list.append(data_list)
    return vector_list


# to be called at top level
def main():
    tree = generate_class_tree()
    tree, probabilities = generate_probabilities(tree)
    vector_data = generate_vector_data(tree, probabilities)
    for trait in tree.traits:
        print str(trait.value) + ' -- ' + str(trait.depth) + ' -- ' + str(trait.parent)

# top level code
if __name__ == '__main__':
    main()
