"""Игра Лото"""

""""на основе модулей cards, games, pouch"""
import cards, games, pouch
from tabulate import tabulate
class Loto_Pouch(pouch.Pouch):
    """Мешок для  игры Loto"""

class Loto_Card(cards.Card):
    """ Карта для игры в Loto"""

class Loto_Deck(cards.Deck):
    """ Колода для игры в Loto"""
    def populate(self): #заполнение  колоды картами, их  24 в лото
        for num in range(1, 25):
            card = Loto_Card()
            self.add(card)

class Loto_Hand(cards.Hand):
    """Набор карт для игры в Loto у одного игрока"""
    def __init__(self, name, credit=0, winning=0, loss=0): #добавляет атрибутов игрока name
        super(Loto_Hand, self).__init__()
        self.name = name
        self.credit = credit
        self.winning = winning
        self.loss = loss

    def __str__(self):
        if self.cards:
            rep = f"Карты игрока: {self.name}\n"
            for card in self.cards:
                 rep += f"{card}\n"
        else:
            rep = "Пусто"
        return rep


class Loto_Player(Loto_Hand):
    """ Игрок в Loto"""
    def take_card(self):
        response = games.ask_yes_no("\n" + self.name + ", будете брать еще одну карту? (Y/N): ")
        return response == "y" or response == "н"

    def replacement_card(self):
        """вопрос в конце раунда """
        response = games.ask_yes_no("\n" + self.name + ", заменить карту? (Y/N): ")
        return response == "y" or response == "н"

    def replacement_number(self, new_barrel):
        """вопрос в конце раунда """
        response = games.ask_yes_no("\n" + self.name + f", закрыть цифру {new_barrel} фишкой? (Y/N): ")
        return  response == "y" or response == "н"

    def mistake(self):
        print(f"\n!!!!!! Игрок {self.name} допустил ошибку!!!!!!")
        self.lose()

    def lose(self):
        print(f"!!!!!! Игрок {self.name} проиграл...!!!!!!\n"
              f"!!!!!! Игрок {self.name} выбывает из игры...!!!!!\n")


    def win(self):
        print(f"\nИгрок {self.name} выиграл...!!!!!!\n"
              f"\n!!!!!Весь банк достается игроку {self.name} !!!!! ")



class Loto_Dealer(Loto_Hand):
    """Дилер в игре Loto, задает вопросы и кричит бочонки, манипулирует колодой, пока недоделал.... """

class Loto_Game():
    """Отдельная игра Loto, внутри будут раунды проверки наличия выпавшего бочонка..."""
    def __init__(self, players):
        self.players = players
        self.dealer = Loto_Dealer("Dealer")
        self.pouch = Loto_Pouch()
        self.deck = Loto_Deck()
        self.deck.populate()
        self.deck.shuffle()
        self.bank = 0  # банк отдельной игры
        print(f"\n!!!! Банк игры пока  {self.bank} УЕ!!!!")
        for player in self.players:
            player.cards.clear()

            while True:
                try:
                    per_hand = int(input(f"{player.name}, введите количество карт, на которых будете играть: "))
                    break
                except:
                    print("Попробуйте ввести число")

            self.deck.deal(player, per_hand)
            #делаем ставку по 1УЕ с карты автоматически
            #bet = int(input(f"{player.name}, сделайте ставку в игре:  ")), можно сделать произвольную ставку.
            player.credit -= per_hand
            player.loss -= per_hand
            self.bank += per_hand
            print(player)

        print(f"!!!!! Банк игры составил: {self.bank} УЕ! Эти  ДЕНЬГИ  могут  оказаться вашими!!!!!")
        print()

    def participant(self, leave_players):
        """ принтует  оставшихся в раунде послек  ошибки  одного из  игроков"""
        print("\t\t************ В игре Лото участвуют игроки ************:")
        col = 1
        for player in self.players:
            if player not in leave_players:
                print(f'{col}. {player.name}, кредит {player.credit}')
                col += 1

    def winner_one(self, winner, leave_players):
        if (len(self.players) - len(leave_players)) != 1:
            self.participant(leave_players)  # печатаем участников
        elif (len(self.players) - len(leave_players)) == 1:
            for player in self.players:
                if player not in leave_players:
                    player.win()
                    player.credit += self.bank
                    player.winning += self.bank
                    self.bank -= self.bank
                    print(f"!!!!! Банк игры опустел..... !!!!!!")
                    winner += 1# и надо  остановить выброс  бочонков
        return winner


    def finish_top(self, current_name):
        print(f"\nИгрок {current_name} закончил на верхний ряд...\n"
              f"Все отдают в банк по 1 УЕ с каждой карты, кроме игрока: {current_name} "
              f"Продолжаем.....")
        for player in self.players:
            if player.name != current_name:
                self.bank += 1
                player.credit -= 1
                player.loss -= 1
                print(f"!!!!! Банк игры составил: {self.bank} УЕ! "
                      f"Эти  ДЕНЬГИ  могут  оказаться вашими!!!!!")


    def finish_middle(self, current_name):
        print(f"\nИгрок {current_name} закончил на середний ряд и  забирает половину банка...\n"
              f" Остальные добавляют по 1 УЕ с каждой карты ")
        for player in self.players:
            if player.name != current_name:
                self.bank += 1
                player.credit -= 1
                player.loss -= 1
            if player.name == current_name:
                self.bank -= self.bank / 2
                player.credit += self.bank / 2
                player.winning += self.bank / 2
                print(f"!!!!! Банк игры составил: {self.bank} УЕ! "
                      f"Эти  ДЕНЬГИ  могут  оказаться вашими!!!!!"
                      f"Продолжаем.....")


    def finish_bottom(self, current_name):
        print(f"\nИгрок {current_name} закончил на нижний ряд и забирает ВСЕ...\n")
        for player in self.players:
            if player.name == current_name:
                player.credit += self.bank
                player.winning += self.bank
                self.bank -= self.bank
                print(f"!!!!! Банк игры опустел.....!!!!!! ")


    def play_round(self):
        leave_players = []#если кто то совершил  ошибку, записывается в список и выбывает до конца раунда
        participants_round = []
        winner = 0
        while winner == 0:
            """пока кто то не закончил на низ или 'n-1'  игроков  не  совершат  ошибку,  то есть появится winner =1  """
            print(self.pouch)#распечатать состояние мешка
            new_barrel = self.pouch.take_barrel()#достаем  один бочонок
            for player in self.players:#перебираем, получаем одного из игроков
                if player not in leave_players:
                    current_name = player.name
                    print(f"\n*************** Ход игрока: {player.name} ***************")
                    print(player)#принтуем его карточки(их может несколько быть)
                    #проверка карточек(всех) на наличие бочонка - True, False
                    have_number = player.have_num(player.cards, new_barrel)# есть ли такой номер на картах игрока
                    #компьютер уже знает ответ на вопрос
                    remove = player.replacement_number(new_barrel)#вопрос о замене
                    #проверка совпадения ответа и have_number, если  True и YES ,  No и False, должно  давать True
                    if have_number == True and remove == True:
                        #return True, то заменяем номер в карточке, и проверяем завершенность ряда
                        for card in player.cards:# в каждой карте
                            card.replacement(card, new_barrel)
                            res = card.closed_card()#проверка на завершеннность ряда, возвращает номер завершенного ряда
                            print(card)
                            """появится  сообщение о  завершенности ряда и выдаст его номер, а дальше условие
                            если 1 и 2 - продолжается цикл с другой карточкой игрока, если 3 - закончить цикл и вызвать 
                            функцию  Баланс счетов, """

                            if res == 0:
                                print("Продолжаем.....")
                            elif res == 1:
                                self.finish_top(current_name)
                            elif res == 2:
                                self.finish_middle(current_name)
                            else:
                                winner += 1
                                self.finish_bottom(current_name)
                                if winner == 1:
                                    break


                    elif have_number == False and remove == False:
                        print("Продолжаем.......")


                    else: #игрок ошибся
                        player.mistake()#выбрасываем совершившего ошибку..
                        leave_players.append(player)#добавляем в список проигравших, и пока
                        #не  оставлся  один игрок печатается список оставшихся участников
                        res = self.winner_one(winner, leave_players)
                        winner += res
                        if winner == 1:
                            break

        else:
            print("Раунд закончен, получите отчет о динамике средств" )
            print("\t\t************ В раунде игры Лото участвовали игроки ************:")
            col = 1
            for player in self.players:
                print(f'{col}. {player.name}, кредит: {player.credit} УЕ, выигрыш: {player.winning} УЕ, проигрыш: {player.loss} УЕ')
                col += 1
            if leave_players:
                print("\t\t************ Сделав ошибку, выбыли игроки: ************:")
                col = 1
                for player in self.players:
                    if player in leave_players:
                        print(f'{col}. {player.name}')
                        col += 1


