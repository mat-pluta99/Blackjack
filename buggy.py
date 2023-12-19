import random
from time import sleep as sleep
import sys
import os

# -------------- WORK IN PROGRESS ----------------
# this is an attempt at adding a possibility to split a hand during the game, but the game does not work

# the dealer is draws his first card and after that, that card's power is added to the dealer's hand power
# then the player draws his first card, but the program crashes when trying to add a power to player's first hand

# i did not test the rest of the code, so it may be full of bugs


# -----INITIALIZING A DECK OF 52 CARDS-----
class Card:
    def __init__(self, name, color, power):
        self.name = name
        self.color = color
        self.power = power

    def __str__(self):
        return "{name} of {color}.".format(name=self.name, color=self.color)


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


def shuffle_deck():
    for contestant in Contestant.contestants:
        contestant.hand_power = [0][0]
        for i in range(2):
            while len(contestant.hand[i]) != 0:
                popped_card = contestant.hand.pop(0)
                deck.append(popped_card)
    random.shuffle(deck)
    return deck


class Contestant:
    contestants = list()

    def __init__(self):
        self.name = "Dealer"
        self.hand = [[], []]
        self.hand_power = [0, 0]
        self.busted = False
        self.turn_ended = False
        self.split = False
        self.chosen_hand = 0
        Contestant.contestants.append(self)

    def draw(self):
        i = 0
        drawn_card = deck.pop(0)
        self.hand[i].append(drawn_card)
        if self.name == "Dealer" and len(self.hand[0]) == 2:
            print("Dealer draws a second card.")
        else:
            print(self.name, "draws", drawn_card.name, "of", drawn_card.color)
        self.hand_power[i] += drawn_card.power

        if self.hand_power[i] > 21:
            for card in self.hand[i]:
                if card.power == 11:
                    card.power -= 10
                    self.hand_power[i] -= 10
                if self.hand_power[i] < 21:
                    break
            if self.hand_power[i] > 21:
                if self.split == True:
                    print(
                        "{name} busts on a hand number {n}!".format(name=self.name, n=i)
                    )
                else:
                    self.busted = True
                    print(self.name, "busts!")

    def stand(self):
        print(
            self.name, "stands with a hand power of", self.hand_power[self.chosen_hand]
        )
        sleep(1.2)


class Player(Contestant):
    def __init__(self):
        Contestant.__init__(self)
        while True:
            self.name = input("Enter a name: ")
            if not self.name.strip():
                print("You did not enter anything!")
                sleep(0.5)
            elif any(
                self.name == player.name for player in Contestant.contestants[:-1]
            ):
                print("This name already exist, please choose enter something else.")
                sleep(0.5)
            else:
                break
        self.chips = 3000
        self.play_again = True
        self.split = False
        self.split_double = False

    def make_bet(self):
        while True:
            try:
                self.bet = int(
                    input(
                        "{player}, how many chips do you want to bet (min. 1 and max. 500)? You have {chips} chips: ".format(
                            player=self.name, chips=self.chips
                        )
                    )
                )
                if self.bet in range(1, 501) and self.bet in range(1, self.chips + 1):
                    break
            except ValueError:
                print(
                    "Wrong input, please bet from min. 1  to max. 500 chips. If you have less than 500 chips, you can only bet up to an amount of chips you have left."
                )

    def double_down(self):
        print(self.name, "doubles down!")
        if self.split == True:
            self.split_double = True
        self.bet *= 2
        self.draw()

    def call(self):
        self.draw()

    def fold(self):
        print(self.name, "folds.")
        self.bet = int(self.bet / 2)
        self.folded = True

    def lose(self):
        self.bet = int(self.bet)
        print(self.name, "loses", self.bet, "chips...")
        self.chips -= self.bet
        sleep(1.2)

    def win(self):
        print(self.name, "wins", self.bet, "chips!")
        self.chips += self.bet
        sleep(1.2)

    def split_hand(self):
        self.split = True
        move_card = self.hand[0].pop(1)
        self.hand[1].append(move_card)

    def choice(self):
        self.chosen_hand = 0
        turn_ended = False
        while turn_ended is False:
            i = self.chosen_hand
            if self.split == True:
                if self.hand_power[0] > 21 and self.hand_power[1] > 21:
                    turn_ended = True
                    self.busted = True
                    break
            elif self.hand_power[0] > 21:
                turn_ended = True
                self.busted = True
                break
            elif self.hand_power[0] == 21:
                turn_ended = True
                break
            print("c- call", end=" ")
            if len(self.hand[i]) < 3 and self.bet <= (self.chips * 2) and i == 0:
                print("d- double down", end=" ")
            print("s- stand", end=" ")
            if len(self.hand[0] == 2 and self.hand[0][0] == self.hand[0][1]):
                self.split_hand()
            if self.split == False:
                print("f - fold (surrender)", end=" ")
            print("| hand power:", self.hand_power[i])
            while True:
                if self.split == True:
                    print(
                        "{name}'s hand {n}".format(name=self.name, n=self.chosen_hand)
                    )
                choice = input("Enter a choice: ")
                try:
                    choice = choice.lower()
                    if choice == "c":
                        self.call()
                    elif choice == "d" and len(self.hand) < 3 and self.chosen_hand == 0:
                        self.double_down()
                        if (
                            self.split == False
                            or self.split == True
                            and self.chosen_hand == 1
                        ):
                            turn_ended = True
                        else:
                            self.chosen_hand = 1
                    elif choice == "s":
                        self.stand()
                        if (
                            self.split == False
                            or self.split == True
                            and self.chosen_hand == 1
                        ):
                            turn_ended = True
                        else:
                            self.chosen_hand = 1
                    elif choice == "f":
                        self.fold()
                        turn_ended = True

                    elif (
                        choice == "spl"
                        and self.hand[0][0].name == self.hand[0][1].name
                        and len(self.hand) < 3
                    ):
                        self.split_hand()
                    else:
                        raise
                except:
                    print("Wrong choice, {name}, try again!".format(name=self.name))
                else:
                    break
        sleep(1.2)


