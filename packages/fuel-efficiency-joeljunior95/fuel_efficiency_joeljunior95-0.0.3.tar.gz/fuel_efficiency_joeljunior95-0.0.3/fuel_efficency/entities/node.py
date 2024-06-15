from dataclasses import dataclass, field
from typing import Protocol

from fuel_efficency.entities.position import Position


@dataclass(slots=True, frozen=True)
class Node(Protocol):
    weight: float
    position: 'Position' = field(default_factory=Position)

    def __lt__(self, other: 'Node'):
        try:
            return self.weight < other.weight
        except:
            raise NotImplementedError("Missing `weight` attribute")

    def __eq__(self, other: 'Node'):
        try:
            return self.weight == other.weight and self.position == other.position
        except:
            raise NotImplementedError("Missing `position` or `weight` attribute")
