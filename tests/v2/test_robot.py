import pytest
import json
from heavylifter.types import Stacks, Movement
from heavylifter.v2.robot import StrongerRobot


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
            Movement(**{"box_count": 2, "src_id": 7, "dst_id": 3}),
            {
                1: ["|K|", "|A|", "|P|"],
                7: [],
                3: ["|Q|", "|U|", "|B|"],
                5: ["|F|", "|T|"],
            },
        )
    ],
)
def test_lift(stacks: Stacks, movement: Movement, expected: Stacks):
    lifted = StrongerRobot.lift(stacks=stacks, movement=movement)
    assert lifted == expected, json.dumps(lifted, indent=4)
