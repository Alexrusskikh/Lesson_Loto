""" Тесты к игре лото"""
import random
import pytest
from pouch import Pouch
import games
from cards import Card, Hand
#к модулю Pouch
class TestPouch:
    def test_init(self):#начальное состояние  мешка
        pouch = Pouch(remains=90, taken=0)
        assert pouch.remains == 90
        assert pouch.taken == 0
        assert len(pouch.taken_barrels) == 0
        assert len(pouch.new_barrels) == 90
        assert max(pouch.new_barrels) == 90
        assert min(pouch.new_barrels) == 1


    def test_take_barrel(self):#изменение состояния мешка  после извлечения бочонка
        pouch = Pouch(remains=90, taken=0)
        pouch.take_barrel()
        assert pouch.remains != 90
        assert pouch.taken != 0
        assert len(pouch.taken_barrels) != 0
        assert len(pouch.new_barrels) != 90


def test_ask_yes_no(question = "question"):
    """Задает  вопрос  с ответом 'да' или 'нет'."""
    response = "y"
    while response not in ("y", "n", "н", "т"):
        response = input(question).lower()
    assert response == "y"

def test_ask_number(question = 'question', low=1, high=3):
    """просит ввести  число  из  заданного диапазона."""
    response = 2
    while response not in range(low, high):
        response = int(input(question))
    assert response == 2

class TestCards:
    def test_init(self):
        card = Card()#начальное состояние карты
        assert len(card.data) == 15
        assert len(card.rows_card) == 3

    def test_replacement_data(self):#замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на * """
        card = Card()  # начальное состояние карты
        new_barrel = random.sample(card.data, 1)
        for index, item in enumerate(card.data):  # в списке чисел карты ищем число
            if item == new_barrel:
                card.data[index] = "*"  # ставим фишку
                assert "*" in card.data == True

    def test_replacement_rows(self):  # замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на * """
        card = Card()  # начальное состояние карты
        new_barrel = random.sample(card.data, 1)
        for row in card.rows_card:# перебираем строки карточки
            for index, item in enumerate(row):#в каждой  строке ищем число
                if item == new_barrel:
                    row[index] = "*" # ставим фишку
                    assert any("*" in sl for sl in card.rows_card) == True

    def test_closed_row(self) -> bool:#проверяет  ряд карточки на завершенность...
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " ", " "]
        assert set(item) == {" ", "*"}

    def test_replacement_row(self):#заменяет ряд карточки на собачек
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " ", " "]
        for index, num in enumerate(item):
            item[index] = "@"
        assert set(item) == {"@"}

class TestHand:
    def test_init(self):
        hand = Hand()
        assert hand.cards == []

    def test_have_num(self):
        """"  в каждой  карте игрока ищет в card.data вхождение new_barrel """
        cards = []
        card = Card()  # начальное состояние карты
        cards.append(card)
        new_barrel = random.sample(card.data, 1)
        new_row = []

        for card in cards:
            if new_barrel not in card.data:
                new_row.append(card.data)
        assert len(new_row) != 0

    def test_clear(self):
        hand = Hand()
        hand.clear()
        assert hand.cards == []

    def test_add(self):
        card = Card()
        hand = Hand()
        hand.add(card)
        """добавляет карту к списку self.cards"""
        assert hand.cards != []



