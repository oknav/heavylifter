from copy import copy

from heavylifter.types import Movement, Robot, Stacks


class StrongerRobot(Robot):
    @staticmethod
    def lift(stacks: Stacks, movement: Movement) -> Stacks:
        """Lift given number of boxes at once from the front of the source stack at once and place it to the front of the destination stack

        Args:
            stacks (Stacks): Stacks with IDs containing the boxes
            movement (Movement): Instruction for the current movement

        Returns:
            Stacks: Stacks of boxes with IDs after the instruction was carried out
        """
        result_stacks = copy(stacks)
        result_stacks[movement.dst_id] = (
            result_stacks[movement.src_id][: movement.box_count]
            + result_stacks[movement.dst_id]
        )
        result_stacks[movement.src_id] = result_stacks[movement.src_id][
            movement.box_count :
        ]

        return result_stacks
