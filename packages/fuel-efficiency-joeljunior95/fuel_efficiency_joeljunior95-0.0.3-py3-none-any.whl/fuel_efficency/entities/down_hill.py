from dataclasses import dataclass, field

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


@dataclass(slots=True, frozen=True, eq=False)
class DownHill(Node):
    weight: float = float(0.5)
    position: 'Position' = field(default_factory=Position)
