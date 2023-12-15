import random
from time import sleep as sleep


# TODO:
# finish split()
# make sure that the player wins a proper amount of chips for each hand, when he splits his initial hand
# make sure that dealer does not draw if every player has either busted, folded or scored a blackjack without additional drawing
# ask if players want to stop or play again
# if a player wants to stop and has enough chips to break a highscore, save his record to the ranking board in the menu
# create a menu, where one can start a new game, see a ranking board or quit the game
# describe a program and its functions!


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
    random.shuffle(deck)
    return deck


class Contestant:
    contestants = list()

    def __init__(self):
        self.name = "Dealer"
        self.hand = list()
        self.hand_power = 0
        self.busted = False
        self.turn_ended = False
        Contestant.contestants.append(self)

    def draw(self):
        drawn_card = deck.pop(0)
        self.hand.append(drawn_card)
        if self.name == "Dealer" and len(self.hand) == 2:
            print("Dealer draws a second card.")
        else:
            print(self.name, "draws", drawn_card.name, "of", drawn_card.color)
        self.hand_power += drawn_card.power
        if self.hand_power > 21:
            for card in self.hand:
                if card.power == 11:
                    card.power -= 10
                    self.hand_power -= 10
                if self.hand_power < 21:
                    break
            if self.hand_power > 21:
                self.busted = True
                print(self.name, "busts!")

    def stand(self):
        print(self.name, "stands with a hand power of", self.hand_power)
        sleep(1.2)


class Player(Contestant):
    def __init__(self):
        Contestant.__init__(self)
        self.name = input("Enter a name: ")
        self.chips = 3000
        self.folded = False

    def bet(self):
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
        self.bet *= 2
        self.draw()

    def call(self):
        self.draw()

    def fold(self):
        print(self.name, "folds.")
        self.folded = True

    def lose(self):
        self.bet = int(self.bet)
        print(self.name, "loses", self.bet, "chips...")
        self.chips -= self.bet
        sleep(1.2)

    def win(self):
        self.bet = int(self.bet)
        print(self.name, "wins", self.bet, "chips!")
        self.chips += self.bet
        sleep(1.2)

    def split(self):
        print("DUPA")
        for card in self.hand:
            pass

    def choice(self):
        while self.turn_ended is False:
            if self.hand_power > 21:
                self.turn_ended = True
                self.busted = True
                break
            print("c- call", end=" ")
            if len(self.hand) < 3 and self.bet <= (self.chips * 2):
                print("d- double down", end=" ")
            if self.hand[0].name == self.hand[1].name and len(self.hand) < 3:
                print("spl - split")
            print("s- stand", "f - fold", end=" ")
            print("| hand power:", self.hand_power)
            while True:
                choice = input("Enter a choice: ")
                try:
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
                        raise
                except:
                    print("Wrong choice, {name}, try again!".format(name=self.name))
                else:
                    break
        sleep(1.2)


def game():
    # -----INITIALIZING A DEALER AND A PLAYER -----
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
            player.chips = 0
            print(
                "{name}, you have {chips}.".format(name=player.name, chips=player.chips)
            )
            if player.chips == 0:
                print("That makes you lose the game! :(")
                Contestant.contestants.remove(player)
            else:
                another_round = input("Do you want to play another game?")


def round_():
    dealer = Contestant()
    move_dealer = Contestant.contestants.pop()
    for p in Contestant.contestants:
        print(p.name)
    Contestant.contestants.insert(0, move_dealer)
    for p in Contestant.contestants:
        print(p.name)
    for player in Contestant.contestants[1:]:
        player.bet()
    for i in range(2):
        for player in Contestant.contestants:
            player.draw()
            sleep(1.2)
    if dealer.hand_power == 21:
        print("The dealer has a Blackjack!")
        sleep(1.1)
    player_blackjacks = 0
    for player in Contestant.contestants[1:]:
        if player.hand_power == 21:
            print(player.name, "has a Blackjack!")
            sleep(1.1)
            player_blackjacks += 1
        if player.hand_power == 21 and dealer.hand_power == 21:
            print(player.name, "ties with the Dealer!")
            sleep(1.1)
        elif player.hand_power == 21 and dealer.hand_power != 21:
            player.bet *= 3 / 2
            player.win()
        elif player.hand_power != 21 and dealer.hand_power == 21:
            player.bet *= 3 / 2
            player.lose()
    if (
        len(Contestant.contestants[1:]) == player_blackjacks
        or player_blackjacks == 0
        and dealer.hand_power == 21
    ):
        pass
    else:
        for player in Contestant.contestants[1:]:
            if player.hand_power == 21:
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
                dealer.hand[0],
                "and",
                dealer.hand[1],
                "| hand power:",
                dealer.hand_power,
            )
            sleep(1.2)
        if any(
            player.busted == False and player.folded == False
            for player in Contestant.contestants[1:]
        ):
            while dealer.hand_power < 17:
                dealer.draw()
            if dealer.hand_power < 21:
                dealer.stand()
            for player in Contestant.contestants[1:]:
                if player.folded:
                    print("By folding,", end=" ")
                    player.lose()
                    continue
                if player.hand_power == 21 and len(player.hand) == 2:
                    continue
                print("{name}'s cards are:".format(name=player.name), end=" ")
                sleep(1.2)
                for card in player.hand:
                    print(card.__str__(), end=" ")
                    sleep(1.2)
                print(
                    "\n{name}'s hand power is {hand_power}.".format(
                        name=player.name, hand_power=player.hand_power
                    )
                )
                sleep(1.3)
                if (
                    player.hand_power < dealer.hand_power
                    and dealer.hand_power < 22
                    or player.busted == True
                ):
                    player.lose()
                elif (
                    player.hand_power > dealer.hand_power
                    or player.busted == False
                    and dealer.busted == True
                ):
                    player.win()
                else:
                    print(player.name, "ties with the dealer!")

                    sleep(1.5)
        else:
            print("Every player has either busted or folded!")
            for player in Contestant.contestants[1:]:
                player.lose()


game()
