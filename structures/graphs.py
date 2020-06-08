from collections import deque
from typing import Dict


class GraphWeightlessDirected:

    def __init__(self, data: Dict[int, list] = None):
        self.vertices = data or {}
        self._shortest_paths = {}

    def add_vertex(self, value: int, edges: list = None):
        edges = edges or {}
        self.vertices[value] = edges

    def add_edge(self, vertex: int, edge: int):
        self.vertices[vertex].append(edge)

    def get_shortest_path(self, start_vertex: int, end_vertex: int):
        if start_vertex not in self.vertices:
            raise ValueError(f'Start vertex ({start_vertex}) not in graph')
        queue = deque([start_vertex])
        visited = []

        while queue:
            current = queue.popleft()
            visited.append(current)
            if current == end_vertex:
                shortest_path = [current]
                while True:
                    previous = self._shortest_paths.get(current)
                    if previous is not None:
                        shortest_path.append(previous)
                    else:
                        shortest_path.reverse()
                        return shortest_path
                    current = previous

            edges = self.vertices.get(current, [])
            for edge in edges:
                self._shortest_paths[edge] = current
            queue.extend(edges)
        else:
            raise ValueError('End destination not in graph')

    def __str__(self):
        return str(self.vertices)


if __name__ == '__main__':
    gwd = GraphWeightlessDirected(
        {
            1: [5, 11],
            3: [4, 6],
            8: [2, 7],
            5: [12, 13],
            12: [10, 15]
        }
    )
    print(gwd.get_shortest_path(1, 15))
    print(gwd._shortest_paths)
