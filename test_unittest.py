import unittest, random, copy
from pouch import Pouch
from cards import Card, Hand, Deck
from loto import Loto_Hand, Loto_Game

class TestPouch(unittest.TestCase):
    def setUp(self):
        self.pouch = Pouch()


    def test_init(self):
        self.assertEqual(self.pouch.remains, 90)
        self.assertEqual(self.pouch.taken, 0)
        self.assertEqual(self.pouch.taken_barrels, [])
        self.assertEqual(len(self.pouch.new_barrels), 90)
        self.assertEqual(max(self.pouch.new_barrels), 90)
        self.assertEqual(min(self.pouch.new_barrels), 1)

    def test_take_barrel(self):
        self.pouch.take_barrel()
        self.assertNotEqual(self.pouch.remains, 90)
        self.assertNotEqual(self.pouch.taken, 0)
        self.assertNotEqual(len(self.pouch.taken_barrels), 0)
        self.assertNotEqual(len(self.pouch.new_barrels), 90)


class QuestionTestCase(unittest.TestCase):
    """Тесты для функций вопросов"""

    def test_ask_yes_no(self, question="question"):
        """Задает  вопрос  с ответом 'да' или 'нет'."""
        response = "y"
        while response not in ("y", "n", "н", "т"):
            response = input(question).lower()
        self.assertEqual(response, "y")

        response = "n"
        while response not in ("y", "n", "н", "т"):
            response = input(question).lower()
        self.assertEqual(response, "n")

        response = "н"
        while response not in ("y", "n", "н", "т"):
            response = input(question).lower()
        self.assertEqual(response, "н")

        response = "т"
        while response not in ("y", "n", "н", "т"):
            response = input(question).lower()
        self.assertEqual(response, "т")

    def test_ask_number(self, question='question', low=1, high=3):
        """просит ввести  число  из  заданного диапазона."""

        response = 2
        while response not in range(low, high):
            response = int(input(question))
        self.assertEqual(response, 2)

        with self.assertRaises(Exception):
            response = 2
            while response not in range(low, high):
                response = int(input(question))
            self.assertEqual(response, 3)

class TestCards(unittest.TestCase):

    def setUp(self):
        self.card = Card()

    def test_init(self):
        self.assertEqual(len(self.card.data), 15)
        self.assertEqual(len(self.card.rows_card), 3)

    def test_replacement_rows(self):  # замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на *  в rows_card """
        new_barrel = random.choice(self.card.data)
        self.card.replacement(self.card, new_barrel)

        self.assertTrue(any("*" in sl for sl in self.card.rows_card))

    def test_replacement_data(self):#замена числа на "*" в self.rows_card, а так  же в self.data
        """ замена выпавшего числа на * card.data"""
        new_barrel = random.choice(self.card.data)
        self.card.replacement(self.card, new_barrel)

        self.assertEqual([i for i in self.card.data if i == '*'], ['*'])
        self.assertTrue(any(True for i in self.card.data if i == '*'))


    def test_closed_row(self):
        """проверяет  ряд карточки на завершенность"""
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " ", " "]
        self.assertTrue(self.card.closed_row(item))

    def test_replacement_row(self):#заменяет ряд карточки на собачек
        card = Card()
        item = [" ", "*", " ", " ", " ", " ", "*", " ", " "]
        self.assertEqual(len(card.replacement_row(item)), 9)
        self.assertEqual(set(card.replacement_row(item)), {"@"})

class TestHend(unittest.TestCase):

    def setUp(self):
        self.hand = Hand()

    def test_init(self):
        self.assertEqual(self.hand.cards, [])

    def test_have_num(self):
        """"  в каждой  карте игрока ищет в card.data вхождение new_barrel """
        card = Card()
        self.hand.cards.append(card)
        new_barrel = random.choice(card.data)
        self.assertTrue(self.hand.have_num(self.hand.cards, new_barrel))

    def test_clear(self):
        card = Card()
        self.hand.cards.append(card)
        self.hand.clear()
        self.assertEqual(self.hand.cards, [])

    def test_add(self):
        card = Card()
        self.hand.add(card)
        """добавляет карту к списку self.cards"""
        self.assertNotEqual(self.hand.cards, [])

    def test_give(self):
        """"передача карты в руки (в колоду)"""
        card = Card()
        self.hand.add(card)
        hand1 = Hand()
        self.hand.give(card, hand1)
        self.assertNotEqual(hand1.cards, [])

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
    def test_populate(self):
        """формирование колоды  из 24 карт"""

        self.deck.populate()
        self.assertEqual(len(self.deck.cards), 24)

    def test_shuffle(self):
        """перемешивание колоды"""

        self.deck.populate()
        old = copy.deepcopy(self.deck.cards)
        self.deck.shuffle()
        new = self.deck.cards
        self.assertNotEqual(new, old)

    def test_deal(self):
        """передача карт игроку из колоды"""

        self.deck.populate()
        hand = Hand()
        per_hand = 2
        self.deck.deal(hand, per_hand)
        self.assertEqual(len(hand.cards), 2)

class TestLoto_Deck(unittest.TestCase):

    def test_populate(self):
        """заполнение  колоды картами, их  24 в лото"""
        deck = Deck()
        deck.populate()
        self.assertEqual(len(deck.cards), 24)

class TestLoto_Hand(unittest.TestCase):

    def test_init(self):
        loto_hand = Loto_Hand('Max', credit=0, winning=0, loss=0)
        self.assertEqual(loto_hand.name, 'Max')
        self.assertEqual(loto_hand.credit, 0)
        self.assertEqual(loto_hand.winning, 0)
        self.assertEqual(loto_hand.loss, 0)

class TestLoto_Game(unittest.TestCase):

    def test_init(self):
        players = []
        loto_game = Loto_Game(players)
        self.assertEqual(loto_game.bank, 0)
        self.assertEqual(len(loto_game.players), 0)
        self.assertEqual(len(loto_game.deck.cards), 24)
        self.assertEqual(loto_game.pouch.remains, 90)










