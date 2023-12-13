import random
from time import sleep as sleep

# TODO:
# finish split()
# chips need to be won!
# oh and do something that the player wins a proper amount of chips for each hand, when he splits his initial hand
# check for blackjacks
# create a bust status


# -----INITIALIZING A DECK OF 52 CARDS-----
def shuffle_deck():
    deck = list()
    card_names = (
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    )
    card_colors = ("Spades", "Hearts", "Diamonds", "Clubs")
    power_limit = 10
    power = 2
    for name in card_names:
        for color in card_colors:
            if name == "Ace":
                power = 11
            new_card = Card(name, color, power)
            deck.append(new_card)
        if power < power_limit:
            power += 1
    random.shuffle(deck)
    return deck


class Card:
    def __init__(self, name, color, power):
        self.name = name
        self.color = color
        self.power = power

    def __str__(self):
        return "{name} of {color}.".format(
            name=self.name, color=self.color, power=self.power
        )


class Contestant:
    contestants = list()

    def __init__(self):
        self.dealer = True
        self.name = "Dealer"
        self.hand = list()
        self.hand_power = 0
        Contestant.contestants.append(self)

    def draw(self):
        drawn_card = deck.pop(0)
        self.hand.append(drawn_card)
        if self.name == "Dealer" and len(self.hand) == 2:
            print("Dealer draws a second card.")
        else:
            print(self.name, "draws", drawn_card.name, "of", drawn_card.color)
        if self.hand_power + drawn_card.power > 21:
            if drawn_card.name == "Ace":
                drawn_card.power = 1
            if self.hand_power + drawn_card.power > 21:
                print(self.name, "busts!")
                sleep(1)
                self.hand_power += drawn_card.power
            else:
                self.hand_power += drawn_card.power
        else:
            self.hand_power += drawn_card.power

    def stand(self):
        print(self.name, "stands with a hand power of", self.hand_power)


class Player(Contestant):
    def __init__(self):
        Contestant.__init__(self)
        self.dealer = False
        self.name = input("Enter a name: ")
        self.chips = 3000

    def bet(self):
        self.bet = int(
            input("{player}, how much do you want to bet: ".format(player=self.name))
        )

    def double_down(self):
        print(self.name, "doubles down!")
        self.bet *= 2
        self.draw()

    def call(self):
        self.draw()

    def fold(self):
        print(self.name, "folds.")
        self.lose()

    def lose(self):
        print(self.name, "loses", self.bet, "chips...")
        self.chips -= self.bet

    def win(self):
        print(self.name, "wins", self.bet, "chips!")
        self.chips += self.bet

    def split(self):
        print("DUPA")
        for card in self.hand:
            pass

    def choice(self):
        self.turn_ended = False
        while self.turn_ended is False:
            if self.hand_power > 21:
                self.turn_ended = True
                break
            print("c- call", end=" ")
            if len(self.hand) < 3:
                print("d- call", end=" ")
            if self.hand[0].name == self.hand[1].name and len(self.hand) < 3:
                print("spl - split")
            print("s- stand", "f - fold", end=" ")
            print("| hand power:", self.hand_power)
            choice = input("Enter a choice: ")
            choice = choice.lower()
            if choice == "c":
                self.call()
            elif choice == "d" and len(self.hand) < 3:
                self.double_down()
                self.turn_ended = True
            elif choice == "s":
                self.stand()
                self.turn_ended = True
            elif choice == "f":
                self.fold()
                self.turn_ended = True
            elif (
                choice == "spl"
                and self.hand[0].name == self.hand[1].name
                and len(self.hand) < 3
            ):
                self.split()
            else:
                print("Wrong choice, {name}, try again!".format(name=self.name))
                self.choice()


if __name__ == "__main__":
    # -----INITIALIZING A DEALER AND A PLAYER -----
    dealer = Contestant()
    deck = shuffle_deck()
    how_many_players = int(input("Enter the amount of players: "))
    for i in range(0, how_many_players):
        new_player = Player()
        print("Welcome,", new_player.name)
    for player in Contestant.contestants[1:]:
        player.bet()
    for i in range(2):
        for player in Contestant.contestants:
            player.draw()
    for player in Contestant.contestants[1:]:
        player.choice()
    while dealer.hand_power < 17:
        dealer.draw()
    else:
        if dealer.hand_power < 21:
            dealer.stand()
