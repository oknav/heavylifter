from copy import copy

from heavylifter.instructions import Stacks
from heavylifter.types import Movement, Robot


class LimitedRobot(Robot):
    @staticmethod
    def lift(stacks: Stacks, movement: Movement) -> Stacks:
        result_stacks = copy(stacks)
        for _ in range(min(movement.box_count, len(result_stacks[movement.src_id]))):
            result_stacks[movement.dst_id] = [
                result_stacks[movement.src_id].pop(0)
            ] + result_stacks[movement.dst_id]
        return result_stacks
