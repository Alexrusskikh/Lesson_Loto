#import games
import random
"""модуль с классом Мешок, а в нем бочонки"""

class Pouch:
    """Мешок с бочонками"""

    def __init__(self, remains=90, taken=0):  # инициализация объекта  класса
        self.remains = remains  # осталось в мешке, от 90 за  ход  уменьшается на 1
        self.taken = taken  # использованны, в начале  игры 0
        self.all_barrels = random.sample([i for i in range(1, 91)], 90)
        self.taken_barrels = []  # список извлеченных бочонков


    def __str__(self):
        rep = f'Всего в мешке бочонков: {len(self)}, извлекли: {self.taken}, \n ' \
              f'список извлеченных: {self.taken_barrels}'
        return rep

    def __len__(self):
        '''возвращает количество  бочонков  в мешке (уменьшается с каждым  ходом)'''
        return len(self.all_barrels)

    def take_barrel(self):
        """достать ОДИН бочонок из мешка, - 1 ход"""
        #take = games.ask_yes_no(question="Достать бочонок(y/n)?: ")
        #if (take == "y" or take == "н"):
        new_barrel = self.all_barrels.pop()

        #self.new_barrel = random.randint(1, 90)  # случайный номер от 1 до 90
        if new_barrel not in self.taken_barrels:
            self.taken_barrels.append(new_barrel)
            self.remains -= 1  # уменьшает количество бочонков  в мешке на 1
            self.taken += 1  # увеличивает количество бочонков  на  столе на 1
            print(f'\nВыпал Бочонок с номером:  *** {new_barrel} ***, осталось ходов: {self.remains}')
            return new_barrel



# if __name__ == "__main__":
#     input("\n\nНажмите  Enter, чтобы выйти.")

pouch = Pouch()
print(pouch)
print(len(pouch))
pouch.take_barrel()
print(len(pouch))