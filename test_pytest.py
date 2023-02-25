""" Тесты к игре лото"""
import random
from pouch import Pouch
from loto import Loto_Hand, Loto_Game, Loto_Player
from cards import Card, Hand, Deck
import copy
import pytest


class TestPouch:

    def setup_class(self):
        """ настройка любых состояний, специфичных для выполнения этого класса (который
         содержит тесты).
        """
        print("\nИнициализация объекта класса")
        self.pouch = Pouch()

    def teardown_class(self):
        """ очистка любых состояний, настроенных ранее с помощью метода
            setup_class.
        """
        print("\nКонец")


    def test_init(self):
        """начальное состояние  мешка"""
        #pouch = Pouch(remains=90, taken=0)
        assert self.pouch.remains == 90
        assert self.pouch.taken == 0
        assert len(self.pouch.taken_barrels) == 0
        assert len(self.pouch.new_barrels) == 90
        assert max(self.pouch.new_barrels) == 90
        assert min(self.pouch.new_barrels) == 1


    def test_take_barrel(self):
        """ изменение состояния мешка  после извлечения бочонка"""
        self.pouch.take_barrel()
        assert self.pouch.remains != 90
        assert self.pouch.taken != 0
        assert len(self.pouch.taken_barrels) != 0
        assert len(self.pouch.new_barrels) != 90


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

    def setup_class(self):
        """ настройка любых состояний, специфичных для выполнения этого класса (который
         содержит тесты).
        """
        print("\nИнициализация объекта класса")
        self.card = Card()

    def teardown_class(self):
        """ очистка любых состояний, настроенных ранее с помощью метода
            setup_class.
        """
        print("\nКонец")


    def test_init(self):

        assert len(self.card.data) == 15
        assert len(self.card.rows_card) == 3

    def test_replacement(self):#замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на * """

        new_barrel = random.choice(self.card.data)
        self.card.replacement(self.card, new_barrel)
        assert [i for i in self.card.data if i == '*'] ==['*']
        assert any([True for i in self.card.data if i == '*']) == True
        assert any("*" in sl for sl in self.card.rows_card) == True

    def test_closed_row(self) -> bool:
        """проверяет  ряд карточки на завершенность"""
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " ", " "]
        assert self.card.closed_row(item) == True

    def test_replacement_row(self):
        """заменяет ряд карточки на собачек"""

        item = [" ", "*", " ", " ", " ", " ", "*", " ", " "]
        assert len(self.card.replacement_row(item)) == 9
        assert set(self.card.replacement_row(item)) == {"@"}


    def test_row_analisis(self):
        """
        возвращает номер закрытого ряда в карточке и заменяет  его @@@@@@@@@
        :param row: порядковый номер горизонтального ряда
        :param item: его содержимое, например [" ", " ", "*", "*", " "]
        :return: номер закрытого ряда в карточке - 1,2,3
        """

        row = 0
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " "]
        assert (self.card.row_analisis(row, item)) == 1

class TestHand:

    def setup_class(self):
        """ настройка любых состояний, специфичных для выполнения этого класса (который
         содержит тесты).
        """
        print("\nИнициализация объекта класса")
        self.hand = Hand()
        self.card = Card()

    def teardown_class(self):
        """ очистка любых состояний, настроенных ранее с помощью метода
            setup_class.
        """
        print("\nКонец")

    def test_init(self):
        assert self.hand.cards == []

    def test_have_num(self):
        """"  в каждой  карте игрока ищет в card.data вхождение new_barrel """
        self.hand.cards.append(self.card)
        new_barrel = random.choice(self.card.data)
        assert(self.hand.have_num(self.hand.cards, new_barrel)) == True

    def test_clear(self):
        """удаление карт из колоды/у игрока"""

        self.hand.cards.append(self.card)
        self.hand.clear()
        assert self.hand.cards == []

    def test_add(self):
        """добавляет карту к списку self.cards"""
        self.hand.add(self.card)
        assert self.hand.cards != []

    def test_give(self):
        """"передача карты в руки (в колоду)"""
        self.hand.add(self.card)
        hand1 = Hand()
        self.hand.give(self.card, hand1)
        assert hand1.cards != []

class TestDeck:

    def setup_class(self):
        """ настройка любых состояний, специфичных для выполнения этого класса (который
         содержит тесты).
        """
        print("\nИнициализация объекта класса")
        self.deck = Deck()

    def teardown_class(self):
        """ очистка любых состояний, настроенных ранее с помощью метода
            setup_class.
        """
        print("\nКонец")


    def test_populate(self):
        """заполнение  колоды картами, их  24 в лото"""

        self.deck.populate()
        assert len(self.deck.cards) == 24

    def test_shuffle(self):
        """перемешивание колоды"""

        self.deck.populate()
        old = copy.deepcopy(self.deck.cards)
        self.deck.shuffle()
        new = self.deck.cards
        assert new != old

    def test_deal(self):
        """передача карт игроку из колоды"""

        self.deck.populate()
        hand = Hand()
        per_hand = 2
        self.deck.deal(hand, per_hand)
        assert len(hand.cards) == 2

class TestLoto_Deck:

    def test_populate(self):
        """заполнение  колоды картами, их  24 в лото"""
        deck = Deck()
        deck.populate()
        assert len(deck.cards) == 24

class TestLoto_Hand:

    def test_init(self):
        loto_hand = Loto_Hand('Max', credit=0, winning=0, loss=0)
        assert loto_hand.name == 'Max'
        assert loto_hand.credit == 0
        assert loto_hand.winning == 0
        assert loto_hand.loss == 0

class TestLoto_Game:

    def test_init(self):
        players = []
        loto_game = Loto_Game(players)
        assert loto_game.bank == 0  # банк отдельной игры
        assert len(loto_game.players) == 0
        assert len(loto_game.deck.cards) == 24
        assert loto_game.pouch.remains == 90








