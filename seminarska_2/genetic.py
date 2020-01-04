import numpy as np
import random
import collections
import draw_manager
import time
from itertools import combinations

class Gene:
    def __init__(self):
        self.move = (0, 0)
        self.left_weight = random.random()
        self.right_weight = random.random()
        self.up_weight = random.random()
        self.down_weight = random.random()
        self.heuristic_weights = list()
        self.heuristic_weights = np.random.dirichlet(np.ones(len(ends)), size=1)
        self.heuristic_weights = np.ndarray.tolist(self.heuristic_weights)[0]



    def determine_step(self, current, end, counter):
        neighbours = get_neighbors(current)
        left = 0
        right = 0
        up = 0
        down = 0
        for neighbor in neighbours:
            if(neighbor == "LEFT"):
                n = current[0] + 0, current[1] - 1
                h = 0
                j = 0
                for i in self.heuristic_weights:
                    h+= (calc_heuristics_manhattan(n, ends[j]) + 1) * i
                    j += 1
                h /= len(self.heuristic_weights)
                left = self.left_weight * (1.0 / h) + (1.0 / (1 + counter[n]))
            if(neighbor == "RIGHT"):
                n = (current[0], current[1] + 1)
                h = 0
                j = 0
                for i in self.heuristic_weights:
                    h += (calc_heuristics_manhattan(n, ends[j]) + 1) * i
                    j += 1
                h /= len(self.heuristic_weights)
                right = self.right_weight * ( 1.0 / h) + (1.0 / (1 + counter[n]))
            if(neighbor == "UP"):
                n = (current[0] - 1, current[1])
                h = 0
                j = 0
                for i in self.heuristic_weights:
                    h += (calc_heuristics_manhattan(n, ends[j]) + 1) * i
                    j += 1
                h /= len(self.heuristic_weights)
                up = self.up_weight * ( 1.0 / h) + (1.0 / (1 + counter[n]))
            if(neighbor == "DOWN"):
                n = (current[0] + 1, current[1])
                h = 0
                j = 0
                for i in self.heuristic_weights:
                    h += (calc_heuristics_manhattan(n, ends[j]) + 1) * i
                    j += 1
                h /= len(self.heuristic_weights)
                down = self.down_weight * (1.0 / h) + (1.0 / (1 + counter[n]))

        max_val = left
        step = (0, -1)
        if right > max_val:
            max_val = right
            step = (0, 1)
        if up > max_val:
            max_val = up
            step = (-1, 0)
        if down > max_val:
            max_val = down
            step = (1, 0)
        return step

    def mutate(self):
        mutate = random.randint(1, 5)
        if mutate == 1:
            self.left_weight = random.random()

        elif mutate == 2:
            self.right_weight = random.random()

        elif mutate == 3:
            self.up_weight = random.random()

        elif mutate == 4:
            self.down_weight = random.random()

        elif mutate == 5:
            self.heuristic_weights = list()
            self.heuristic_weights = np.random.dirichlet(np.ones(len(ends)), size=1)
            self.heuristic_weights = np.ndarray.tolist(self.heuristic_weights)[0]




class Walker:
    def __init__(self, chromosome_length):
        self.chromosome_lenght = chromosome_length
        self.path = list()
        self.path.append(tuple(start))
        self.genes = list()
        for i in range(self.chromosome_lenght):
            self.genes.append(Gene())
        self.found = False
        self.f_score = 0

    def walk(self, end):
        c = collections.Counter(self.path)
        for gene in self.genes:
            move = gene.determine_step(self.path[-1], end, c)
            a = list(self.path[-1])
            a[0] += move[0]
            a[1] += move[1]
            a = tuple(a)
            self.path.append(a)
            c = collections.Counter(self.path)
            if a in ends:
                self.found = True
                break

            self.f_score = self.calc_price()
            if(self.found):
                self.f_score /= 2
            else:
                self.f_score *= 1.5
            repeated = 0
            for i in c.values():
                if i > 1:
                    repeated += 1
            self.f_score += repeated * 5




    def calc_price(self):
        price = 0
        for step in self.path:
            if (narray[step] >= 0):
                price += narray[step]
        return price

    def mutate(self):
        mutations += 1
        self.genes[random.randint(0, len(self.genes) - 1)].mutate()

    @staticmethod
    def reproduce(a_parent, b_parent, mutate = True):
        a_child = Walker(empty_spaces)
        b_child = Walker(empty_spaces)
        mutated = False
        for i in range(empty_spaces):
            if(random.random() < 0.5):
                a_child.genes[i] = a_parent.genes[i]
                b_child.genes[i] = b_parent.genes[i]
            else:
                a_child.genes[i] = b_parent.genes[i]
                b_child.genes[i] = a_parent.genes[i]
            if(mutate):
                if(random.random() < 0.01):
                    if(random.random() < 0.5):
                        a_child.mutate()
                    else:
                        b_child.mutate()
                    mutated = True
        return (a_child, b_child, mutated)






def calc_heuristics_manhattan(aPoint, bPoint):
    return abs(aPoint[0] - bPoint[0]) + abs(aPoint[1] - bPoint[1])

def get_neighbors(current):
    neighbors = list()
    current = list(current)
    original = current.copy()

    #levo
    current[1] -= 1
    if current[1] >= 0:
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append("LEFT")
    current = original.copy()

    #desno
    current[1] += 1
    if current[1] < np.size(narray, 1):
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append("RIGHT")
    current = original.copy()

    #gor
    current[0] -= 1
    if current[0] >= 0:
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append("UP")
    current = original.copy()

    #dol
    current[0] += 1
    if current[0] < np.size(narray, 0):
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append("DOWN")
    current = original.copy()

    return neighbors


narray = np.loadtxt("labyrinth_4.txt", int, delimiter=",")
start = np.argwhere(narray == -2)
start = list(map(list, start))[0]
ends = np.argwhere(narray == -3)
ends = list(map(tuple, ends))

empty_spaces = len(np.argwhere(narray >= 0))
empty_spaces += len(np.argwhere(narray == -3))

dm = draw_manager.DrawManager(narray)

dm.draw_lab()
generation = list()
for i in range(200):
    generation.append(Walker(empty_spaces))

old_generation = None
combos = [i for i in range(20)]
combos = [i for i in combinations(combos, 2)]
for i in range(10):
    for walker in generation:
        walker.walk(ends[0])
    mutations = 0
    generation.sort(key = lambda x: x.f_score)
    if old_generation != None:
        if generation[0].f_score > old_generation[0].f_score:
            generation = old_generation.copy()
            #random.shuffle(generation)
            print("GENERATIONAL DISASTER")
    new_generation = list()
    """
    for i in range(10):
        for j in range(10):
            children = Walker.reproduce(generation[i], generation[j])
            if(i == j):
                new_generation.append(children[0])
            else:
                new_generation.append(children[0])
                new_generation.append(children[1])
    """
    for j in combos:
        children = Walker.reproduce(generation[0], generation[j[1]])
        new_generation.append(children[0])
        new_generation.append(children[1])
        if children[3]:
            mutations += 1

    #for j in range(5):
     #   new_generation.append(generation[i])
    old_generation = generation.copy()
    generation = new_generation.copy()
    print("Best f_score: {}\npath price: {}\nnumber of mutations: {}".format(old_generation[0].f_score, old_generation[0].calc_price(), mutations))


dm.draw_end_path(old_generation[0].path)

dm.call_sys_exit()
