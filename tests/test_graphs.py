import pytest

from structures.graphs import Djikstra


class TestDjikstra:

    test_graph = {
        'Paris': {'Moscow': 3, 'Milan': 2, 'Berlin': 1, 'London': 4},
        'London': {'Moscow': 5, 'Milan': 2, 'Berlin': 1, 'Dublin': 2},
        'Berlin': {'Paris': 3, 'Moscow': 2},
        'Moscow': {'Tashkent': 3, 'Almaty': 2, 'Saint-Petersburg': 1, 'Paris': 3},
        'Milan': {'Vatican': 1, 'Madrid': 2, 'Moscow': 4, 'Tashkent': 6},
        'Tashkent': {'Moscow': 3, 'Samarkand': 1, 'Saint-Petersburg': 2, 'London': 6},
        'Samarkand': {'Almaty': 1, 'Moscow': 4}
    }
    berlin_results = (
        {'Almaty': 'Moscow',
         'Dublin': 'London',
         'London': 'Paris',
         'Madrid': 'Milan',
         'Milan': 'Paris',
         'Moscow': 'Berlin',
         'Paris': 'Berlin',
         'Saint-Petersburg': 'Moscow',
         'Samarkand': 'Tashkent',
         'Tashkent': 'Moscow',
         'Vatican': 'Milan'},
        {'Almaty': 4,
         'Berlin': 0,
         'Dublin': 9,
         'London': 7,
         'Madrid': 7,
         'Milan': 5,
         'Moscow': 2,
         'Paris': 3,
         'Saint-Petersburg': 3,
         'Samarkand': 6,
         'Tashkent': 5,
         'Vatican': 6}
    )

    @pytest.mark.parametrize('source', ['Berlin'])
    def test_djikstra(self, source: str):
        results = Djikstra(self.test_graph, source)
        previous = results.previous
        distances = results.distances
        assert previous, distances == self.berlin_results
