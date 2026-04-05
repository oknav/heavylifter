from heavylifter.instructions import Stacks, Movement


def lift(boxes: Stacks, movements: list[Movement]):
    stacks: list[list[str]] = boxes["stacks"]

    for move in movements:
        box_count = move["box_count"]
        src_stack_index = move["src_stack"] - 1
        dst_stack_index = move["dst_stack"] - 1

        for _ in range(box_count):
            stacks[dst_stack_index] = [stacks[src_stack_index].pop(0)] + stacks[
                dst_stack_index
            ]

    return boxes
