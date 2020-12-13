from os import scandir
import copy
import re


class Read_data:

    def show_avaiable_files(self):
        for file in scandir():
            if file.name[-5:] == ".atsp":
                print(file.name)


    def read_file(self, file_name):
        nodes = []
        row = []
        full_list = []
        with open(format(file_name), mode='r') as file:
            data = file.readlines()
        for i in data:
            number_list = re.findall(r'\d+', i)
            for i in number_list:
                full_list.append(int(i))
        full_list.pop(0)
        size = full_list.pop(0)
        for position, i in enumerate(full_list):
            if position % size != 0:
                row.append(int(i))
            else:
                nodes.append(row)
                row = []
                row.append(int(i))
        nodes.append(row)
        nodes.pop(0)
        return nodes


