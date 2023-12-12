import random


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
    def __init__(self):
        self.name = "Dealer"
        self.hand = list()
        self.hand_power = 0

    def draw(self):
        drawn_card = deck.pop(0)
        self.hand.append(drawn_card)
        print(self.name, "draws", drawn_card.name, "of", drawn_card.color)
        if self.hand_power + drawn_card.power > 21:
            if drawn_card.name == "Ace":
                drawn_card.power = 1
            if self.hand_power + drawn_card.power > 21:
                self.lose()
            else:
                self.hand_power += drawn_card.power
        else:
            self.hand_power += drawn_card.power


class Player(Contestant):
    def __init__(self) -> None:
        Contestant.__init__(self)
        self.name = input("Enter a name: ")
        self.chips = 3000

    def bet(self):
        self.bet = input(
            "{player}, how much do you want to bet: ".format(player=self.name)
        )

    def double_down(self):
        self.draw()
        print(self.name, "doubles down and draws", self.hand[-1])

    def call(self):
        self.draw()

    def stand(self):
        pass

    def fold(self):
        pass

    def lose(self):
        pass

    def win(self):
        pass

    def split(self):
        pass


if __name__ == "__main__":
    # -----INITIALIZING A DEALER -----
    dealer = Contestant()
    deck = shuffle_deck()
    player = Player()
    dealer.draw()
    player.double_down()
