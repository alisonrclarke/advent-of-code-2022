from enum import Enum
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day02_test_input.txt" if test_mode else f"day02_input.txt"
data = utils.input_as_lines(input_file)


class RPSOutcome(Enum):
    WIN = 6
    DRAW = 3
    LOSE = 0


class RPSHand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def get_winner(self) -> "RPSHand":
        if self == RPSHand.ROCK:
            return RPSHand.PAPER
        elif self == RPSHand.PAPER:
            return RPSHand.SCISSORS
        else:
            return RPSHand.ROCK

    def get_loser(self) -> "RPSHand":
        if self == RPSHand.ROCK:
            return RPSHand.SCISSORS
        elif self == RPSHand.PAPER:
            return RPSHand.ROCK
        else:
            return RPSHand.PAPER

    @staticmethod
    def get_score_part_1(opponent_hand: "RPSHand", my_hand: "RPSHand") -> int:
        score = my_hand.value
        if opponent_hand == my_hand:
            # Draw
            score += RPSOutcome.DRAW.value
        elif opponent_hand.get_winner() == my_hand:
            # my hand wins
            score += RPSOutcome.WIN.value

        return score

    @staticmethod
    def get_score_part_2(opponent_hand: "RPSHand", aim: RPSOutcome) -> int:
        if aim == RPSOutcome.DRAW:
            my_hand = opponent_hand
        elif aim == RPSOutcome.WIN:
            my_hand = opponent_hand.get_winner()
        else:
            my_hand = opponent_hand.get_loser()

        return aim.value + my_hand.value


opponent_codes = {"A": RPSHand.ROCK, "B": RPSHand.PAPER, "C": RPSHand.SCISSORS}

# Part 1
my_codes = {"X": RPSHand.ROCK, "Y": RPSHand.PAPER, "Z": RPSHand.SCISSORS}

total_score = 0
for line in data:
    opponent_code, my_code = line.split(" ")
    total_score += RPSHand.get_score_part_1(
        opponent_codes[opponent_code], my_codes[my_code]
    )

print(f"Part 1: {total_score}")

# Part 2
aim_codes = {"X": RPSOutcome.LOSE, "Y": RPSOutcome.DRAW, "Z": RPSOutcome.WIN}
total_score = 0
for line in data:
    opponent_code, my_code = line.split(" ")
    total_score += RPSHand.get_score_part_2(
        opponent_codes[opponent_code], aim_codes[my_code]
    )

print(f"Part 2: {total_score}")
