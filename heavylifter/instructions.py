from functools import cached_property
import logging
from typing import TypedDict
import re


class InvalidInputException(Exception):
    pass


Stacks = dict[int, list[list[str]]]


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


def _pre_validate(instructions: str) -> bool:
    bottoms = re.findall("bottom", instructions)
    if not len(bottoms) == 1:
        raise InvalidInputException(
            "'bottom' must be present in input instructions exactly once"
        )

    if re.match(pattern=r"\|\|", string=instructions):
        raise InvalidInputException("No empty boxes are allowed")

    return True


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
        _pre_validate(instructions)
        self._stacks, self._movements = self._clean_instructions(instructions)

    @staticmethod
    def _filter_empty(lines: list[str]):
        return [line for line in lines if line.strip()]

    @classmethod
    def _split_instructions(cls, instructions: str) -> tuple[list[str], list[str]]:
        """Splits the input instructions into two groups, details about the stacks
        and the movements.

        Args:
            instructions (str): String instructions

        Returns:
            tuple[list[str], list[str]]: Returns a tuple with the lines containing
            information about the `stacks` and `movements`
        """

        instruction_split = re.split(pattern="bottom", string=instructions)
        return (
            cls._filter_empty(instruction_split[0].splitlines()),
            cls._filter_empty(instruction_split[1].splitlines()),
        )

    @staticmethod
    def _validate_stacks(stacks: list[str]):
        # last row should contain stack numbers less than 10
        stack_number_row = stacks[-1].strip()

        # match for exactly 1 number in row or at most 9 numbers with 3 whitespaces and a number at the end
        if not re.match(
            pattern=r"^(\d+)$|^(\d+\s{3}){1,9}\d+$",
            string=stack_number_row,
        ):
            raise InvalidInputException(
                "Format for numbering the stacks might be incorrect (maximum 10 stacks are allowed)"
            )

        # check if boxes are unique
        labelled_boxes = re.findall(pattern=r"(\|[A-Z]\|)", string="\n".join(stacks))

        if len(labelled_boxes) != len(set(labelled_boxes)):
            raise InvalidInputException("Box labels must be globally unique")

    @staticmethod
    def _validate_movements(movements: list[str]):
        if not all(
            re.fullmatch(pattern=r"^move \d+ from \d+ to \d+$", string=movement)
            for movement in movements
        ):
            raise InvalidInputException(
                "Movement instructions must match format of 'move #1 from #2 to #3'"
            )

    def _clean_instructions(self, instructions: str) -> tuple[list[str], list[str]]:
        stacks_raw, movements_raw = self._split_instructions(instructions)
        self._validate_stacks(stacks=stacks_raw)
        self._validate_movements(movements=movements_raw)

        return stacks_raw, movements_raw

    @cached_property
    def stacks(self) -> Stacks:
        # get numbers only from string
        stack_numbers = map(
            int, re.findall(pattern=r"\d+", string=self._stacks.pop(-1))
        )

        # pattern to ensure empty spots in stack get parsed as well
        box_pattern = re.compile(r"(\s{3}|\|[A-Z]\|)\s?")

        stacks_by_row = [
            re.findall(pattern=box_pattern, string=_stacks) for _stacks in self._stacks
        ]
        transposed_stacks = [
            list([box for box in row if box.strip()]) for row in zip(*stacks_by_row)
        ]

        return dict(zip(stack_numbers, transposed_stacks))

    @cached_property
    def movements(self) -> list[Movement]:
        match_all_numbers = r"\d+"

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


def transpose_result_stacks(stacks: list[list[str]]):
    empty_box = "   "
    max_box_count = max(len(stack) for stack in stacks)

    result_stack = [
        [empty_box] * (max_box_count - len(stack)) + stack for stack in stacks
    ]
    return [list(row) for row in zip(*result_stack)]
