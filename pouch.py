#import games
import random
"""модуль с классом Мешок, а в нем бочонки"""

class Pouch:
    """Мешок с бочонками"""

    def __init__(self):  # инициализация объекта  класса
        self.all_barrels = random.sample([i for i in range(1, 91)], 90)
        self.taken_barrels = []  # список извлеченных бочонков

    def __str__(self):
        return f'\nВсего в мешке бочонков: {len(self)}, извлекли: {90 - len(self)}, \n ' \
              f'список извлеченных: {self.taken_barrels}'


    def __len__(self):
        '''возвращает количество  бочонков  в мешке (уменьшается с каждым  ходом)'''
        return len(self.all_barrels)

    def take_barrel(self):
        """достать ОДИН бочонок из мешка, - 1 ход"""
        #take = games.ask_yes_no(question="Достать бочонок(y/n)?: ")
        #if (take == "y" or take == "н"):
        self.all_barrels = random.sample(self.all_barrels, len(self))#встряхнуть мешок
        new_barrel = self.all_barrels.pop()
        self.taken_barrels.append(new_barrel)
        print(f'\nВыпал Бочонок с номером:  *** {new_barrel} ***, осталось ходов:  {len(self)}')
        return new_barrel

if __name__ == "__main__":
    input("\n\nНажмите  Enter, чтобы выйти.")

