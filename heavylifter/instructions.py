from functools import cached_property
import logging
from typing import TypedDict
import re


class InvalidInputException(Exception):
    pass


Stacks = list[list[str]]


class Movement(TypedDict):
    box_count: int
    src_stack: int
    dst_stack: int


def _open_file(abs_path: str) -> str:
    """Read lines from file into a string

    Args:
        abs_path (str): Absolute path of the file to read

    Returns:
        str: Content of the file
    """
    try:
        with open(abs_path, "r") as f:
            return f.read()
    except OSError:
        logging.error(msg="File could not be opened", exc_info=True)

    return ""


### Validation:
# bottom is present
# stack validation:
#   letters between | | are unique
#   no empty boxes
#   no more than 10 stacks
#   boxes (and 3-whitespaces) seperated by 1 space
#
# move validation:
#   move #\d from #\dt to #\d (check if stack exists?)
# NOTE: what happens, when there are not enough boxes in stack -- gonna stop moving


class Instruction:
    def __init__(self, instructions: str):
        self._boxes, self._movements = self._split_instructions(instructions)

    @staticmethod
    def _clean_lines(lines: list[str]):
        return [line for line in lines if line.strip()]

    @classmethod
    def _split_instructions(cls, instructions: str) -> tuple[list[str], list[str]]:
        """Splits the input instructions into two groups, details about the boxes
        and the movements.

        Args:
            instructions (str): String instructions

        Returns:
            tuple[list[str], list[str]]: Returns a tuple with the lines containing
            information about the `boxes` and `movements`
        """

        instruction_split = re.split(pattern="bottom", string=instructions)
        return (
            cls._clean_lines(instruction_split[0].splitlines()),
            cls._clean_lines(instruction_split[1].splitlines()),
        )

    @cached_property
    def boxes(self) -> Stacks:
        # pattern to ensure empty spots in stack get parsed as well
        box_pattern = re.compile(r"(\s{3}|\|[A-Z]\|)\s?")

        # pop last stack as it containes the number of stacks
        self._boxes.pop(-1)

        stacks_by_row = [
            re.findall(pattern=box_pattern, string=_boxes) for _boxes in self._boxes
        ]
        transposed_stacks = [
            list([box for box in row if box.strip()]) for row in zip(*stacks_by_row)
        ]

        return transposed_stacks

    @cached_property
    def movements(self) -> list[Movement]:
        match_all_numbers = r"\d"

        movements = []
        for move in self._movements:
            if not move.strip():
                continue

            # regex match the numbers, assign them in order to Movement dict
            numbers = re.findall(pattern=match_all_numbers, string=move)
            movements.append(
                Movement(
                    box_count=int(numbers[0]),
                    src_stack=int(numbers[1]),
                    dst_stack=int(numbers[2]),
                )
            )

        return movements


def transpose_result_stacks(stacks: Stacks):
    empty_box = "   "
    max_box_count = max(len(stack) for stack in stacks)

    result_stack = [
        [empty_box] * (max_box_count - len(stack)) + stack for stack in stacks
    ]
    return [list(row) for row in zip(*result_stack)]
