import pytest
import json

from heavylifter.instructions import Instruction, transpose_result_stacks


class TestInstructionParsing:
    @pytest.mark.parametrize(
        "instructions_from_filename, expected",
        [
            (
                "instruction_set_read_test.txt",
                {
                    "number_of_stacks": 9,
                    "stacks": [
                        ["|B|", "|R|"],
                        ["|M|", "|B|", "|T|"],
                        ["|C|", "|L|", "|Z|"],
                        ["|F|", "|C|", "|S|"],
                        ["|H|", "|G|", "|P|"],
                        ["|J|", "|V|"],
                        ["|N|", "|L|", "|G|"],
                        ["|R|", "|Z|", "|M|"],
                        ["|L|", "|M|"],
                    ],
                },
            ),
            (
                "instruction_example.txt",
                {
                    "number_of_stacks": 4,
                    "stacks": [
                        ["|K|", "|A|", "|P|"],
                        ["|Q|", "|U|"],
                        ["|B|"],
                        ["|F|", "|T|"],
                    ],
                },
            ),
        ],
        indirect=["instructions_from_filename"],
    )
    def test_boxes(
        self,
        instructions_from_filename: str,
        expected: dict[str, list[str | int]],
    ):
        boxes = Instruction(instructions_from_filename).boxes
        assert boxes == expected, json.dumps(boxes, indent=4)

    @pytest.mark.parametrize(
        "instructions_from_filename, expected",
        [
            (
                "instruction_set_read_test.txt",
                [
                    {"num_of_boxes": 6, "src_stack": 1, "dst_stack": 7},
                    {"num_of_boxes": 2, "src_stack": 2, "dst_stack": 4},
                    {"num_of_boxes": 2, "src_stack": 7, "dst_stack": 4},
                    {"num_of_boxes": 6, "src_stack": 4, "dst_stack": 3},
                    {"num_of_boxes": 1, "src_stack": 5, "dst_stack": 1},
                    {"num_of_boxes": 3, "src_stack": 8, "dst_stack": 3},
                ],
            ),
            (
                "instruction_example.txt",
                [
                    {"num_of_boxes": 1, "src_stack": 3, "dst_stack": 4},
                    {"num_of_boxes": 2, "src_stack": 1, "dst_stack": 3},
                    {"num_of_boxes": 1, "src_stack": 1, "dst_stack": 2},
                    {"num_of_boxes": 2, "src_stack": 4, "dst_stack": 1},
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
            {
                "number_of_stacks": 4,
                "stacks": [
                    ["|F|", "|B|"],
                    ["|P|", "|Q|", "|U|"],
                    ["|A|", "|K|"],
                    ["|T|"],
                ],
            },
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
