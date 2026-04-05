from heavylifter.instructions import Stacks, Movement


def lift(stacks: Stacks, movements: list[Movement]):
    for move in movements:
        box_count = move["box_count"]
        src_stack_index = move["src_stack"] - 1
        dst_stack_index = move["dst_stack"] - 1

        stacks[dst_stack_index] = (
            stacks[src_stack_index][:box_count] + stacks[dst_stack_index]
        )
        stacks[src_stack_index] = stacks[src_stack_index][box_count:]

    return stacks
