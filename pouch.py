import games
import random

"""модуль с классом Мешок, а в нем бочонки"""


class Pouch:
    """Мешок с бочонками"""

    def __init__(self, remains=90, taken=0):  # инициализация объекта  класса
        self.remains = remains  # осталось в мешке, от 90 за  ход  уменьшается на 1
        self.taken = taken  # использованны в начале  игры 0
        self.taken_barrels = []  # список извлеченных бочонков
        self.new_barrel = None
    def __str__(self):
        rep = f'Всего в мешке бочонков: {self.remains}, извлекли: {self.taken}, \n ' \
              f'список извлеченных: {self.taken_barrels}'
        return rep

    def can_move(self):
        ''' проверяет возможность хода - есть ли бочонки в мешке, в лото в этом нет необходимости, все равно
         кто то выиграет
        :return: True-False
        '''
        return self.remains > 0

    def take_barrel(self):
        """достать ОДИН бочонок из мешка, - 1 ход"""
        #take = games.ask_yes_no(question="Достать бочонок(y/n)?: ")
        #if (take == "y" or take == "н"):
        self.new_barrel = random.randint(1, 90)  # случайный номер от 1 до 90
        if self.new_barrel not in self.taken_barrels:
            self.taken_barrels.append(self.new_barrel)
            self.remains -= 1  # уменьшает количество бочонков  в мешке на 1
            self.taken += 1  # увеличивает количество бочонков  на  столе на 1
            print(f'\nВыпал Бочонок с номером:  *** {self.new_barrel} ***, осталось ходов: {self.remains}')
            return self.new_barrel


if __name__ == "__main__":
    input("\n\nНажмите  Enter, чтобы выйти.")


