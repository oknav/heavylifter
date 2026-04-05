import pytest
import json
from heavylifter.instructions import Stacks, Movement
from heavylifter.v1.lift import lift


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
                ["|F|", "|B|"],
                ["|P|", "|Q|", "|U|"],
                ["|A|", "|K|"],
                ["|T|"],
            ],
        )
    ],
)
def test_lift(boxes: Stacks, movements: list[Movement], expected: Stacks):
    assert lift(boxes, movements) == expected, json.dumps(expected)
