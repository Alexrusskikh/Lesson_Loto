""""это модуль с карточками, их колодой"""

import random
from tabulate import tabulate

class Card():
    """Одна игральная карта для игры в Лото.  Создание 15 случайных чисел карточки лото.
    Первый столбец - от 1 до 9, второй от 10 до 19, и т.д, последний столбец - от 80 до 90 включительно.
    :return: Возвращает "правильный" ряд чисел карточки лото"""
    #атрибуты  класса Card
    __emptynum = " "
    __crossednum = "*"
    __crossedrow = "@"
    # data = None
    # rows_card = None
    num = 0

    def __init__(self):
        self.num += 1
        Card.num += 1
        row_1 = []
        row_2 = []
        # случайные  цифры первого столбца
        column1 = random.sample(range(1, 10), 2)  # из выборки от 1 до 9 получаем 2 числа, (в виде списка)
        # записываем  по  индексу в row_1 и row_2
        row_1.append(column1[0])
        row_2.append(column1[1])

        # выбор столбцов со 2 по 8
        for i in range(1, 8):
            too_num = random.sample(range(i * 10, (i * 10) + 10), 2)  # из выборки от 1 до последнего числа десятка
            # получаем 2 числа, а затем записываем  по  индексу в row_1 и row_2
            row_1.append(too_num[0])
            row_2.append(too_num[1])

        # случайные  цифры 9 столбца, включая 90
        column9 = random.sample(range(80, 91), 2)  # из выборки от 80 до 90 берем 2 числа, получаем список
        # записываем  по  индексу в row_1 и row_2
        row_1.append(column9[0])
        row_2.append(column9[1])

        # список row_1 оставляем без изменений, редуцируем row_2 до 6 чисел (чтобы потом получить не 18 чисел, а 15)
        num_6 = random.sample(row_2, 6)

        # объединяем row_1 и row_2, получаем 15 случайных чисел по порядку
        data = row_1 + num_6
        self.data = sorted(data)

        col1_8 = []  # объединяем  числа  по столбцам(соответственно  десятков) добавляя пробелы
        for col in range(1, 9):
            coln = list(
                filter(lambda i: ((col - 1) * 10) <= i <= (((col - 1) * 10) + 9), data))  # фильтр  по  десяткам
            # print(coln)
            while len(coln) < 3:  # пока ряд меньше 3 цифр, добавляет пробелы
                coln[len(coln):] = self.__emptynum
                random.shuffle(coln)
            col1_8.append(coln)
        # print("col1_8",col1_8)

        col9 = []  # объединяем числа по столбцам(соответственно десятков) добавляя пробелы
        coln = list(filter(lambda i: 80 <= i < 91, data))  # фильтр  по  десяткам
        # print(coln)
        while len(coln) < 3:  # пока ряд меньше 3 цифр, добавляет пробелы
            coln[len(coln):] = self.__emptynum
            random.shuffle(coln)
        col9.append(coln)
        # print("col9", col9)
        num_list = col1_8 + col9  # cписок  списков  по столбцам
        # print(num_list)

        # строки для карточки, т.к. модуль tabulate не выводит по столбцам
        row1_card = []
        row2_card = []
        row3_card = []
        # создание строк для карточки из столбцов
        for el in num_list:
            row1_card.append(el[0])
            row2_card.append(el[1])
            row3_card.append(el[2])
        # print(row1_card)
        # print(row2_card)
        # print(row3_card)
        # print(tabulate([row1_card, row2_card, row3_card], tablefmt='double_grid'))
        self.rows_card = [row1_card, row2_card, row3_card]

        # print(self.data)
        # print(self.rows_card)

    def __str__(self):
        rep = f"Карта №: {self.num}\n" \
              f"{tabulate([self.rows_card[0], self.rows_card[1], self.rows_card[2]], tablefmt='double_grid')}"
        # print(self.num)
        # print(self.data)
        # print(self.rows_card)
        return rep

    def visualization(self):
        """" просто принтует карту """
        print(tabulate([self.rows_card[0], self.rows_card[1], self.rows_card[2]], tablefmt='double_grid'))


    def replacement(self, card, new_barrel):#замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на * """
        if new_barrel in card.data:
            print ("Есть такая цифра!")
            for index, item in enumerate(self.data):# в списке чисел карты ищем число
                if item == new_barrel:
                    self.data[index] = self.__crossednum  # ставим фишку
            for row in self.rows_card:# перебираем строки карточки
                for index, item in enumerate(row):#в каждой  строке ищем число
                    if item == new_barrel:
                        row[index] = self.__crossednum  # ставим фишку

        else:
            print(f"На Вашей карте нет такого числа: {new_barrel}\n"
                  f"****** Вы проиграли!!! ******")



    def closed_row(self, item) -> bool:#проверяет  ряд карточки на завершенность...
        return set(item) == {self.__emptynum, self.__crossednum}

    def replacement_row(self, item):
        for index, num in enumerate(item):
            item[index] = self.__crossedrow
        return item

    def row_analisis(self, row, item):
        """
        возвращает номер закрытого ряда в карточке и заменяет  его @@@@@@@@@
        :param row: порядковый номер горизонтального ряда
        :param item: его содержимое, например [" ", " ", "*", "*", " "]
        :return: номер закрытого ряда в карточке - 1,2,3
        """
        number_row = 0
        if row == 0 and self.closed_row(item) == True:
            number_row += 1
            # print(f"Вы закончили на {numbers} ряд, все кроме Вас повышают ставку...")
            self.replacement_row(item)
        elif row == 1 and self.closed_row(item) == True:
            # print(f"Вы закончили на {numbers} ряд, заберите половину  банка, все кроме Вас повышают  ставку...")
            number_row += 2
            self.replacement_row(item)
        elif row == 2 and self.closed_row(item) == True:
            # print(f"Вы закончили на {numbers} ряд, заберите весь  банка, игра закончена")
            number_row += 3
            self.replacement_row(item)
        return number_row

    def closed_card(self):
        """
        перебор рядов карточки
        """
        row_finish = 0
        for row, item in enumerate(self.rows_card):  # перебираем  ряды  одной карты, получаем row, item
            x = self.row_analisis(row, item)# возвращает параметры всех рядов, открытые 0, № закрытых и заменяет  на @@@@
            row_finish += x
        # if row_finish != 0:
        #     print(f"Вы закончили  на {row_finish} ряд")
        return row_finish


