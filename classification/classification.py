import random


class Tree:

    def __init__(self):
        self.traits = list()
        self.probabilities = dict()
        self.vector_data = list()
        self.training = list()
        self.testing = list()


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

    tree.probabilities = probability_dict
    return tree


def get_max_spanning():
    pass


def generate_vector_data(tree):
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
                parent_probability = tree.probabilities[trait.parent]
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

    tree.vector_data = vector_list
    return tree


def training_testing(training_set, testing_set, index, class_trees):
    i = 0
    class_probabilities = list()
    while i < 10:
        count = 0.0
        for vector in training_set[index]:
            if vector[i] == 0:
                count += 1.0
        i += 1
        total = round(count / 1599.0, 2)
        class_probabilities.append(total)

    new_tree = class_trees[index]
    new_tree.training = class_probabilities

    i = 0
    class_probabilities = list()
    while i < 10:
        count = 0.0
        for vector in testing_set[index]:
            if vector[i] == 0:
                count += 1.0
        i += 1
        total = round(count / 400.0, 2)
        class_probabilities.append(total)

    new_tree.testing = class_probabilities
    return new_tree


def get_classifiers(class_trees):
    training_set = list()
    testing_set = list()

    # add equal number of data sets to the training and testing sets for each class
    for tree in class_trees:
        testing_set.append(tree.vector_data[:400])
        training_set.append(tree.vector_data[400:-1])

    new_class1 = training_testing(training_set, testing_set, 0, class_trees)
    class_trees[0] = new_class1
    new_class2 = training_testing(training_set, testing_set, 1, class_trees)
    class_trees[1] = new_class2
    new_class3 = training_testing(training_set, testing_set, 2, class_trees)
    class_trees[2] = new_class3
    new_class4 = training_testing(training_set, testing_set, 3, class_trees)
    class_trees[3] = new_class4

    accuracies = list()
    for tree in class_trees:
        diffs = list()
        i = 0
        while i < 10:
            diff = round(tree.training[i] - tree.testing[i], 2)
            if diff < 0:
                diff *= -1
            diffs.append(diff)
            i += 1
        accuracy = 1 - sum(diffs)
        accuracies.append(accuracy)

    total_accuracy = sum(accuracies) / 4.0

    return accuracies, total_accuracy


def get_real_data(averages):
    data_path = 'C:\Users\Nick\Desktop\Work\AI\Datasets\wine.csv'

    classes = list()
    class1 = list()
    class2 = list()
    class3 = list()
    data = list(open(data_path).readlines())
    i = 0
    for line in data:
        line = line.strip('\n').strip(" ' ")
        if i < 59:
            line = line.split(',')
            line = line[1:]
            class1.append(line)
        elif 130 > i >= 59:
            line = line.split(',')
            line = line[1:]
            class2.append(line)
        else:
            line = line.split(',')
            line = line[1:]
            class3.append(line)
        i += 1
    classes.append(class1)
    classes.append(class2)
    classes.append(class3)

    # create binary data from classes
    x = 0
    while x < 13:
        k = 0
        while k < 3:
            for each_class in classes:
                j = 0
                for each_class_set in each_class:
                    if float(each_class_set[x]) <= averages[x]:
                        classes[k][j][x] = 0
                    else:
                        classes[k][j][x] = 1
                    j += 1
                k += 1
        x += 1

    return classes


def real_training_testing(training_set, testing_set, index):
    i = 0
    class_training_probabilities = list()
    class_testing_probabilities = list()
    while i < 13:
        count = 0.0
        for vector in training_set[index]:
            if vector[i] == 0:
                count += 1.0
        i += 1
        total = round(count / 143.0, 2)
        class_training_probabilities.append(total)

    i = 0
    while i < 13:
        count = 0.0
        for vector in testing_set[index]:
            if vector[i] == 0:
                count += 1.0
        i += 1
        total = round(count / 35.0, 2)
        class_testing_probabilities.append(total)

    training = sum(class_training_probabilities)
    testing = sum(class_testing_probabilities)
    return training, testing


def get_real_classifier(classes):
    training_set = list()
    testing_set = list()

    testing_set.append(classes[0][:12])
    testing_set.append(classes[1][:14])
    testing_set.append(classes[2][:9])
    training_set.append(classes[0][12:-1])
    training_set.append(classes[1][14:-1])
    training_set.append(classes[2][9:-1])

    training, testing = real_training_testing(training_set, testing_set, 0)
    total = testing - training
    if total < 0:
        total *= -1

    total = 1 - total
    return total


# to be called at top level
def main():
    # create all 4 class trees for part 1 and generate their data and store them in a list
    parent_tree = generate_class_tree()
    class_trees = list()

    tree1 = Tree()
    tree1.traits = parent_tree.traits
    tree1 = generate_probabilities(tree1)
    tree1 = generate_vector_data(tree1)
    class_trees.append(tree1)

    tree2 = Tree()
    tree2.traits = parent_tree.traits
    tree2 = generate_probabilities(tree2)
    tree2 = generate_vector_data(tree2)
    class_trees.append(tree2)

    tree3 = Tree()
    tree3.traits = parent_tree.traits
    tree3 = generate_probabilities(tree3)
    tree3 = generate_vector_data(tree3)
    class_trees.append(tree3)

    tree4 = Tree()
    tree4.traits = parent_tree.traits
    tree4 = generate_probabilities(tree4)
    tree4 = generate_vector_data(tree4)
    class_trees.append(tree4)

    accuracies, total_accuracy = get_classifiers(class_trees)

    print 'DT Structure: \n'
    i = 0
    for trait in parent_tree.traits:
        if i == 0:
            print '  ' + str(trait.value)
        elif i == 1 or i == 3 or i == 5 or i == 7 or i == 9:
            if trait.value == 10:
                print str(trait.value) + ' ',
            else:
                print str(trait.value) + '  ',
        else:
            print str(trait.value)
        i += 1

    print '\n\nClass 1 Weights: '
    for key in class_trees[0].probabilities:
        print str(key) + ' = ' + str(class_trees[0].probabilities[key])

    print '\n\nClass 2 Weights: '
    for key in class_trees[1].probabilities:
        print str(key) + ' = ' + str(class_trees[1].probabilities[key])

    print '\n\nClass 3 Weights: '
    for key in class_trees[2].probabilities:
        print str(key) + ' = ' + str(class_trees[2].probabilities[key])

    print '\n\nClass 4 Weights: '
    for key in class_trees[3].probabilities:
        print str(key) + ' = ' + str(class_trees[3].probabilities[key])

    print '\n\n' + 'Class 1 Accuracy :' + str(accuracies[0]) + \
                   '\nClass 2 Accuracy :' + str(accuracies[1]) + \
                   '\nClass 3 Accuracy :' + str(accuracies[2]) + \
                   '\nClass 4 Accuracy :' + str(accuracies[3]) + '\n'
    print 'Total Accuracy: ' + str(round(total_accuracy, 2))

    print '\n\n\n ---------------- PART 2 ----------------\n\n\n'

    averages = [13.00, 2.34, 2.37, 19.49, 99.74, 2.30,
                2.03, 0.36, 1.59, 5.06, 0.96, 2.61, 746.89]
    classes = get_real_data(averages)  # binary data

    print 'The averages for each column are: '
    for avg in averages:
        print avg

    accuracy = get_real_classifier(classes)
    print '\nAccuracy for real wine data set is: ' + str(accuracy)


# top level code
if __name__ == '__main__':
    main()
