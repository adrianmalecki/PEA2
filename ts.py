import copy
import random
from queue import *
import copy
import time
import random
import operator
import math
from sys import maxsize


class TabuSearch:
    def __init__(self, max_time):
        self.best_path = maxsize
        self.lowest_cost = maxsize
        self.current_path = maxsize
        self.current_cost = maxsize
        self.max_time = max_time
        self.counter = 0
        self.tabu_list = []
        pass

    def find_solution(self, nodes):
        size = len(nodes)
        total_time = 0
        find_time = 0
        self.current_path, self.lowest_cost = self.first_solution(nodes, size)
        self.best_path = self.current_path
        self.tabu_list = [[0 for i in range(size)] for i in range(size)]
        while total_time < self.max_time:
            start = time.process_time()
            if self.counter > size:
                self.current_path = self.best_path
                self.counter = 0
                self.tabu_list = [[0 for i in range(size)] for i in range(size)]
            v1 = random.randint(0, size - 1)
            new_cost, new_path, v2 = self.find_best_transformation(v1, nodes)

            if new_cost < self.lowest_cost:  # przejscie lepsze
                find_time = total_time
                self.best_path = new_path
                self.current_path = new_path
                self.lowest_cost = new_cost

            elif self.tabu_list[v1][v2] > 0:
                continue

            else:
                self.current_path = new_path
                self.counter += 1

            self.tabu_list[v1][v2] += size   #ustawienie kadencji
            self.verify_tabu()
            duration = time.process_time() - start

            total_time += duration
        return self.best_path, self.lowest_cost, find_time

    def verify_tabu(self):
        for x, rows in enumerate(self.tabu_list):
            for y, i in enumerate(rows):
                if type(i) == int and i > 0:
                    self.tabu_list[x][y] = i - 1

    def first_solution(self, nodes, size):
        help_list = copy.deepcopy(nodes)
        node = random.randint(0, size - 1)
        path = []
        for i in range(0, size):
            help_list[i][node] = 100000000

        while len(path) < size:
            path.append(node)
            min_value = min(help_list[node])
            node = help_list[node].index(min_value)
            for i in range(0, size):
                help_list[i][node] = 100000000
        cost = self.calculate_cost(nodes, path)
        return path, cost

    def calculate_cost(self, nodes, path):
        cost = 0
        for i in range(1, len(path)):
            cost += nodes[path[i - 1]][path[i]]
        cost += nodes[path[len(nodes) - 1]][path[0]]
        return cost

    def swap(self, node1, node2, path):
        path[node1], path[node2] = path[node2], path[node1]

    def find_best_transformation(self, node, nodes):
        queue = PriorityQueue()
        size = len(nodes)
        for i in range(0, size - 1):
            if i != node:
                transformed_path = copy.deepcopy(self.current_path)
                self.swap(node, i, transformed_path)
                transformed_cost = self.calculate_cost(nodes, transformed_path)
                queue.put((transformed_cost, transformed_path, i))
        return queue.get()
