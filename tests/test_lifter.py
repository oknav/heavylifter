import pytest
import json
from heavylifter.types import Stacks, Movement
from heavylifter.lifter import Robot, arrange_stacks
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
