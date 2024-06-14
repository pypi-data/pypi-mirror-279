from abc import ABC
from dataclasses import dataclass, field

from fuel_efficency.entities.position import Position


@dataclass(slots=True, frozen=True)
class Terrain(ABC):
   weight: float = float(1)
   position: 'Position' = field(default_factory=Position)

   def __lt__(self, other: 'Terrain'):
      if not isinstance(other, Terrain):
         raise NotImplementedError("Missing `weight` attribute")

      return self.weight < other.weight

   def __le__(self, other: 'Terrain'):
      if not isinstance(other, Terrain):
         raise NotImplementedError("Missing `weight` attribute")

      return self.weight <= other.weight

   def __gt__(self, other: 'Terrain'):
      if not isinstance(other, Terrain):
         raise NotImplementedError("Missing `weight` attribute")

      return self.weight > other.weight

   def __ge__(self, other: 'Terrain'):
      if not isinstance(other, Terrain):
         raise NotImplementedError("Missing `weight` attribute")

      return self.weight >= other.weight

   def __eq__(self, other: 'Terrain'):
      if not isinstance(other, Terrain):
         raise NotImplementedError("Missing `position` or `weight` attribute")

      return self.weight == other.weight and self.position == other.position
