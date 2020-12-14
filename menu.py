import time
from read_data import Read_data
from sa import SimulatedAnnealing
from ts import TabuSearch



class Menu:
    def __init__(self):
        self.read_data = Read_data()
        self.nodes = []
        self.choice = 0
        self.max_time = 0
        self.a = 0
        self.temperature = 0

    def main_menu(self):
        while self.choice != 6:
            print('_________MENU_________')
            print('1. Wczytaj dane')
            print('2. Wprowadz kryterium stopu(czas w sekundach)')
            print('3. Tabu Search')
            print('4. Ustaw współczynnik zmainy temperatury dla SW')
            print('5. Ustaw temperature')
            print('6. SW')
            print('7. Wyjście')

            self.choice = input('Wybór: ')

            if self.choice == '1':
                self.read_data.show_avaiable_files()
                file_name = input("Podaj nazwe pliku: ")
                #file_name = 'ftv170.atsp'
                try:
                    open(format(file_name), "r")
                    self.nodes = self.read_data.read_file(file_name)
                    print(self.nodes)
                except IOError:
                    print("Error!")

            elif self.choice == '2':
                self.max_time = int(input("Podaj czas: "))

            elif self.choice == '3':
                self.tabu_search = TabuSearch(self.nodes,self.max_time)
                best_path, best_sol,find_time = self.tabu_search.find_solution()
                print('Ścieżka: ', best_path)
                print('Koszt: ',  best_sol)
                print('Czas: ', find_time)

            elif self.choice == '4':
                self.a = float(input("Podaj współczynnik schładzania: "))

            elif self.choice == '5':
                self.temperature = int(input("Podaj temperature początkową: "))

            elif self.choice == '6':
                self.sa = SimulatedAnnealing(self.temperature, self.a, self.max_time)
                best_path, best_sol, end_temp, find_time = self.sa.find_solution(self.nodes)
                print('Ścieżka: ', best_path)
                print('Koszt: ', best_sol)
                print('Temperatura koncowa: ', end_temp)
                print('Czas: ', find_time)
            elif self.choice == '7':
                exit()

            else:
                print("Wprowadz poprawną liczbę")


M = Menu()
M.main_menu()
