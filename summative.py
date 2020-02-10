# Wouter van der Ham (0986470)
# Lars van Houwelingen (0987210)
import os
import sys
from dataclasses import dataclass
from random import randint
import matplotlib.pyplot as plt


class GreedyPig:
    players: list = []
    mode: int = 0
    currentPlayer: int = 0
    limit: int = 0
    output: bool = True
    returnValue = False

    def __init__(self, player_amount=None, players: list = None, mode: int = None, output: bool = True):
        self.output = output

        if player_amount is None:
            Text("Welcome to the mini game: Greedy Pig.\nFirst of all, "
                 "let's fill in the amount of players in a range of (2-6).", output=self.output)
            player_amount = Text.getint('Amount of players: ')
        if not 2 <= player_amount <= 6:
            Text.warn(self.output)
            GreedyPig(mode=mode, players=players)
            return

        if mode is None:
            Text("Select now in which mode you'd like to play:\n\n1. Who reaches 50 points first wins\n"
                 "2. Who reaches 100 points first wins\n", output=self.output)
            mode = Text.getint("Game mode: ")

        self.mode = mode

        if mode != 1 and mode != 2:
            Text.warn(self.output)
            GreedyPig(player_amount=player_amount, mode=mode, players=players)
            return

        if mode == 1:
            self.limit = 50
        elif mode == 2:
            self.limit = 100

        if players is None:
            self.start(player_amount, mode)
        else:
            self.players = players
            self.roll(fresh=True)

    def start(self, players: int, mode: int):
        self.mode = mode
        for i in range(1, players + 1):
            self.input_name(i)

        self.roll()

    def input_name(self, i):
        name = str(input("Name of player " + str(i) + ": "))
        if name != '':
            return self.players.append(Player(i, name, 0, None))
        else:
            Text.warn(self.output)
            return self.input_name(i)

    def check(self):
        """return True if nobody has reached the limit"""
        for i in self.players:
            if i.amount >= self.limit:
                return False
        return True

    def roll(self, turn: int = 0, fresh: bool = False):
        player = self.players[self.currentPlayer]

        if not fresh:
            Text("------------------------------------------\nCurrent ranking:", 'bold', output=self.output)
            for i in self.players:
                Text(i.name + ": " + str(i.amount), output=self.output)
            Text("------------------------------------------", 'bold', output=self.output)

        if player.algorithm is None:
            Text("It's " + player.name + "\'s turn now.\n"
                                         "Press \"enter\" to roll the dice,\n"
                                         "or type \"-\" to collect points and end your turn.", output=self.output)

        if player.algorithm is None:
            output = input()
            if output == "":
                rolled = randint(1, 6)
                if rolled == 1:
                    Text("You rolled 1! this turns score is reset and the next player is up.\n\n\n", 'fail',
                         output=self.output)
                    self.next_player()
                else:
                    Text("You rolled " + str(rolled) + "! Your turn's score is now: " + str(turn + rolled)
                         + ".\n\n", 'blue', output=self.output)
                    if self.check():
                        self.roll(turn + rolled, True)
                    else:
                        Text(player.name + " has won the game!", 'green', output=self.output)
                        self.returnValue = player.id
            elif output == "-":
                player.amount += turn
                Text("A total of " + str(turn) + " is added to your points!\nYou are currently at " +
                     str(player.amount) + " points.", output=self.output)
                if self.check():
                    self.next_player()
                else:
                    Text("\n\n" + player.name + " has won the game!", 'green', output=self.output)
                    self.returnValue = player.id
            else:
                Text.warn(self.output)
                self.roll(turn, True)
        else:
            if player.algorithm(turn):
                rolled = randint(1, 6)
                if rolled > 1:
                    Text('Bot: ' + player.name + " rolled: " + str(rolled), "bold", output=self.output)
                    if self.check():
                        self.roll(turn + rolled, True)
                    else:
                        Text(player.name + " has won the game!", 'green', output=self.output)
                        self.returnValue = player.id
                else:
                    Text('Bot: ' + player.name + " rolled: " + str(rolled), 'fail', output=self.output)
                    self.next_player()
            else:
                Text('Bot: ' + player.name + " stopped", "bold", output=self.output)
                player.amount += turn
                if self.check():
                    self.next_player()
                else:
                    Text(player.name + " has won the game!", 'green', output=self.output)
                    self.returnValue = player.id

    def next_player(self):
        if self.currentPlayer < len(self.players) - 1:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 0
        self.roll()

    def result(self):
        # yes I know this is not a good way to do this, but I didn't want to rewrite the whole game.
        while self.returnValue:
            return self.returnValue


@dataclass
class Player:
    id: int = 0
    name: str = ""
    amount: int = 0
    algorithm = None

    def __init__(self, id: int, name: str, amount: int, algorithm):
        self.id = id
        self.name = name
        self.amount = amount
        self.algorithm = algorithm


class Text:
    styles = {
        'header': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'warning': '\033[93m',
        'fail': '\033[91m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    }
    output: bool = True

    def __init__(self, text: str, style: str = '', output: bool = True):
        if output:
            if style != '' and self.supports_color():
                print(self.styles[style] + text + self.styles['end'])
            else:
                print(text)

    @staticmethod
    def warn(output: bool = True):
        if output:
            Text('\nInvalid input, try again\n', 'warning')

    @staticmethod
    def getint(text: str = ''):
        output = input(text)

        if output == '':
            Text.warn()
            return Text.getint(text)

        try:
            val = int(output)
            return val
        except ValueError:
            Text.warn()
            return Text.getint(text)

    @staticmethod
    def supports_color():
        """Returns True if the running system's terminal supports color, and False otherwise."""
        supported_platform = sys.platform != 'Pocket PC' and (sys.platform != 'win32' or 'ANSICON' in os.environ)
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        return supported_platform and is_a_tty


class Automator:
    results: dict = {}
    dummies: dict = {
        'players': [
            Player(1, 'Lars', 0, lambda x: x <= 12),
            Player(2, 'Menno', 0, lambda x: x <= 33),
            Player(3, 'Wouter', 0, lambda x: x <= 15)
            # if you set the last parameter (called algorithm) to None, you can play against bots
        ]
    }

    def __init__(self, loops: int = 1):
        length = len(self.dummies['players'])

        for i in range(1, length + 1):  # prepare the result array
            self.results[i] = 0

        for i in range(loops):
            self.results[GreedyPig(length, self.dummies['players'][:], 2, False).result()] += 1
            # put the last player at the first place.
            self.dummies['players'] = self.dummies['players'][-1:] + self.dummies['players'][:-1]

        plt.bar(self.results.keys(), self.results.values())
        plt.show()


Automator(1000)
