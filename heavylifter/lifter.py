import logging

from heavylifter.types import Robot, Stacks, Movement


def arrange_stacks(stacks: Stacks, movements: list[Movement], robot: Robot) -> Stacks:
    """Carry out instructions of moving boxes across stacks of boxes

    Args:
        stacks (Stacks): Stacks with IDs containing the boxes
        movements (list[Movement]): List of instructions on how to move the boxes
        robot (Robot): Robot object with a **lift** method

    Raises:
        ValueError: if the source or destination stack ID is not present

    Returns:
        Stacks: Stacks of boxes with IDs after the instructions were carried out
    """
    for move in movements:
        if not {move.src_id, move.dst_id}.issubset(stacks.keys()):
            err_msg = "Source or destination stack ID does not exist"
            logging.error(err_msg, extra=dict(move=move, stack_ids=list(stacks.keys())))
            raise ValueError(err_msg)

        if move.box_count > len(stacks[move.src_id]):
            logging.warning(
                msg="Box count in instruction is more than the boxes in the stack. "
                "Moving only the available number of boxes",
                extra=dict(
                    boxes_to_move=move.box_count, box_count=len(stacks[move.src_id])
                ),
            )

        stacks = robot.lift(stacks=stacks, movement=move)
    return stacks
