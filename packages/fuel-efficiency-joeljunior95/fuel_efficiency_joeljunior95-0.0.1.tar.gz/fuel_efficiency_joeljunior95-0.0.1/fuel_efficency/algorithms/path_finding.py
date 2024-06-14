from abc import ABC, abstractmethod
import math
from typing import List

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


class PathfindingStrategy(ABC):

    @abstractmethod
    def find_path(grid:List[List[Node]], start:Node, end:Node):
        pass # pragma: no cover

    def get_neighbors(grid:List[List[Node]], node:Node, directions:List[Position]) -> List[Node]:
        neighbors: List[Node] = []
        x_len = len(grid)
        y_len = len(grid[0])
        for direction in directions:
            resulting_direction = node.position + direction
            if (resulting_direction.x >= 0 and resulting_direction.x < x_len) and \
                    (resulting_direction.y >= 0 and resulting_direction.y < y_len) :
                neighbor = grid[resulting_direction.x][resulting_direction.y]
                neighbors.append(neighbor)

        return neighbors

    def calculate_distance(node1:Node, node2: Node) -> float:
        x1: int  = node1.position.x
        y1: int  = node1.position.y

        x2: int  = node2.position.x
        y2: int  = node2.position.y

        return math.sqrt((math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))
