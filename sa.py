import copy
import random
from queue import *
import copy
import time
import random
import operator
import math
from sys import maxsize


class SimulatedAnnealing:
    def __init__(self, temperature, a, max_time):
        self.temperature = temperature
        self.best_path = maxsize
        self.lowest_cost = maxsize
        self.current_path = maxsize
        self.current_cost = maxsize
        self.max_time = max_time
        self.a = a
        pass

    def check_data_init(self):
        if self.temperature == 0:
            self.temperature = 1000
        if self.a == 0:
            self.a = 0.9
        if self.max_time == 0:
            self.max_time = 100

    def find_solution(self, nodes):
        self.check_data_init()
        size = len(nodes)
        total_time = 0
        self.current_path, self.lowest_cost = self.first_solution(nodes, size)
        self.best_path = self.current_path
        while total_time < self.max_time:
            start = time.process_time()
            v1 = random.randint(0, size - 1)
            new_cost, new_path = self.find_best_transformation(v1, nodes)

            if new_cost < self.lowest_cost:
                self.best_path = new_path
                self.current_path = new_path
                self.lowest_cost = new_cost
            else:
                probability = math.exp((self.lowest_cost - new_cost) / self.temperature)
                if random.random() < probability:
                    self.current_path = new_path
            duration = time.process_time() - start
            total_time += duration
            self.temperature = self.temperature * self.a
        return self.best_path, self.lowest_cost, self.temperature

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
                queue.put((transformed_cost, transformed_path))
        return queue.get()
