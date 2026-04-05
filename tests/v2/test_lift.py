import pytest
import json
from heavylifter.instructions import Stacks, Movement
from heavylifter.v2.lift import lift


@pytest.mark.parametrize(
    "boxes, movements, expected",
    [
        (
            [
                ["|K|", "|A|", "|P|"],
                ["|Q|", "|U|"],
                ["|B|"],
                ["|F|", "|T|"],
            ],
            [
                {"box_count": 1, "src_stack": 3, "dst_stack": 4},
                {"box_count": 2, "src_stack": 1, "dst_stack": 3},
                {"box_count": 1, "src_stack": 1, "dst_stack": 2},
                {"box_count": 2, "src_stack": 4, "dst_stack": 1},
            ],
            [
                ["|B|", "|F|"],
                ["|P|", "|Q|", "|U|"],
                ["|K|", "|A|"],
                ["|T|"],
            ],
        )
    ],
)
def test_lift(boxes: Stacks, movements: list[Movement], expected: Stacks):
    lifted = lift(boxes, movements)
    assert lifted == expected, json.dumps(lifted, indent=4)
