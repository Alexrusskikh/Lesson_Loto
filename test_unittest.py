import unittest
from pouch import Pouch
from cards import Card
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
    def test_init(self):
        card = Card()
        self.assertEqual(len(card.data), 15)
        self.assertEqual(len(card.rows_card), 3)
