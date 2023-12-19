import random
from time import sleep as sleep
import sys
import os


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
    """
    shuffle_deck() takes all the cards from each player's hand, zeroes its power, puts theses cards back to the deck and then this deck is shuffled
    """
    global deck
    for contestant in Contestant.contestants:
        contestant.hand_power = 0
        while len(contestant.hand) != 0:
            popped_card = contestant.hand.pop(0)
            deck.append(popped_card)
    random.shuffle(deck)
    return deck


class Contestant:
    """This is a base class of each contestant in the game, including a dealer controlled by a computer. A contestant is able to draw a card to their hand, raise their hand power and bust by having a more powerful hand than 21 or have their turn ended after making a choice to stand, drawing 21 or busting"""

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
    """
    This is a class of every player, except for the dealer. A player can choose their name, enter their bets, choose to call, double down, stand or fold. If they beat any high score from the leaderboard(see "leaderboard.txt"), their name and score is saved.
    """

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
                else:
                    raise
            except:
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

    def choice(self):
        while self.turn_ended is False:
            if self.hand_power > 21:
                self.turn_ended = True
                self.busted = True
                break
            elif self.hand_power == 21:
                self.turn_ended = True
                break
            print("c- call", end=" ")
            if len(self.hand) < 3 and self.bet <= (self.chips * 2):
                print("d- double down", end=" ")
            print("s- stand", end=" ")
            print("f - fold (surrender)", end=" ")
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
                    else:
                        raise
                except:
                    print("Wrong choice, {name}, try again!".format(name=self.name))
                else:
                    break
        sleep(1.2)


def game():
    """
    game() function asks for the amount of players, initiates them and then starts a round. If a player has no chips after a round, they lose and are kicked out of the game. If a player still has any chips left, they can either continue playing or quit the game.

    If they quit, their score is compared to the leaderboard and, if the player has beaten any highscore, their name and score are appended to the ranking list. Then that ranking list is used to save the best 10 scores ever beaten in this game and write them in the "leaderboard.txt" file.
    """
    shuffle_deck()
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
                    if player.chips > int(ranking[-1][1]):
                        add_to_leaderboard(player.name, player.chips)
                    player.play_again = False
                    print("See you around, {name}!".format(name=player.name))
                    sleep(1)
        if any(player.play_again == True for player in Contestant.contestants[1:]):
            pass
        else:
            menu()


def round_():
    """
    round_() function controls the flow of a round of the game. The deck is shuffled by shuffle_deck() function and each contestand draws 2 cards to his hand, 1 card at a time.

    Then, the dealer's and the players' hand powers are compared if they have blackjack. If there is no hand power of 21, then players make choices to either call, double down or fold from the round.

    After that, the dealer draws until he either busts or has a hand power of 17 or more.

    At the end, the players' hand powers are compared to the dealer's hand power. Depending of the powers, the players can either win a round and add their bets to their chips, lose a round and their amount of chips is reduced by their bet, or tie with the dealer.
    """
    os.system("cls")
    shuffle_deck()
    contestants_amount = len(Contestant.contestants)
    for i in range(0, contestants_amount - 1):
        contestant = Contestant.contestants[i]
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
        player.turn_ended = False
        player.folded = False
        print(player.name, "with", player.chips, "chips")
    sleep(1)
    for player in Contestant.contestants[1:]:
        player.make_bet()
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
            player.busted == False
            and player.folded == False
            and (player.hand_power == 21 and len(player.hand) == 2) == False
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
        elif any(
            player.busted == False
            and player.folded == False
            and (player.hand_power == 21 and len(player.hand) == 2) == True
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
                    player.hand_power == 21
                    and len(player.hand == 2)
                    and player.hand_power > dealer.hand_power
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
    load_leaderboard()
    os.system("cls")
    print("Blackjack.py by Mateusz Pluta https://github.com/mat-pluta99")
    print()
    print("-------BLACKJACK CASINO-------")
    print("1. Play the game")
    print("2. Leaderboard")
    print("3. Quit the game")
    while True:
        menu_choice = input("Enter your choice: ")
        if menu_choice[0] == "1":
            game()
        elif menu_choice[0] == "2":
            os.system("cls")
            see_leaderboard()
            menu()
        elif menu_choice[0] == "3":
            print("See you soon!")
            sleep(1)
            sys.exit()
        else:
            print("There's no such option, please try again!")
            sleep(1)


def load_leaderboard():
    """
    load_leadeboard() function loads the list of scores from a file "leaderboard.txt" and then saved them to a list named ranking.
    """
    global ranking
    ranking = list()
    f = open("leaderboard.txt", "r")
    for line in f:
        splitted_line = line.split(":")
        name = splitted_line[0].strip()
        score = splitted_line[1].strip()
        record = (name, score)
        ranking.append(record)
    ranking.sort(key=lambda tup: int(tup[1]), reverse=True)
    f.close()
    return ranking


def add_to_leaderboard(name, score):
    """add_to_leaderboard() function adds a new highscore to the ranking and then rewrites the "leaderboard.txt" file with the updated list of the 10 best high scores ever achieved in the game."""
    global ranking
    ranking.append((name, score))
    ranking.sort(key=lambda tup: int(tup[1]), reverse=True)
    ranking = ranking[0:10]
    place = ranking.index((name, score))
    print(
        "Congratulations for beating the record, {name}!! You're now the {n}.luckiest player in the ranking!".format(
            name=name, n=place + 1
        )
    )
    sleep(2)
    f = open("leaderboard.txt", "w")
    for score in ranking:
        f.write(score[0] + " : " + str(score[1]) + "\n")
    f.close()
    return ranking


def see_leaderboard():
    """
    see_leaderboard() prints the best 10 scores for a user to see.
    """
    global ranking
    print("-----THE LUCKY 10-----")
    i = 1
    for score in ranking:
        print("{i}. {name} - {record}".format(i=i, name=score[0], record=score[1]))
        i += 1
    anything = input("Press ENTER to close the leaderboard...")


if __name__ == "__main__":
    menu()
