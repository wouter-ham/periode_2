# Made by:
# Wouter van der Ham (0986470)

from dataclasses import dataclass
from random import randint


class GreedyPig:
    players: list = []
    mode: int = 0
    currentPlayer: int = 0
    limit: int = 0

    def __init__(self):
        print(
            "Welcome to the mini game: Greedy Pig.\nFirst of all, let's fill in the amount of players in a range of "
            "(2-6).")
        players = int(input("Amount of players: "))
        print(
            "Select now in which mode you'd like to play:\n\n1. Who reaches 50 points first wins\n2. Who reaches 100 "
            "points first wins\n3. Set a custom limit")
        mode = int(input("Game mode: "))

        if mode == 1:
            self.limit = 50
        elif mode == 2:
            self.limit = 100
        else:
            self.limit = int(input("Custom limit: "))
        print()
        self.start(players, mode)

    def start(self, players: int, mode: int):
        self.mode = mode
        for i in range(1, players + 1):
            name = str(input("Name of player " + str(i) + ": "))
            self.players.append(Player(i, name, 0))
        self.roll()

    def check(self):
        for i in self.players:
            if i.amount >= self.limit:
                return False
        return True

    def roll(self, turn: int = 0, fresh: bool = False):
        player = self.players[self.currentPlayer]

        if not fresh:
            print(Colors.BOLD + "------------------------------------------\nCurrent ranking:" + Colors.ENDC)
            for i in self.players:
                print(i.name + ": " + str(i.amount))
            print(Colors.BOLD + "------------------------------------------" + Colors.ENDC)

        print("It's " + player.name + ''''s turn now.
        Press "enter" to roll the dice,
        or type "-" to collect points and end your turn.''')
        output = input()
        if output == "":
            rolled = randint(1, 6)
            if rolled == 1:
                print(Colors.FAIL + "You rolled 1! this turns score is reset and the next player is up." + Colors.ENDC)
                self.next_player()
            else:
                print(Colors.OKBLUE + "You rolled " + str(rolled) + "! Your turn's score is now: " + str(
                    turn + rolled) + ".\n\n" + Colors.ENDC)
                if self.check():
                    self.roll(turn + rolled, True)
                else:
                    print(Colors.OKGREEN + str(player.name) + " has won the game!")
        elif output == "-":
            player.amount += turn
            print("A total of " + str(turn) + " is added to your points!\nYou are currently at " +
                  str(player.amount) + " points.")
            if self.check():
                self.next_player()
            else:
                print(Colors.OKGREEN + "\n\n" + str(player.name) + " has won the game!" + Colors.ENDC)

    def next_player(self):
        if self.currentPlayer < len(self.players) - 1:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 0
        self.roll()


@dataclass
class Player:
    id: int = 0
    name: str = ""
    amount: int = 0

    def __init__(self, id: int, name: str, amount: int):
        self.id = id
        self.name = name
        self.amount = amount


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


GreedyPig()
