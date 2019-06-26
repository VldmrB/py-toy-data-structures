import random

import pytest
from hypothesis import given
from hypothesis import strategies as st

from structures.linked_lists import SingleNode, Single


assorted_strategies = given(st.one_of(
    st.text(), st.integers(),
    st.booleans(), st.lists(st.integers())))


class TestSingleNode:
    
    @staticmethod
    def generate_repr_string(value):
        value = f'{value!r}' if isinstance(value, str) else value
        return f'{SingleNode.__name__}({value})'

    @staticmethod
    def generate_str(value, next_value):
        repr_str = TestSingleNode.generate_repr_string(value)
        repr_str_2 = TestSingleNode.generate_repr_string(next_value)
        return f'{repr_str} --> {repr_str_2}'

    @given(st.integers())
    def test_value_attr_on_creation(self, value):
        assert SingleNode(value).value == value

    def test_next_attr_on_creation(self):
        assert SingleNode(5).next is None

    @assorted_strategies
    def test_repr_descriptor(self, value):
        node = SingleNode(value)
        assert repr(node) == self.generate_repr_string(value)

    @assorted_strategies
    def test_str_descriptor_with_no_next(self, value):
        node = SingleNode(value)
        assert str(node) == f'{self.generate_repr_string(value)} --> {None}'

    @assorted_strategies
    def test_str_descriptor_with_next(self, value):
        node = SingleNode(value)
        node.next = SingleNode(value)
        assert self.generate_str(value, value) == str(node)

    @assorted_strategies
    def test_eq_descriptor(self, value):
        assert SingleNode(value) == SingleNode(value)


class TestSingle:

    integer_lists = st.lists(st.integers())
    str_lists = st.lists(st.text())
    int_str_list = given(st.one_of(integer_lists, str_lists))

    def test_empty_list_is_false(self):
        assert not Single()

    def test_non_empty_list_is_true(self):
        assert Single(0)

    @assorted_strategies
    def test_repr_descriptor(self, value):
        if isinstance(value, list):
            contents = f'{value}'
        else:
            contents = f'{[value]}'
        assert f'{Single.__name__}({contents})' == repr(Single(value))

    @int_str_list
    def test_mergesort(self, value):
        sorted_list = sorted(value)
        merge_sorted = Single(value)
        merge_sorted.mergesort()
        assert repr(merge_sorted) == repr(Single(sorted_list))

    @assorted_strategies
    def test_len_descriptor(self, value):
        if isinstance(value, list):
            value_len = len(value)
        else:
            value_len = 1
        assert value_len == len(Single(value))

    @given(st.lists(st.integers(), 1))
    def test_contains_descriptor(self, value):
        random_value = random.choice(value)
        lst = Single(value)
        assert random_value in lst

    @given(st.lists(st.integers(), 1))
    def test_index_method_with_present_value(self, value):
        random_value = random.choice(value)
        lst = Single(value)
        assert value.index(random_value) == lst.index(random_value)

    def test_index_method_with_non_present_value(self):
        lst = Single([0, 1, 2, 3, 4, 5])
        with pytest.raises(ValueError):
            lst.index('a non-integer value')
            assert True

    def test_index_method_on_empty(self):
        lst = Single()
        with pytest.raises(ValueError):
            lst.index('some value')
            assert True


