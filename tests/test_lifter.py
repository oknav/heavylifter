from unittest.mock import Mock

import pytest
import json
from heavylifter.types import Stacks, Movement
from heavylifter.lifter import Robot, arrange_stacks, transpose_result_stacks
from heavylifter.v1.robot import LimitedRobot
from heavylifter.v2.robot import StrongerRobot


@pytest.mark.parametrize(
    "stacks, movements, robot, expected",
    [
        (
            {
                1: ["|K|", "|A|", "|P|"],
                2: ["|Q|", "|U|"],
                3: ["|B|"],
                4: ["|F|", "|T|"],
            },
            [
                Movement(**{"box_count": 1, "src_id": 3, "dst_id": 4}),
                Movement(**{"box_count": 2, "src_id": 1, "dst_id": 3}),
                Movement(**{"box_count": 1, "src_id": 1, "dst_id": 2}),
                Movement(**{"box_count": 2, "src_id": 4, "dst_id": 1}),
            ],
            StrongerRobot,
            {
                1: ["|B|", "|F|"],
                2: ["|P|", "|Q|", "|U|"],
                3: ["|K|", "|A|"],
                4: ["|T|"],
            },
        ),
        (
            {
                1: ["|K|", "|A|", "|P|"],
                2: ["|Q|", "|U|"],
                3: ["|B|"],
                4: ["|F|", "|T|"],
            },
            [
                Movement(**{"box_count": 1, "src_id": 3, "dst_id": 4}),
                Movement(**{"box_count": 2, "src_id": 1, "dst_id": 3}),
                Movement(**{"box_count": 1, "src_id": 1, "dst_id": 2}),
                Movement(**{"box_count": 2, "src_id": 4, "dst_id": 1}),
            ],
            LimitedRobot,
            {
                1: ["|F|", "|B|"],
                2: ["|P|", "|Q|", "|U|"],
                3: ["|A|", "|K|"],
                4: ["|T|"],
            },
        ),
    ],
)
def test_arrange_stacks(
    stacks: Stacks, movements: list[Movement], robot: Robot, expected: Stacks
):
    lifted = arrange_stacks(stacks, movements, robot)
    assert lifted == expected, json.dumps(lifted, indent=4)


@pytest.mark.parametrize("robot", (LimitedRobot, StrongerRobot))
def test_no_movements(robot: Robot):
    movements = []
    stacks = {
        1: ["|K|", "|A|", "|P|"],
        2: ["|Q|", "|U|"],
        3: ["|B|"],
        4: ["|F|", "|T|"],
    }

    lifted = arrange_stacks(stacks, movements, robot)
    assert lifted == {
        1: ["|K|", "|A|", "|P|"],
        2: ["|Q|", "|U|"],
        3: ["|B|"],
        4: ["|F|", "|T|"],
    }, json.dumps(lifted, indent=4)


@pytest.mark.parametrize(
    "movements",
    [
        pytest.param(
            [
                Movement(**{"box_count": 1, "src_id": 3, "dst_id": 4}),
                Movement(**{"box_count": 2, "src_id": 34, "dst_id": 3}),
                Movement(**{"box_count": 1, "src_id": 1, "dst_id": 2}),
            ],
            id="invalid src_id",
        ),
        pytest.param(
            [
                Movement(**{"box_count": 1, "src_id": 3, "dst_id": 4}),
                Movement(**{"box_count": 2, "src_id": 1, "dst_id": 3}),
                Movement(**{"box_count": 1, "src_id": 1, "dst_id": 78}),
                Movement(**{"box_count": 2, "src_id": 4, "dst_id": 1}),
            ],
            id="invalid dst_id",
        ),
    ],
)
def test_invalid_stack_ids(movements: list[Movement]):
    stacks = {
        1: ["|K|", "|A|", "|P|"],
        2: ["|Q|", "|U|"],
        3: ["|B|"],
        4: ["|F|", "|T|"],
    }
    mock_robot = Mock(spec=LimitedRobot)
    mock_robot.lift.return_value = stacks

    with pytest.raises(ValueError) as exc_info:
        arrange_stacks(stacks=stacks, movements=movements, robot=mock_robot)

    assert exc_info.match("Source or destination stack ID does not exist")

@pytest.mark.parametrize(
    "result_boxes, expected",
    [
        (
            [
                ["|F|", "|B|"],
                ["|P|", "|Q|", "|U|"],
                ["|A|", "|K|"],
                ["|T|"],
            ],
            [
                ["   ", "|P|", "   ", "   "],
                ["|F|", "|Q|", "|A|", "   "],
                ["|B|", "|U|", "|K|", "|T|"],
            ],
        )
    ],
)
def test_result_transpose(result_boxes: list[list[str]], expected: list[list[str]]):
    result = transpose_result_stacks(stacks=result_boxes)
    assert result == expected, json.dumps(result, indent=4)