class Hand():
    """ Набор карт на руках у одного игрока. """
    def __init__(self):
        self.cards = []
    def __str__(self):
        if self.cards:
            rep = f"Карты игрока:\n"
            for card in self.cards:
                 rep += f"{card}\n"
        else:
            rep = "Нет карт на  руках..."
        return rep

    def have_num(self, cards, new_barrel):
        """"  в каждой  карте игрока ищет в card.data вхождение new_barrel """
        new_row = []
        for card in cards:
            if new_barrel in card.data:
                new_row.append(card.data)
        return any(new_barrel in el for el in new_row)


    def clear(self):
        """удаляет все карты из списка self.cards - на руках пусто, и  колоду  очистит,
        не  знаю, надо  ли.... """
        self.cards = []

    def add(self, card):
        """добавляет карту к списку self.cards"""
        self.cards.append(card)

    def give(self, card, hand):
        """"передача карты в руки (в колоду)"""
        self.cards.remove(card)
        hand.add(card)#раздача карт



class Deck(Hand):
    """создание класса Колода через наследование класса Hand"""

    def populate(self): #заполнение  колоды картами, их  24 в лото
        for num in range(1, 25):
            card = Card()
            # print(f'Карта №: {card.num}')
            # print(f'card.data: {card.data}')
            # print(f'card.rows_card: {card.rows_card}')
            # print(card)
            self.add(card)

    def shuffle(self):#перемешивание колоды
        random.shuffle(self.cards)

    def deal(self, hand, per_hand):#передача карт игроку из колоды,
        for el in range(per_hand):
            if self.cards:
                card = random.choice(self.cards)
                self.give(card, hand)
                # print(f'Карта №: {card.num}')
                # print(f'card.data: {card.data}')
                # print(f'card.rows_card: {card.rows_card}')
                #print(card)
            else:
                print("В колоде кончились карты....")

if __name__=="__main__":
    input("\n\nНажмите  Enter, чтобы выйти.")
