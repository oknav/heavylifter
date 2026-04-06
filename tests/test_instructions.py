from multiprocessing import Value

import pytest
import json
import re

from heavylifter.instructions import (
    Instruction,
    InvalidInputException,
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
    def test_stacks_from_file(
        self,
        instructions_from_filename: str,
        expected: dict[str, list[str | int]],
    ):
        boxes = Instruction(instructions_from_filename).stacks
        assert boxes == expected, json.dumps(boxes, indent=4)

    def test_more_ids_than_stacks(self, more_ids_than_stacks: str):
        assert Instruction(more_ids_than_stacks).stacks == {
                    1: ["|K|", "|A|", "|P|"],
                    2: ["|Q|", "|U|"],
                    3: ["|B|"],
                    4: [],
                }

    def test_more_stacks_than_ids(self, more_stacks_than_ids: str,):
        with pytest.raises(ValueError) as exc_info:
            Instruction(more_stacks_than_ids).stacks

    @pytest.mark.parametrize(
        "instructions, error_msg",
        [
            (
                "no_bottom",
                "'bottom' must be present in input instructions exactly once",
            ),
            (
                "multiple_bottom",
                "'bottom' must be present in input instructions exactly once",
            ),
            (
                "no_stack_numbers",
                "Format for numbering the stacks might be incorrect (maximum 10 stacks are allowed)",
            ),
            ("no_boxes", "There are no stacks present"),
            ("empty_boxes", "No empty boxes are allowed"),
            (
                "more_than_max_stacks",
                "Format for numbering the stacks might be incorrect (maximum 10 stacks are allowed)",
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

        assert exc_info.match(re.escape(error_msg))

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

