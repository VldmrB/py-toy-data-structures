from structures.linked_lists import SingleNode
# from hypothesis import given
# from hypothesis.strategies import text


def test_single_node_creation(value=5):
    assert SingleNode(value).value == value


def test_single_node_str_descriptor_output(value=5):
    node = SingleNode(value)
    assert str(node) == 'Node(' + str(value) + ') --> ' + str(None)
