from collections import deque
from typing import Dict


class Djikstra:
    """Distances from source to all other nodes for weighted, directed graphs with(out)? cycles."""

    def __init__(self, graph: Dict[str, Dict[str, int]], source: str):
        if source not in graph:
            raise KeyError(f' {source!r} vertex not in graph')
        self._graph = graph
        self._source = source
        self.previous, self.distances = self._calculate()

    def get_shortest_path(self, edge: str):
        if edge not in self.distances:
            raise KeyError(f'Edge {edge!r} not in graph')
        path = []
        current = edge
        while current != self._source:
            path.append(current)
            current = self.previous[current]
        else:
            path.append(self._source)

        path.reverse()
        return path

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph: Dict[str, Dict[str, int]], source: str = None):
        source = source or self._source
        if source not in graph:
            raise KeyError(f' {self._source!r} vertex not in graph')
        self._graph = graph
        self._source = source
        self.previous, self.distances = self._calculate()

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source: str):
        if source not in self._graph:
            raise KeyError(f' {self._source!r} vertex not in graph')
        self._source = source
        self.previous, self.distances = self._calculate()

    def _calculate(self):
        if self._source not in self._graph:
            raise KeyError(f' {self._source!r} vertex not in graph')
        visited = set()
        previous = {}
        distances = {self._source: 0}
        queue = deque([self._source])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            for edge, weight in self._graph.get(current, {}).items():
                known_shortest_distance_to_edge = distances.get(edge)
                distance_to_edge_through_current = distances[current] + weight
                if (known_shortest_distance_to_edge is None
                        or distance_to_edge_through_current < known_shortest_distance_to_edge):
                    distances[edge] = distance_to_edge_through_current
                    previous[edge] = current
                queue.append(edge)

        return previous, distances


if __name__ == '__main__':
    gd = {
        'Moscow': {'Tashkent': 3, 'Almaty': 2, 'Saint-Petersburg': 1, 'Paris': 3},
        'Paris': {'Moscow': 3, 'Milan': 2, 'Berlin': 1, 'London': 4},
        'London': {'Moscow': 5, 'Milan': 2, 'Berlin': 1, 'Dublin': 2},
        'Berlin': {'Paris': 3, 'Moscow': 2},
        'Milan': {'Vatican': 1, 'Madrid': 2, 'Moscow': 4, 'Tashkent': 6},
        'Tashkent': {'Moscow': 3, 'Samarkand': 1, 'Saint-Petersburg': 2, 'London': 6},
        'Samarkand': {'Almaty': 1, 'Moscow': 4}
    }
    lol = Djikstra(gd, 'Berlin')
    print(lol.get_shortest_path('Vatican'))
    print(lol.get_shortest_path('Berlin'))
