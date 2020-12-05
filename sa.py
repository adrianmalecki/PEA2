import copy
import random
from sys import maxsize
from read_data import Read_data

class SimulatedAnnealing:
    def __init__(self):
        self.temperature = 60
        self.free_nodes = []
        pass

    def find_solution(self, nodes):
        size = len(nodes)

        self.first_solution(nodes, size)

    def first_solution(self, nodes, size):
        help_list = copy.deepcopy(nodes)
        node = 8#random.randint(0, size)
        path = []
        for i in range(0, size):
            help_list[i][node] = 100000000

        while len(path) < size:
            path.append(node)
            min_value = min(help_list[node])
            node = help_list[node].index(min_value)
            for i in range(0, size):
                help_list[i][node] = 100000000
        print(path)
        self.calculate_cost(nodes, path)
        return path

    def calculate_cost(self, nodes, path):
        cost = 0
        for i in range(1, len(path)):
            cost += nodes[path[i-1]][path[i]]
        cost += nodes[path[len(nodes)-1]][path[0]]
        print('cost', cost)




