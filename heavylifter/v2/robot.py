from copy import copy

from heavylifter.types import Movement, Robot, Stacks


class StrongerRobot(Robot):
    @staticmethod
    def lift(stacks: Stacks, movement: Movement) -> Stacks:
        result_stacks = copy(stacks)
        result_stacks[movement.dst_id] = (
            result_stacks[movement.src_id][: movement.box_count]
            + result_stacks[movement.dst_id]
        )
        result_stacks[movement.src_id] = result_stacks[movement.src_id][
            movement.box_count :
        ]

        return result_stacks
