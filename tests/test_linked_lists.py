from structures.linked_lists import SingleNode
from hypothesis import given
from hypothesis import strategies as st


class TestSingleNode:

    repr_and_str_strategies = given(st.one_of(
        st.text(), st.integers(), st.booleans(),
        st.iterables(st.integers()), st.lists(st.integers())
        ))

    @staticmethod
    def generate_repr_string(value):
        value = f'{value!r}' if isinstance(value, str) else value
        return f'SingleNode({value})'

    def test_value_attr_on_creation(self, value=5):
        assert SingleNode(value).value == value

    def test_next_attr_on_creation(self):
        assert SingleNode(5).next is None

    @repr_and_str_strategies
    def test_repr_descriptor_output(self, value):
        node = SingleNode(value)
        assert repr(node) == self.generate_repr_string(value)

    @repr_and_str_strategies
    def test_str_descriptor_output(self, value):
        node = SingleNode(value)
        assert str(node) == f'{self.generate_repr_string(value)} --> {None}'
