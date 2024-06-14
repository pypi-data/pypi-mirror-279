from dataclasses import dataclass, field

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position
from fuel_efficency.entities.terrain import Terrain


@dataclass(slots=True, frozen=True, eq=False)
class UpHill(Terrain):
    weight: float = float(2)
    position: 'Position' = field(default_factory=Position)
