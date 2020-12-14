import copy
import random
from queue import *
import copy
import time
import random
import operator
import math
from sys import maxsize

#klasa służaca do zanjdowania rozwiązania metoda symulowanego wyżarzania
class SimulatedAnnealing:
    def __init__(self, temperature, a, deadline):
        self.temperature = temperature
        self.best_path = maxsize
        self.lowest_cost = maxsize
        self.current_path = maxsize
        self.current_cost = maxsize
        self.deadline = deadline
        self.no_improvement_counter = 0
        self.a = a
        pass

    #sprawdzenie czy użytkownik wprowadził parametry, jesli nie wczytanie domyślnych
    def check_data_init(self):
        if self.temperature == 0:
            self.temperature = 1000
        if self.a == 0:
            self.a = 0.99
        if self.deadline == 0:
            self.deadline = 100

    # funkcja znajdująca rozwiązanie dla grafu
    def find_solution(self, nodes):
        self.check_data_init()
        size = len(nodes)
        total_time = 0
        find_time = 0
        self.current_path, self.lowest_cost = self.first_solution(nodes, size) # przypisanie wygenerowanego rozwiązania do zmiennych
        self.best_path = self.current_path # przypisanie do najlepszego rozwiązania
        while total_time < self.deadline: # sprawdzenie czy nie przekroczono warunku zatrzymania
            start = time.process_time()
            if self.no_improvement_counter > size: # sprawdzenie czy liczba iteracji bez poprawy rozwiązania nie przekroczyła zakresu
                self.current_path = self.best_path # powrót do najlpeszego znalezionego rozwiązania
                self.temperature = 1000 # powrót do startowej temperatury
                self.no_improvement_counter = 0 # wyzerowanie licznika

            v1 = random.randint(0, size-1) # wylosowanie wierzchołka
            new_cost, new_path = self.find_best_transformation(v1, nodes) # znalezienie najlepszej transformacji dla wierzchołka

            if new_cost < self.lowest_cost:  # przejscie lepsze
                find_time = total_time
                self.best_path = new_path
                self.current_path = new_path
                self.lowest_cost = new_cost
                self.no_improvement_counter = 0
            else: # przejście gorsze
                self.no_improvement_counter += 1
                probability = math.exp((self.lowest_cost - new_cost) / self.temperature) # obliczenie prawdopodobieństwa przyjęcia rozwiązania gorszego
                if random.random() < probability:
                    self.current_path = new_path
            duration = time.process_time() - start
            total_time += duration
            self.temperature = self.temperature * self.a # zmniajszenie temperatury
        return self.best_path, self.lowest_cost, self.temperature, find_time

    # funkcja generujaca losowe rozwiązanie metoda zachłanną
    def first_solution(self, nodes, size):
        help_list = copy.deepcopy(nodes)
        node = random.randint(0, size-1)
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

    # funkcja obliczajca koszt przejścia ścieżki
    def calculate_cost(self, nodes, path):
        cost = 0
        for i in range(1, len(path)):
            cost += nodes[path[i - 1]][path[i]]
        cost += nodes[path[len(nodes) - 1]][path[0]]
        return cost

    # funkcja podmienająca dwa wierzchołki w ścieżce
    def swap(self, node1, node2, path):
        path[node1], path[node2] = path[node2], path[node1]
        return path

    # funkcja znajdująca najlepsze sąsiedztwo
    def find_best_transformation(self, node, nodes):
        queue = PriorityQueue() # kolejka priorytetowa szeregująca wyniki według najnizszego kosztu
        size = len(nodes)
        for i in range(0, size-1):
            if i != node:
                transformed_path = copy.deepcopy(self.current_path)
                transformed_path = self.swap(node, i, transformed_path)# podmienienie wierzchołków w ścieżce
                transformed_cost = self.calculate_cost(nodes, transformed_path)
                queue.put((transformed_cost, transformed_path)) # umieszczenie rozwiązania w kolejce priorytetowej
        return queue.get() # zwrócenie najlepszego rozwiązania
