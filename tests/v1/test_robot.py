import pytest
import json
from heavylifter.instructions import Stacks, Movement
from heavylifter.v1.robot import LimitedRobot


@pytest.mark.parametrize(
    "stacks, movement, expected",
    [
        (
            {
                1: ["|K|", "|A|", "|P|"],
                7: ["|Q|", "|U|"],
                3: ["|B|"],
                5: ["|F|", "|T|"],
            },
            Movement(**{"box_count": 1, "src_id": 3, "dst_id": 5}),
            {
                1: ["|K|", "|A|", "|P|"],
                7: ["|Q|", "|U|"],
                3: [],
                5: ["|B|", "|F|", "|T|"],
            },
        )
    ],
)
def test_lift(stacks: Stacks, movement: Movement, expected: Stacks):
    lifted = LimitedRobot.lift(stacks=stacks, movement=movement)
    assert lifted == expected, json.dumps(lifted, indent=4)
