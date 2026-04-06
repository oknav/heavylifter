import pytest
import json

from heavylifter.instructions import (
    Instruction,
    InvalidInputException,
    transpose_result_stacks,
)
from heavylifter.types import Movement


class TestInstructionParsing:
    @pytest.mark.parametrize(
        "instructions_from_filename, expected",
        [
            (
                "instruction_example.txt",
                {
                    1: ["|K|", "|A|", "|P|"],
                    2: ["|Q|", "|U|"],
                    3: ["|B|"],
                    4: ["|F|", "|T|"],
                },
            ),
        ],
        indirect=["instructions_from_filename"],
    )
    def test_stacks(
        self,
        instructions_from_filename: str,
        expected: dict[str, list[str | int]],
    ):
        boxes = Instruction(instructions_from_filename).stacks
        assert boxes == expected, json.dumps(boxes, indent=4)

    @pytest.mark.parametrize(
        "instructions, error_msg",
        [
            (
                "no_bottom",
                "'bottom' must be present in input instructions exactly once",
            ),
            (
                "no_stack_numbers",
                "Format for numbering the stacks might be incorrect \(maximum 10 stacks are allowed\)",
            ),
            ("no_boxes", "There are no stacks present"),
            ("empty_boxes", "No empty boxes are allowed"),
            (
                "more_than_max_stacks",
                "Format for numbering the stacks might be incorrect \(maximum 10 stacks are allowed\)",
            ),
            (
                "invalid_movements",
                "Movement instructions must match format of 'move #1 from #2 to #3'",
            ),
        ],
    )
    def test_invalid_instructions(self, instructions: str, error_msg: str, request):
        with pytest.raises(InvalidInputException) as exc_info:
            Instruction(request.getfixturevalue(instructions))

        assert exc_info.match(error_msg)

    def test_no_movements(self, no_movements: str):
        movements = Instruction(no_movements).movements
        assert len(movements) == 0

    @pytest.mark.parametrize(
        "instructions_from_filename, expected",
        [
            (
                "instruction_example.txt",
                [
                    Movement(**{"box_count": 1, "src_id": 3, "dst_id": 4}),
                    Movement(**{"box_count": 2, "src_id": 1, "dst_id": 3}),
                    Movement(**{"box_count": 1, "src_id": 1, "dst_id": 2}),
                    Movement(**{"box_count": 2, "src_id": 4, "dst_id": 1}),
                ],
            ),
        ],
        indirect=["instructions_from_filename"],
    )
    def test_movements(
        self, instructions_from_filename: str, expected: list[dict[str, int]]
    ):
        movements = Instruction(instructions_from_filename).movements
        assert movements == expected, json.dumps(movements, indent=4)


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
def test_result_transpose(result_boxes, expected):
    result = transpose_result_stacks(stacks=result_boxes)
    assert result == expected, json.dumps(result, indent=4)
