import random
from collections import Counter


class Player:
    points_to_win = -1
    turns_played = 0

    def __init__(self, name: str):
        self.name = name
        self.points = 0
        self.rolls_played = 0
        self.turns_played = 0

    def add_points(self, points: int):
        self.points += points
        self.rolls_played += 1
        print(f"Added {points} points to {self.name}'s score for a total of {self.points} points!")

    def check_win(self):
        return Player.points_to_win and self.points > Player.points_to_win


def score_calculator(result_of_roll: list):
    most_common = Counter(result_of_roll).most_common()

    # Creates lists; highest counting bonus and detriment,
    # reversed so that the first tuple is the highest num and count.
    bonus_list = sorted([(num, count) for num, count in most_common if num > 2],
                        key=lambda x: x[1], reverse=True)

    detriment_list = sorted([(num, count) for num, count in most_common if num < 3],
                            key=lambda x: x[1], reverse=True)

    # My solution for handling assignment in cases where there are no Detriments/Bonuses - so that rest of function
    # doesn't break.
    try:
        max_bonus_number, max_bonus_count = bonus_list[0][0], bonus_list[0][1]
    except IndexError:
        max_bonus_number = -1
        max_bonus_count = 1

    try:
        max_detriment_number, max_detriment_count = detriment_list[0][0], detriment_list[0][1]
    except IndexError:
        max_detriment_number = -1
        max_detriment_count = 1

    if max_detriment_count > 1:
        print(f"You rolled {max_detriment_count} {max_detriment_number}s. This means your score for this round will be "
              f"divided by {max_detriment_count}.")
        print("Press ENTER to continue.")
        input()

    if max_detriment_count > 1 and max_bonus_count > 1:  # Cutesy little transition if both
        print("On the bright side...\n")

    if max_bonus_count > 1:
        print(f"You rolled {max_bonus_count} {max_bonus_number}s. This means your score for this round will be "
              f"multiplied by {max_bonus_count}.")
        print("Press ENTER to continue.")
        input()

    print("Score breakdown:")
    print(f"Raw Roll: {sum(result_of_roll)}")
    print(f"Detriment Divisor: {max_detriment_count}")
    print(f"Bonus Multiplier: {max_bonus_count}")
    print("")

    score = (sum(result_of_roll) // max_detriment_count) * max_bonus_count

    print(f"Your roll, {sum(result_of_roll)}, will be divided by {max_detriment_count}, and then multiplied by "
          f"{max_bonus_count} for a score of {score}.")

    return score


def roll_die(sides: int = 6, player: Player = None):
    roll = random.randint(1, sides)
    if player:
        print(f"{player} rolled a {roll}")
    return roll


def roll_dice(dice_to_roll: int, sides: int = 6):
    roll_result = list([roll_die(sides) for i in range(dice_to_roll)])
    print(f"You rolled {dice_to_roll} dice with the resulting values:")
    print(f"{' '.join([str(num) for num in roll_result])}")
    return roll_result


def prompt_name(message: str):
    print(message)
    response = input()
    if response.isalpha():
        return response
    else:
        print("(alpha only please)")
        prompt_name(message)


def choose_num_dice():
    numDice = roll_die()
    print(f"You rolled a {numDice}.")
    if ask_yn(f"You will roll {numDice} dice.\nWould you like to roll again to decide the number "
              f"of dice you roll ONCE?"):
        numDice = roll_die()
        print(f"Result of roll is {numDice}. ENTER to continue.")
        input()

    print(f"You will roll {numDice} dice this turn. ENTER to continue.")
    input()
    return numDice


def first_move():
    pOneRoll = roll_die()
    print(f"Player One rolled a {pOneRoll}.")
    pTwoRoll = roll_die()
    print(f"Player Two rolled a {pTwoRoll}")

    if pOneRoll == pTwoRoll:
        print("Tie, re-rolling")
        first_move()
    elif pOneRoll > pTwoRoll:
        return True
    else:
        return False


def ask_yn(message: str):
    while True:
        print(f"{message} (y/n)")

        try:
            response = input().lower()[0]
        except IndexError:
            print("Please enter a response.")
            continue

        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Please be clear")


def prompt_int(message: str, acceptable_values: range):
    while True:
        print(f"{message} ({min(acceptable_values)}-{max(acceptable_values)})")

        response = input()

        try:
            response = int(response)
        except ValueError:
            continue

        if response in acceptable_values:
            return response

        print("Please enter a valid number.")


def gameplay_loop(activePlayer: Player):
    diceToRoll = choose_num_dice()
    scoreCalc = score_calculator(roll_dice(diceToRoll))
    activePlayer.add_points(scoreCalc)

    print("ENTER to continue.")
    input()

    Player.turns_played += 1

    if Player.turns_played == 1:
        # noinspection SpellCheckingInspection
        winscore = decide_win_score(activePlayer.points)
        print(f"Score to win will be set to {winscore} for this game.")

        Player.points_to_win = winscore

        print("ENTER to continue.")
        input()
    return roll_again(diceToRoll)


def decide_win_score(points):
    print("(First move, will now decide score required to win game.)")
    sides = prompt_int("Please select a num 3-15. "
                       "This will roll a dice with that many sides to decide winning score.", range(3, 16))

    multiplier = roll_die(sides)

    while multiplier == 1:  # Got a bug fix for this code from ChatGPT. That thing is WILD.
        print("Rolled a 1, re-rolling.")
        multiplier = roll_die(sides)
        print(f"You rolled a {multiplier}.")
        if multiplier != 1:
            break  # break will skip else, thus not ingrepeat

    else:
        print(f"You rolled a {multiplier}")

    return points * multiplier


def on_win(winningPlayer: Player, losingPlayer: Player):
    # noinspection SpellCheckingInspection
    def close_match(scorediff):
        if scorediff < 16:
            return "Close match!"
        else:
            return ""

    scoreDiff = winningPlayer.points - losingPlayer.points

    print(f"Congrats, {winningPlayer.name}! You won this game with {winningPlayer.points} points!")
    print(f"You won on turn {Player.turns_played}, and {losingPlayer.name} was "
          f"{Player.points_to_win - losingPlayer.points} points behind you. {close_match(scoreDiff)}")
    exit()


def roll_again(numDice: int):
    print(f"You will now roll the same amount of dice you just rolled ({numDice}) "
          f"again to decide if you will get another turn.")
    print()

    resultRollAgain = roll_dice(numDice)

    if len(set(resultRollAgain)) == 1:
        print(f"You rolled all {resultRollAgain[0]}s! You will roll again.")
        print("ENTER to continue.")
        input()
        return True
    else:
        print("You will not roll again. TIP: With lower numbers of dice, you score lower,"
              " but are more likely to roll again!")
        print("ENTER to continue.")
        input()
        return False


def main():
    if not ask_yn("This is a game of many dice and conditions. You will work to roll dice, avoid low rolls\n"
                  "< 3 (as they will be counted as detriments), and aim for high rolls > 3 (as these will\n"
                  "count as bonuses. You will roll for the number of dice that you would like to roll, and will be\n"
                  "given the option to roll this number of dice again. This is a strategic option, as later in your\n"
                  "turn you will roll this same number of dice again to decide whether you will get another turn,\n"
                  "thus skipping your opponent for the turn. You will also be prompted to roll a d(3-15, your choice)\n"
                  "die that will multiply the current score to decide the winning score based off of the first roll.\n"
                  "Gameplay stages are also commented so that you will see what is happening throughout the game.\n"
                  "Are you ready to play?"):
        print("Alright, see you when you're ready!")
        exit()

    pOne = Player(prompt_name("Player One Name:"))
    pTwo = Player(prompt_name("Player Two Name:"))

    print("Rolling to decide first player. ENTER to continue.")
    input()
    if first_move():
        activePlayer = pOne
        inactivePlayer = pTwo
    else:
        activePlayer = pTwo
        inactivePlayer = pOne

    while True:
        if Player.turns_played > 0:
            if pOne.check_win():  # This chunk is fairly self-documenting
                on_win(pOne, pTwo)
            elif pTwo.check_win():
                on_win(pTwo, pOne)

            print("********************")  # Recaps points after every turn except the first.
            print(f"{pOne.name} score: {pOne.points}. {Player.points_to_win - pOne.points} points to win!")
            print(f"{pTwo.name} score: {pTwo.points}. {Player.points_to_win - pTwo.points} points to win!")
            print("********************")

            print()

        print(f"{activePlayer.name}'s turn.")
        print("ENTER to continue.")
        input()
        if gameplay_loop(activePlayer):  # Will return true if it is next player's turn
            continue
        else:
            activePlayer, inactivePlayer = inactivePlayer, activePlayer  # Swaps players


def test():  # To take place of main for testing implementation of Counter in score_calculator()
    test_roll = [1, 1, 1, 3, 3]

    print(score_calculator(test_roll))


if __name__ == "__main__":
    main()
