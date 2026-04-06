from copy import copy

from heavylifter.types import Movement, Robot, Stacks


class LimitedRobot(Robot):
    @staticmethod
    def lift(stacks: Stacks, movement: Movement) -> Stacks:
        """Lift 1 box at a time from the front of the source stack at once and place it to the front of the destination stack as many times as the instruction states

        Args:
            stacks (Stacks): Stacks with IDs containing the boxes
            movement (Movement): Instruction for the current movement

        Returns:
            Stacks: Stacks of boxes with IDs after the instruction was carried out
        """
        result_stacks = copy(stacks)

        # if the instruction box count exceeds the actual number of boxes in the source stack, move the available boxes only
        lift_count = min(movement.box_count, len(result_stacks[movement.src_id]))
        for _ in range(lift_count):
            result_stacks[movement.dst_id] = [
                result_stacks[movement.src_id].pop(0)
            ] + result_stacks[movement.dst_id]
        return result_stacks
