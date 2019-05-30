from structures.linked_lists import SingleNode


def test_single_node_value_assignment():
    assert SingleNode(5).value == 5


def test_single_node_str_descriptor():
    """
    _next = (str(self.next) if not self.next
             else 'Node(' + str(self.next.value) + ')')
    return 'Node(' + str(self.value) + ') --> ' + _next
    """
    node_value = 5
    node = SingleNode(node_value)
    assert str(node) == 'Node(' + str(5) + ') --> ' + str(None)

