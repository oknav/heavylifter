import argparse
from heavylifter.instructions import Instruction
import logging

from heavylifter.lifter import arrange_stacks, transpose_result_stacks
from heavylifter.types import Stacks
from heavylifter.v1.robot import LimitedRobot
from heavylifter.v2.robot import StrongerRobot


def _pretty_print_result(stacks: Stacks):

    str_stack_rows = [
        " ".join(stack) for stack in transpose_result_stacks(list(stacks.values()))
    ]
    str_stacks = "\n".join(str_stack_rows)
    stack_numbers = "   ".join(map(str, stacks.keys()))
    mid_position = int((len(stack_numbers) + 2) / 2)

    print(str_stacks)
    print(" " + stack_numbers + " ")
    print((mid_position - 3) * " " + "bottom")


def main():
    parser = argparse.ArgumentParser(
        prog="HeavyLifter",
        description="Moves boxes between stacks",
        epilog="""The robot has to be fed an *instruction set file* 
        containing the starting state as a pictogram followed by the 
        instructions to be carried out in order. There are TWO available versions to use.""",
    )
    parser.add_argument("filepath", help="absolute path to the input instruction file")
    parser.add_argument(
        "--version",
        default="v1",
        choices=["v1", "v2"],
        help="the version of the lifter to use",
    )

    parsed = parser.parse_args()

    try:
        with open(parsed.filepath, "r") as f:
            file_content = f.read()
    except OSError:
        logging.error("Could not open file", exc_info=True)
        return

    match parsed.version:
        case "v1":
            robot = LimitedRobot()
        case "v2":
            robot = StrongerRobot()
        case _:
            logging.error("Invalid robot version")
            return

    instruction = Instruction(file_content)
    try:
        arranged_stacks = arrange_stacks(
            stacks=instruction.stacks, movements=instruction.movements, robot=robot
        )
        _pretty_print_result(stacks=arranged_stacks)
    except ValueError:
        logging.error(msg="Error occured when moving boxes", exc_info=True)


if __name__ == "__main__":
    main()
