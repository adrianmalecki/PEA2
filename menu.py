import time
from read_data import Read_data
from sa import SimulatedAnnealing


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
            print('3. Wybór sąsiedztwa')
            print('4. Tabu Search')
            print('5. Ustaw współczynnik zmainy temperatury dla SW')
            print('6. Ustaw temperature')
            print('7. SW')
            print('8. Wyjście')

            self.choice = input('Wybór: ')

            if self.choice == '1':
                self.read_data.show_avaiable_files()
                #file_name = input("Podaj nazwe pliku: ")
                file_name = 'rbg403.atsp'
                try:
                    open(format(file_name), "r")
                    self.nodes = self.read_data.read_file(file_name)
                    print(self.nodes)
                except IOError:
                    print("Error!")

            elif self.choice == '2':
                self.max_time = int(input("Podaj czas: "))
            
            elif self.choice == '5':
                self.a = float(input("Podaj współczynnik schładzania: "))

            elif self.choice == '6':
                self.temperature = int(input("Podaj temperature początkową: "))

            elif self.choice == '7':
                self.sa = SimulatedAnnealing(self.temperature, self.a, self.max_time)
                best_path, best_sol, end_temp = self.sa.find_solution(self.nodes)
                print(best_path, best_sol, end_temp)
            elif self.choice == '8':
                exit()

            else:
                print("Wprowadz poprawną liczbę")


M = Menu()
M.main_menu()
