import logging
from typing import TypeVar

from heavylifter.instructions import Stacks, Movement
from heavylifter.v1.robot import LimitedRobot
from heavylifter.v2.robot import StrongerRobot

Robot = TypeVar("Robot", LimitedRobot, StrongerRobot)


def arrange_stacks(stacks: Stacks, movements: list[Movement], robot: Robot):
    for move in movements:
        if move.box_count > len(stacks[move.src_id]) - 1:
            logging.warning(
                msg="Box count in instruction is more than the boxes in the stack. "
                "Moving only the available number of boxes"
            )

        if not {move.src_id, move.dst_id}.issubset(stacks.keys()):
            err_msg = "Source or destination stack ID does not exist"
            logging.error(err_msg, extra=dict(move=move, stack_ids=list(stacks.keys())))
            raise ValueError(err_msg)

        stacks = robot.lift(stacks=stacks, movement=move)
    return stacks