def game():
    deck = shuffle_deck()
    while True:
        try:
            how_many_players = int(input("Enter the amount of players (max. 5): "))
            if how_many_players in range(1, 6):
                break
            else:
                raise
        except:
            print("Wrong input, try again!")
    for i in range(0, how_many_players):
        new_player = Player()
        print("Welcome,", new_player.name)
        sleep(1)
    while True:
        round_()
        for player in Contestant.contestants[1:]:
            print(
                "{name}, you have {chips}.".format(name=player.name, chips=player.chips)
            )
            if player.chips == 0:
                print("That makes you lose the game! :(")
                player.play_again = False
            else:
                another_round = input("Do you want to play another game? (y/n): ")
                if another_round.startswith("N") or another_round.startswith("n"):
                    player.play_again = False
                    print("See you around, {name}!".format(name=player.name))
                    sleep(1)
        if any(player.play_again == True for player in Contestant.contestants[1:]):
            pass
        else:
            menu()


def round_():
    os.system("cls")
    shuffle_deck()
    contestants_amount = len(Contestant.contestants)
    for i in range(0, contestants_amount - 1):
        contestant = Contestant.contestants[i]
        print(contestant.name)
        if contestant.name == "Dealer" or contestant.play_again == False:
            Contestant.contestants.remove(contestant)
            i -= 1
    dealer = Contestant()
    move_dealer = Contestant.contestants.pop()
    Contestant.contestants.insert(0, move_dealer)
    list_of_remaining = [
        contestant
        for contestant in Contestant.contestants
        if contestant.name == "Dealer" or contestant.play_again == True
    ]

    Contestant.contestants = list_of_remaining
    print("Remaining players:")
    for player in Contestant.contestants[1:]:
        player.busted = False
        player.chosen_hand = 0
        player.folded = False
        player.split = False
        print(player.name, "with", player.chips, "chips")
    sleep(1)
    for player in Contestant.contestants[1:]:
        player.make_bet()
    for i in range(2):
        for player in Contestant.contestants:
            player.draw()
            sleep(1.2)
    if dealer.hand_power[0] == 21:
        print("The dealer has a Blackjack!")
        sleep(1.1)
    player_blackjacks = 0
    for player in Contestant.contestants[1:]:
        if player.hand_power[0] == 21:
            print(player.name, "has a Blackjack!")
            sleep(1.1)
            player_blackjacks += 1
        if player.hand_power[0] == 21 and dealer.hand_power[0] == 21:
            print(player.name, "ties with the Dealer!")
            sleep(1.1)
        elif player.hand_power[0] == 21 and dealer.hand_power[0] != 21:
            player.bet *= 3 / 2
            player.win()
        elif player.hand_power[0] != 21 and dealer.hand_power[0] == 21:
            player.bet *= 3 / 2
            player.lose()
    if (
        len(Contestant.contestants[1:]) == player_blackjacks
        or player_blackjacks == 0
        and dealer.hand_power[0] == 21
    ):
        pass
    else:
        for player in Contestant.contestants[1:]:
            if player.hand_power[0] == 21:
                pass
            else:
                print("---{name}'s turn---".format(name=player.name))
                sleep(1)
                player.choice()
        if any(
            player.busted == False and player.folded == False
            for player in Contestant.contestants[1:]
        ):
            print("---DEALER'S TURN---")
            sleep(1)
            print(
                "The dealer's hand:",
                dealer.hand[0][0],
                "and",
                dealer.hand[0][1],
                "| hand power:",
                dealer.hand_power[0],
            )
            sleep(1.2)
        if any(
            player.busted == False
            and player.folded == False
            and (player.hand_power[0] == 21 and len(player.hand[0]) == 2) == False
            for player in Contestant.contestants[1:]
        ):
            while dealer.hand_power[0] < 17:
                dealer.draw()
            if dealer.hand_power[0] < 21:
                dealer.stand()
            for player in Contestant.contestants[1:]:
                if player.folded:
                    print("By folding,", end=" ")
                    player.lose()
                    continue
                if player.hand_power[0] == 21 and len(player.hand[0]) == 2:
                    continue
                for i in range(0, 2):
                    if player.split == False and i == 1:
                        continue
                    if player.split == True:
                        print("Hand", player.chosen_hand)
                    print("{name}'s cards are:".format(name=player.name), end=" ")
                    sleep(1.2)
                    for card in player.hand[i]:
                        print(card.__str__(), end=" ")
                        sleep(1.2)
                    print(
                        "\n{name}'s hand power is {hand_power}.".format(
                            name=player.name, hand_power=player.hand_power[i]
                        )
                    )
                sleep(1.3)
                if (
                    player.hand_power[0] < dealer.hand_power[0]
                    and dealer.hand_power[0] < 22
                    and player.split == False
                    or player.busted == True
                ):
                    player.lose()
                elif (
                    player.hand_power[0] > dealer.hand_power[0]
                    or player.busted == False
                    and dealer.busted == True
                ):
                    player.win()
                elif player.split == False:
                    print(player.name, "ties with the dealer!")
                    sleep(1.5)
                elif player.split == True:
                    split_bet = 0
                    for i in range(2):
                        if player.hand_power[i] > dealer.hand_power[0]:
                            if player.split_double == True and i == 0:
                                split_bet += player.bet
                            split_bet += player.bet
                            print("For a hand number {n}, {name} wins!")
                            sleep(1)
                        elif player.hand_power[i] < dealer.hand_power[0]:
                            if player.split_double == True and i == 0:
                                split_bet -= player.bet
                            split_bet -= player.bet
                            print("For a hand number {n}, {name} loses...")
                            sleep(1)
                        else:
                            print("For a hand number {n}, {name} ties.")
                            sleep(1)
                    player.bet = split_bet
                    if player.bet < 0:
                        player.lose()
                    elif player.bet > 0:
                        player.win()
                    else:
                        print(player.name, "ties with the dealer!")
        elif any(
            player.busted == False
            and player.folded == False
            and (player.hand_power[0] == 21 and len(player.hand[0]) == 2) == True
            for player in Contestant.contestants[1:]
        ):
            for player in Contestant.contestants[1:]:
                if player.busted == True:
                    print("By busting,", end=" ")
                    player.lose()
                elif player.folded == True:
                    print("By folding,", end=" ")
                    player.lose()
                elif (
                    player.hand_power[0] == 21
                    and len(player.hand[0] == 2)
                    and player.hand_power[0] > dealer.hand_power[0]
                ):
                    print(
                        "By {name} having a Blackjack and Dealer not having one,".format(
                            name=player.name
                        )
                    )
                    player.win()
                else:
                    print(player.name, "ties with the dealer!")

        else:
            print("Every player has either busted or folded!")
            for player in Contestant.contestants[1:]:
                player.lose()
    sleep(2)


def menu():
    os.system("cls")
    print("Blackjack.py by Mateusz Pluta https://github.com/mat-pluta99")
    print()
    print("-------BLACKJACK CASINO-------")
    print("1. Play the game")
    print("2. Leaderboard")
    print("3. Quit the game")
    menu_choice = input("Enter your choice: ")
    while True:
        if menu_choice[0] == "1":
            game()
        elif menu_choice[0] == "2":
            pass
        elif menu_choice[0] == "3":
            print("See you soon!")
            sleep(1)
            sys.exit()


menu()
