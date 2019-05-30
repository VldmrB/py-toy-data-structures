from structures.linked_lists import SingleNode
# from hypothesis import given
# from hypothesis.strategies import text


class TestSingleNode:
    def test_node_creation(self, value=5):
        assert SingleNode(value).value == value

    def test_node_str_descriptor_output(self, value=5):
        node = SingleNode(value)
        assert str(node) == 'Node(' + str(value) + ') --> ' + str(None)
