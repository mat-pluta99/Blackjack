import random
<<<<<<< HEAD
from time import sleep as sleep

# TODO:
# finish split()
# chips need to be won! do a check if: dealer busted, if a player busted, if a player has a better hand than dealer
# oh and do something that the player wins a proper amount of chips for each hand, when he splits his initial hand
=======
>>>>>>> parent of cb74aed (game mechanics have been created)


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
        self.split_hand = list()
        self.split_hand_power = 0
        self.hand_power = 0

    def draw(self, hand, hand_power):
        drawn_card = deck.pop(0)
<<<<<<< HEAD
        hand.append(drawn_card)
        if self.name == "Dealer" and len(hand) == 2:
            print("Dealer draws a second card.")
        else:
            print(self.name, "draws", drawn_card.name, "of", drawn_card.color)
        if hand_power + drawn_card.power > 21:
            if drawn_card.name == "Ace":
                drawn_card.power = 1
            if hand_power + drawn_card.power > 21:
                print(self.name, "busts!")
                sleep(1)
                hand_power += drawn_card.power
=======
        self.hand.append(drawn_card)
        print(self.name, "draws", drawn_card.name, "of", drawn_card.color)
        if self.hand_power + drawn_card.power > 21:
            if drawn_card.name == "Ace":
                drawn_card.power = 1
            if self.hand_power + drawn_card.power > 21:
                self.lose()
>>>>>>> parent of cb74aed (game mechanics have been created)
            else:
                hand_power += drawn_card.power
        else:
            hand_power += drawn_card.power

<<<<<<< HEAD
    def stand(self, hand_power):
        print(self.name, "stands with a hand power of", hand_power)

=======
>>>>>>> parent of cb74aed (game mechanics have been created)

class Player(Contestant):
    def __init__(self):
        Contestant.__init__(self)
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

    def stand(self):
        print(self.name, "stands.")

    def fold(self):
        print(self.name, "folds.")
        self.lose()

    def win(self):
        if player.split == False:
            print(self.name, "wins", self.bet, "chips!")
            self.chips += self.bet

    def lose(self):
        print(self.name, "loses", self.bet, "chips...")
        self.chips -= self.bet

    def split(self):
<<<<<<< HEAD
        self.split = True
        self.split_bet = self.bet
        split_card = self.hand.pop(1)
        self.split_hand.append(split_card)
        print("DRAW TO THE FIRST HAND:", end=" ")
        self.draw()
        print("DRAW TO THE SECOND HAND:", end=" ")
        self.draw(self.split_hand)
        print("---FIRST HAND---")
        self.choice()
        print("---SECOND HAND---")
        self.choice(self.split_hand, self.split_hand_power)
        if self.hand_power > 21 and self.split_hand_power > 21:
            self.busted = True
            print(self.name, "busts with both hands!")

    def choice(self, hand, hand_power):
        self.turn_ended = False
        while self.turn_ended is False:
            if hand_power > 21:
                self.turn_ended = True
                break
            print("c- call", end=" ")
            if len(self.hand) < 3:
                print("d- call", end=" ")
            if (
                self.hand[0].name == self.hand[1].name
                and len(self.hand) < 3
                and self.split == False
            ):
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
=======
        pass
>>>>>>> parent of cb74aed (game mechanics have been created)


if __name__ == "__main__":
    # -----INITIALIZING A DEALER -----
    dealer = Contestant()
    deck = shuffle_deck()
<<<<<<< HEAD
    how_many_players = int(input("Enter the amount of players: "))
    for i in range(0, how_many_players):
        new_player = Player()
        print("Welcome,", new_player.name)
    for player in Contestant.contestants[1:]:
        player.split = False
        player.busted = False
        player.bet()
    for i in range(2):
        for player in Contestant.contestants:
            player.draw(player.hand, player.hand_power)
    for player in Contestant.contestants[1:]:
        player.choice()
    while dealer.hand_power < 17:
        dealer.draw(dealer.hand, dealer.hand_power)
    else:
        if dealer.hand_power < 21:
            dealer.stand()
        else:
            dealer.busted = True
            print("Dealer busts!")
    for player in Contestant.contestants[1:]:
        if player.split == True:
            if player.busted == True:
                player.bet += player.split_bet
                print(player.name, "loses", player.bet, "chips...")
            elif player.busted == False:
                if player.hand_power > 21 == False:
                    if player.hand_power > dealer.hand_power:
                        print(
                            player.name,
                            "wins",
                            self.bet,
                            "chips by first hand and",
                            end=" ",
                        )
                        self.chips += self.bet
                    elif player.hand_power < dealer.hand_power:
                        print(
                            player.name,
                            "loses",
                            self.bet,
                            "chips by first hand and",
                            end=" ",
                        )
                        self.chips -= self.bet
                    else:
                        print(player.name, "ties with dealer first hand and", end=" ")
                elif player.split_hand_power > 21 == False:
                    if player.split_hand_power > dealer.hand_power:
                        print(
                            player.name, "wins", self.split_bet, "chips by second hand!"
                        )
                        self.chips += self.split_bet
                    elif player.split_hand_power < dealer.hand_power:
                        print(
                            player.name,
                            "loses",
                            self.split_bet,
                            "chips by second hand!",
                        )
                        self.chips -= self.split_bet
                    else:
                        print(player.name, "ties with dealer by second hand!")
=======
    player = Player()

    player.bet()
    player.double_down()
    player.call()
    player.stand()
    player.fold()
    player.lose()
    player.win()
>>>>>>> parent of cb74aed (game mechanics have been created)
