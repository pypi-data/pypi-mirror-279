import heapq
import math
from typing import List

from fuel_efficency.algorithms.path_finding import PathfindingStrategy
from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


class DijkstraStrategy(PathfindingStrategy):

    cardinal_directions = [Position(-1, -1), Position(-1, 0), Position(-1, 1), Position(0, -1), Position(0, 1), Position(1, -1), Position(1, 0), Position(1, 1)]

    def reconstruct_path(came_from: dict[Node, Node], current: Node) -> List[Node]:
        path: List[Node] = [current]

        while current in came_from:
            current = came_from[current]
            path = [current] + path

        return path[1:]


    def find_path(grid:List[List[Node]], start:Node, end:Node) -> List[List[Node]]:
        path: List[List[Node]] = []

        came_from:dict[Node, Node] = {}

        open_set: List[tuple[Node, float]] = []

        heapq.heappush(open_set, (0, start))

        g_score: dict[Node, float] = {}
        g_score[start] = 0


        while len(open_set) > 0:
            current = heapq.heappop(open_set)[1]

            if current == end:
                path = DijkstraStrategy.reconstruct_path(came_from, current)
                break

            for neighbor in DijkstraStrategy.get_neighbors(grid, current):
                g = g_score[current] + neighbor.weight + DijkstraStrategy.calculate_distance(current, neighbor)

                if neighbor not in g_score or g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = g

                    heapq.heappush(open_set, (g, neighbor))

        return path

    def get_neighbors(grid:List[List[Node]], node:Node) -> List[Node]:
        neighbors: List[Node] = PathfindingStrategy.get_neighbors(grid, node, DijkstraStrategy.cardinal_directions)
        # x_len = len(grid)
        # y_len = len(grid[0])
        # for direction in DijkstraStrategy.cardinal_directions:
        #     resulting_direction = node.position + direction
        #     if (resulting_direction.x >= 0 and resulting_direction.x < x_len) and \
        #             (resulting_direction.y >= 0 and resulting_direction.y < y_len) :
        #         neighbor = grid[resulting_direction.x][resulting_direction.y]
        #         neighbors.append(neighbor)

        return neighbors

    def calculate_distance(node1:Node, node2: Node) -> float:
        # x1: int  = node1.position.x
        # y1: int  = node1.position.y

        # x2: int  = node2.position.x
        # y2: int  = node2.position.y

        # return math.sqrt((math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))
        distance: float = PathfindingStrategy.calculate_distance(node1, node2)

        return distance
