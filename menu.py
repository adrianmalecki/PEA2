import time
from read_data import Read_data
from sa import SimulatedAnnealing


class Menu:
    def __init__(self):
        self.read_data = Read_data()
        self.sa = SimulatedAnnealing()
        self.nodes = []
        self.choice = 0

    def main_menu(self):
        while self.choice != 6:
            print('_________MENU_________')
            print('1. Wczytaj dane')
            print('2. Wprowadz kryterium stopu')
            print('3. Wybór sąsiedztwa')
            print('4. Tabu Search')
            print('5. Ustaw współczynnik zmainy temperatury dla SW')
            print('6. SW')
            print('7. Wyjście')

            self.choice = input('Wybór: ')

            if self.choice == '1':
                self.read_data.show_avaiable_files()
                #file_name = input("Podaj nazwe pliku: ")
                file_name = 'ftv10.atsp'
                try:
                    open(format(file_name), "r")
                    self.nodes = self.read_data.read_file(file_name)
                    print(self.nodes)
                except IOError:
                    print("Error!")

            elif self.choice == '6':
                self.sa.find_solution(self.nodes)

            elif self.choice == '7':
                exit()

            else:
                print("Wprowadz poprawną liczbę")


M = Menu()
M.main_menu()
