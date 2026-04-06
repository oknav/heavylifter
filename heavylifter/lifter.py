import logging

from heavylifter.types import Robot, Stacks, Movement


def arrange_stacks(stacks: Stacks, movements: list[Movement], robot: Robot) -> Stacks:
    for move in movements:
        if move.box_count > len(stacks[move.src_id]):
            logging.warning(
                msg="Box count in instruction is more than the boxes in the stack. "
                "Moving only the available number of boxes",
                extra=dict(
                    boxes_to_move=move.box_count, box_count=len(stacks[move.src_id])
                ),
            )

        if not {move.src_id, move.dst_id}.issubset(stacks.keys()):
            err_msg = "Source or destination stack ID does not exist"
            logging.error(err_msg, extra=dict(move=move, stack_ids=list(stacks.keys())))
            raise ValueError(err_msg)

        stacks = robot.lift(stacks=stacks, movement=move)
    return stacks
