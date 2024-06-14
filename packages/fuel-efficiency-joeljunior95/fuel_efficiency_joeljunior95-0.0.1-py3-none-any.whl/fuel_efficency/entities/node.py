from dataclasses import dataclass, field
from typing import Protocol

from fuel_efficency.entities.position import Position


@dataclass(slots=True, frozen=True)
class Node(Protocol):
    weight: float
    position: 'Position' = field(default_factory=Position)
