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
    bonus_list = sorted([(num, count) for num, count in most_common if num > 2]
                        , key=lambda x: x[1], reverse=True)

    detriment_list = sorted([(num, count) for num, count in most_common if num < 3]
                            , key=lambda x: x[1], reverse=True)

    # My solution for handling assignment in cases where there are no Detriments/Bonuses - so that rest of function
    # doesn't break.
    try:
        max_bonus_number, max_bonus_count = bonus_list[0][0], bonus_list[0][1]
    except IndexError:
        max_bonus_count = 1

    try:
        max_detriment_number, max_detriment_count = detriment_list[0][0], detriment_list[0][1]
    except IndexError:
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
            break  # break will skip else, thus not repeating itself

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
    list = [1, 1, 1, 3, 3]

    score_calculator(list)


if __name__ == "__main__":
    main()