def main():
    """ создает игроков, организует  их  в виде  списка, создает  объект Game,
    и передает в него список  игроков как аргумент? затем  вызывает метод  play, и  делает  это циклически,
    пока не получить команду прекратить игру
    :return:
    """

    players = []#список  игроков (кортежи)
    """ можно было сделать через while,  не интересуясь  количеством  игроков,  просто  спрашивая добавить
       игрока  или нет...."""

    while True:
        try:
            num_players = games.ask_number(question="Сколько  игроков участвует в игре Лото? (от 2 до 5): ", low=2, high=5)
            break
        except ValueError:
            print("Вы ввели не число. Попробуйте снова: ")


    for i in range(num_players):#создание объектов player, соответствующее количеству  игроков

        name = input("Введите имя игрока: ") # ввод атрибутов объектов класса Player
        while True:
            try:
                credit = int(input("Кредит игрока: "))  # ввод атрибутов объектов класса Player
                break
            except ValueError:
                print("Вы ввели не число. Попробуйте снова: ")


        player = Loto_Player(name, credit)  # создание объектов player
        players.append(player)#добавляем  по  одному  в  список игроков players


    print("\t\t************ В игре Лото участвуют игроки ************:")
    col = 1
    for player in players:
        print(f' {col}. {player.name}, кредит: {player.credit} УЕ, выигрыш: {player.winning} УЕ, '
              f'проигрыш: {player.loss} УЕ')
        col += 1

    start = games.ask_yes_no(question="Начать игру(y/n)?: ")
    """спрашиваем  об  этом  один  раз, позднее, когда  заверщиться  раунд и выясниться  победитель
    просто спросим  Хотите сыграть снова?  и  запустим  цикл  игры без принтования  правил
    и  глупых  шуточек"""
    if (start == "y" or start =="н"):
        print("""\t\tУчастники  игры! Будьте  внимательны!
         У вас  всего один  шанс закрыть число на  карте фишкой, иначе - проигрыш!...\n""")
    else:
        print("\t\tИспугались? Деньги не  вернем!!!!!...\n")

    again = None
    """будем  повторять  циклично  создание  объекта Игра"""
    while not(again == "т" or again == "n"):
        game = Loto_Game(players)#создание  отдельной  игры Лото, игровой  цикл повторяется в этом объекте.
        game.play_round()
        again = games.ask_yes_no(question="Сыграем снова тем же составом (y/n)?: ")

    else:
        print("Игра закончена")


if __name__ == '__main__':
    input("\n\nНажмите  Enter, чтобы выйти.")













