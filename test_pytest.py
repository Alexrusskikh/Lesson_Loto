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

    def test_replacement(self):#замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на * """
        card = Card()  # начальное состояние карты
        new_barrel = random.choice(card.data)
        card.replacement(card, new_barrel)
        assert [i for i in card.data if i == '*'] ==['*']
        assert any([True for i in card.data if i == '*']) == True
        assert any("*" in sl for sl in card.rows_card) == True

    def test_closed_row(self) -> bool:#проверяет  ряд карточки на завершенность...
        card = Card()
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " ", " "]
        assert card.closed_row(item) == True

    def test_replacement_row(self):#заменяет ряд карточки на собачек
        card = Card()
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " "]
        assert len(card.replacement_row(item)) == 9
        assert set(card.replacement_row(item)) == {"@"}


    def test_row_analisis(self):
        """
        возвращает номер закрытого ряда в карточке и заменяет  его @@@@@@@@@
        :param row: порядковый номер горизонтального ряда
        :param item: его содержимое, например [" ", " ", "*", "*", " "]
        :return: номер закрытого ряда в карточке - 1,2,3
        """
        card = Card()
        row = 0
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " "]
        assert (card.row_analisis(row, item)) == 1

class TestHand:

    def test_init(self):
        hand = Hand()
        assert hand.cards == []

    def test_have_num(self):
        """"  в каждой  карте игрока ищет в card.data вхождение new_barrel """
        hand = Hand()
        card = Card()
        hand.cards.append(card)
        new_barrel = random.choice(card.data)
        assert(hand.have_num(hand.cards, new_barrel)) == True


    def test_clear(self):
        hand = Hand()
        card = Card()
        hand.cards.append(card)
        hand.clear()
        assert hand.cards == []

    def test_add(self):
        hand = Hand()
        card = Card()
        hand.add(card)
        """добавляет карту к списку self.cards"""
        assert hand.cards != []

    def give(self):
        """"передача карты в руки (в колоду)"""
        hand = Hand()
        card = Card()
        hand.add(card)
        hand1 = Hand()
        hand.give(card, hand1)
        assert hand1.cards != []


