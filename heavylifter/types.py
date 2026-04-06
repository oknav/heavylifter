from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class Movement:
    box_count: int
    src_id: int
    dst_id: int


Stacks = dict[int, list[str]]


class Robot(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def lift(stacks: Stacks, movement: Movement) -> Stacks: ...
