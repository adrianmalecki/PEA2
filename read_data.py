import os
from os import scandir
import copy
import re


class Read_data:

    def show_avaiable_files(self):
        for file in scandir():
            if file.name[-5:] == ".atsp":
                print(file.name)

    def try_open_file(self, file_name):
        try:
            open(format(file_name), "r")
            return 1
        except IOError:
            return 0

    def read_file(self, file_name):
        nodes = []
        help_list = []
        full_list = []
        with open(format(file_name), mode='r') as file:
            data = file.readlines()
        for i in data:
            if len(re.findall(r'\d+', i)) != 0:
                number_list = re.findall(r'\d+', i)
                for i in number_list:
                    full_list.append(int(i))

        full_list.pop(0)
        size = full_list.pop(0)

        for position, i in enumerate(full_list):
            if position % size != 0:
                help_list.append(int(i))
            else:
                nodes.append(help_list)
                help_list = []
                help_list.append(int(i))
        nodes.append(help_list)
        nodes.pop(0)
        self.weights = copy.deepcopy(nodes)
        self.file_name = file_name
        return nodes

    def get_data(self):
        file_name = input("Podaj nazwe pliku: ")

        if self.try_open_file(file_name) == 1:
            print("Sukces!\n")
            weights = self.read_weights(file_name)
            return weights

        else:
            print("Niestety nie ma takiego pliku!")


