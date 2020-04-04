import random


class Dialog():
    '''Class contains methods
       to communicate with user'''

    def input_answer(self, message):
        '''
        check and processing
        answer entered by user
        '''
        print(message)
        answer = str(input())
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print('error input, try again')
            return self.input_answer(message)

    def input_int(self, message):
        '''
        check and processing
        input entered by user
        '''
        print(message)
        try:
            int_input = int(input())
        except ValueError:
            print('Players number must be int, try again')
            return self.input_int(message)

        return int_input


class Card():
    def __init__(self):
        self._array = []
        self._card_list = []
        self.real_card = []
        self.sum = 0

        while len(self._array) < 15:
            num = random.randrange(1, 91, 1)
            if self._array.count(num) == 0:
                self._array.append(num)
                self.__append_num_check()

        self._array.sort()

        for num in self._array:
            self.sum += num

        counter = 0

        for card in self._card_list:
            if card.sum != self.sum:
                counter += 1
            else:
                return

        if counter == len(self._card_list): self._card_list.append(self)
        else: self.__init__()

        self.__sort()


    def __append_num_check(self):
        num_checker = []
        for number in self._array:
            if number == 90: num_checker.append(8)
            else: num_checker.append(number // 10)

        for i in num_checker:
            if num_checker.count(i) > 3:
                self._array.pop()
                return

    def __sort(self):
        sorted_card = []
        columns = 9
        for i in range(0,columns):
            column_arr = []
            for number in self._array:
                if i*10 <= number < (i+1)*10:
                    column_arr.append(number)

            while len(column_arr)<3:
                column_arr.append(0)

            for i in range(0,3):
                number = column_arr.pop(random.randrange(0,3,1))
                column_arr.append(number)

            sorted_card.append(column_arr)

        for i in range(0,3):
            self.real_card.append([])

        for card in sorted_card:
            for i, number in enumerate(card):
                self.real_card[i].append(number)

    def get_array(self):
        return self._array

    def set_array(self, num):
        def change_array(array):
            i = array.index(num)
            array.insert(i, -1)
            array.remove(num)

        change_array(self._array)
        for line in self.real_card:
            if line.count(num):
                change_array(line)

    array = property(get_array, set_array)

    def __repr__(self):
        pretty_card = ''
        for card in self.real_card:
            for number in card:
                pretty_card += f'{number}\t'

            pretty_card += '\n'

        return pretty_card


class Game():
    def __init__(self):
        self.round = 0
        self._used_kegs = []
        self._winner = None

    def _keg_gen(self):
        if len(self._used_kegs) == 90:
            return

        keg = random.randrange(1,91,1)
        while self._used_kegs.count(keg) != 0:
            keg = random.randrange(1,91,1)

        self._used_kegs.append(keg)
        return keg

    def _card_check(self, card, keg):
        if card.count(keg) == 0:
            return False
        else:
            return True

    def __human_move(self, player, card, keg):
        player_name = player.name
        player_is_human = player.is_human
        right_answer = self._card_check(card.array, keg)

        message = f'{player_name}, your card:\n{card}you have {keg}? answer y if yes, n if no'
        answer = dialog.input_answer(message)

        if answer == right_answer:
            if answer: card.array = keg
        else:
            players.remove(player)
            print(f'{player_name} are lost!')
            return

    def __bot_move(self, player, card, keg):
        player_name = player.name
        print(f'bot {player_name} card:\n{card}')
        # add 1% chance to bot loose
        right_answer = self._card_check(card.array, keg)
        humanize = random.randrange(0,100,1)

        if humanize == 0:
            players.remove(player)
            print(f'{player_name} are lost!')
            return

        if right_answer:
            card.array = keg

    def _move(self, player, keg):
        card = player_cards[player.name]

        if player.is_human:
            self.__human_move(player, card, keg)
        else:
            self.__bot_move(player, card, keg)

        if card.array.count(-1) == 15:
            self._winner = player.name
        if len(players) == 1:
            self._winner = players[0]

    def input_players_number(self):
        message = 'Input players number'
        players_number = dialog.input_int(message)

        return players_number

    def play(self, players):
        while self._winner is None:
            keg = self._keg_gen()
            print(self.round_state())
            for player in players:
                self._move(player, keg)
            self.round += 1

        print(f'{self._winner} is the winner!')

    def round_state(self):
        return f'round {self.round}'


class Player():
    def __init__(self):
        self.name = self.set_player_name()
        self.is_human = self.set_is_human_flag()
        '''
        self.name = name
        self.is_human = is_human
        '''

    def set_player_name(self):
        player_number = len(players) + 1
        print(f'Input name of player {player_number}')
        name = str(input())
        if len(players) == 0:
            return name

        for player in players:
            if not player.name == name:
                return name

        print('This name already exist. Try again')
        return self.player_name()

    def set_is_human_flag(self):
        message = f'is player {self.name} human? answer "y" if yes or "n" if no'
        is_human = dialog.input_answer(message)
        return is_human

    def __repr__(self):
        return self.name

def main():
    players_number = game.input_players_number()

    for i in range(players_number):
        players.append(Player())

    for player in players:
        player_cards[player.name] = Card()

    game.play(players)


if __name__ == '__main__':
    players = []
    player_cards = {}
    dialog = Dialog()
    game = Game()
    main()

