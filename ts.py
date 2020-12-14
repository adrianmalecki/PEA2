import copy
import random
from queue import *
import copy
import time
import random
import operator
import math
from sys import maxsize

#klasa służaca do zanjdowania rozwiązania metoda tabu search
class TabuSearch:
    def __init__(self, nodes, deadline):
        self.nodes = nodes
        self.size = 0
        self.best_path = maxsize
        self.lowest_cost = maxsize
        self.current_path = maxsize
        self.current_cost = maxsize
        self.deadline = deadline
        self.no_improvement_counter = 0
        self.tabu_list = []
        pass
    #sprawdzenie czy użytkownik wprowadził parametry, jesli nie wczytanie domyślnych
    def check_data_init(self):
        if self.deadline == 0:
            self.deadline = 100

    # funkcja znajdująca rozwiązanie dla grafu
    def find_solution(self):
        self.check_data_init()
        total_time = 0
        find_time = 0
        self.size = len(self.nodes)
        self.current_path, self.lowest_cost = self.generate_solution() # przypisanie wygenerowanego rozwiązania do zmiennych
        self.best_path = self.current_path # przypisanie do najlepszego rozwiązania
        self.tabu_list = [[0 for i in range(self.size)] for i in range(self.size)] # wyzerownia listy tabu
        while total_time < self.deadline:  # sprawdzenie czy nie przekroczono warunku zatrzymania
            start = time.process_time()
            if self.no_improvement_counter > self.size: # sprawdzenie czy liczba iteracji bez poprawy rozwiązania nie przekroczyła zakresu
                self.current_path, t = self.generate_solution() # wygenerowanie nowej ścieżki
                self.no_improvement_counter = 0 # wyzerowanie licznika
                self.tabu_list = [[0 for i in range(self.size)] for i in range(self.size)] # wyzerownia listy tabu
            v1 = random.randint(0, self.size-1) # wylosowanie wierzchołka
            new_cost, new_path, v2 = self.find_best_transformation(v1) # znalezienie najlepszej transformacji dla wierzchołka

            if new_cost < self.lowest_cost:  # przejscie lepsze
                find_time = total_time
                self.best_path = new_path
                self.current_path = new_path
                self.lowest_cost = new_cost

            elif self.tabu_list[v1][v2] > 0: # przejście gorsze znajdujace sie na liście tabu
                continue

            else:  # przejście gorsze nie znajdujace sie na liście tabu
                self.current_path = new_path
                self.no_improvement_counter += 1

            self.tabu_list[v1][v2] += self.size   # ustawienie kadencji
            self.verify_tabu(self.tabu_list) # zaktualizowanie listy tabu
            duration = time.process_time() - start

            total_time += duration
        return self.best_path, self.lowest_cost, find_time

    # funkcja dekrementująca wartości w liście tabu
    def verify_tabu(self, tabu_list):
        help_list = []
        help_row = []
        for rows in tabu_list:
            for cols in rows:
                if cols > 0:
                    cols = cols - 1
                else:
                    cols = cols
                help_row.append(cols)
            help_list.append(help_row)
            help_row = []
        tabu_list = help_list
        return tabu_list

    # funkcja generujaca losowe rozwiązanie metoda zachłanną
    def generate_solution(self):
        help_list = copy.deepcopy(self.nodes)
        node = random.randint(0, self.size-1) # wylosowanie wierzchołka startowego
        path = []
        for i in range(0, self.size):
            help_list[i][node] = 100000000

        while len(path) < self.size:
            path.append(node)
            min_value = min(help_list[node])
            node = help_list[node].index(min_value)
            for i in range(0, self.size):
                help_list[i][node] = 100000000
        cost = self.calculate_cost(path)
        return path, cost

    # funkcja obliczajca koszt przejścia ścieżki
    def calculate_cost(self, path):
        cost = 0
        for i in range(1, len(path)):
            cost += self.nodes[path[i - 1]][path[i]]
        cost += self.nodes[path[len(self.nodes) - 1]][path[0]]
        return cost

    # funkcja podmienająca dwa wierzchołki w ścieżce
    def swap(self, node1, node2, path):
        path[node1], path[node2] = path[node2], path[node1]
        return path

    # funkcja znajdująca najlepsze sąsiedztwo
    def find_best_transformation(self, node):
        queue = PriorityQueue() # kolejka priorytetowa szeregująca wyniki według najnizszego kosztu
        for i in range(0, self.size - 1):
            if i != node:
                transformed_path = copy.deepcopy(self.current_path)
                transformed_path = self.swap(node, i, transformed_path) # podmienienie wierzchołków w ścieżce
                transformed_cost = self.calculate_cost(transformed_path)
                queue.put((transformed_cost, transformed_path, i)) # umieszczenie rozwiązania w kolejce priorytetowej
        return queue.get() # zwrócenie najlepszego rozwiązania
