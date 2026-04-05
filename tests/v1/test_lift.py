import pytest
import json
from heavylifter.instructions import Stacks, Movement
from heavylifter.v1.lift import lift


@pytest.mark.parametrize(
    "boxes, movements, expected",
    [
        (
            {
                "number_of_stacks": 4,
                "stacks": [
                    ["|K|", "|A|", "|P|"],
                    ["|Q|", "|U|"],
                    ["|B|"],
                    ["|F|", "|T|"],
                ],
            },
            [
                {"num_of_boxes": 1, "src_stack": 3, "dst_stack": 4},
                {"num_of_boxes": 2, "src_stack": 1, "dst_stack": 3},
                {"num_of_boxes": 1, "src_stack": 1, "dst_stack": 2},
                {"num_of_boxes": 2, "src_stack": 4, "dst_stack": 1},
            ],
            {
                "number_of_stacks": 4,
                "stacks": [
                    ["|F|", "|B|"],
                    ["|P|", "|Q|", "|U|"],
                    ["|A|", "|K|"],
                    ["|T|"],
                ],
            },
        )
    ],
)
def test_lift(boxes: Stacks, movements: list[Movement], expected: Stacks):
    assert lift(boxes, movements) == expected, json.dumps(expected)
