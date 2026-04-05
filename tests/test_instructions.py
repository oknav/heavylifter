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
                    1: ["|B|", "|R|"],
                    2: ["|M|", "|B|", "|T|"],
                    3: ["|C|", "|L|", "|Z|"],
                    4: ["|F|", "|C|", "|S|"],
                    5: ["|H|", "|G|", "|P|"],
                    6: ["|J|", "|V|"],
                    7: ["|N|", "|L|", "|G|"],
                    8: ["|R|", "|Z|", "|M|"],
                    9: ["|L|", "|M|"],
                },
            ),
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
    def test_boxes(
        self,
        instructions_from_filename: str,
        expected: dict[str, list[str | int]],
    ):
        boxes = Instruction(instructions_from_filename).stacks
        assert boxes == expected, json.dumps(boxes, indent=4)

    @pytest.mark.parametrize(
        "instructions_from_filename, expected",
        [
            (
                "instruction_set_read_test.txt",
                [
                    {"box_count": 6, "src_stack": 1, "dst_stack": 7},
                    {"box_count": 2, "src_stack": 2, "dst_stack": 4},
                    {"box_count": 2, "src_stack": 7, "dst_stack": 4},
                    {"box_count": 6, "src_stack": 4, "dst_stack": 3},
                    {"box_count": 1, "src_stack": 5, "dst_stack": 1},
                    {"box_count": 3, "src_stack": 8, "dst_stack": 3},
                ],
            ),
            (
                "instruction_example.txt",
                [
                    {"box_count": 1, "src_stack": 3, "dst_stack": 4},
                    {"box_count": 2, "src_stack": 1, "dst_stack": 3},
                    {"box_count": 1, "src_stack": 1, "dst_stack": 2},
                    {"box_count": 2, "src_stack": 4, "dst_stack": 1},
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
