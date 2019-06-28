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

    def __repr__(self):
        return self.__class__.__name__

    str_insert_test_value = 'test value'  # for testing insertion, indexing

    integer_lists = st.lists(st.integers())
    str_lists = st.lists(st.text())
    int_str_list = given(st.one_of(integer_lists, str_lists))

    @classmethod
    def lst_and_its_random_value(cls, value):
        random_value = random.choice(value)
        lst = Single(value)
        return random_value, lst

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

    @assorted_strategies
    def test_len_descriptor(self, value):
        if isinstance(value, list):
            value_len = len(value)
        else:
            value_len = 1
        assert value_len == len(Single(value))

    @given(st.lists(st.integers(), 1, 5))
    def test_contains_descriptor(self, value):
        random_value, lst = self.lst_and_its_random_value(value)
        assert random_value in lst

    @given(st.lists(st.integers(), 1, 5))
    def test_index_with_present_value(self, value):
        random_value, lst = self.lst_and_its_random_value(value)
        assert value.index(random_value) == lst.index(random_value)

    def test_index_with_non_present_value(self):
        lst = Single([0, 1, 2, 3, 4, 5])
        with pytest.raises(ValueError):
            lst.index(self.str_insert_test_value)
            assert True

    def test_index_on_empty(self):
        lst = Single()
        with pytest.raises(ValueError):
            lst.index(self.str_insert_test_value)
            assert True

    @given(st.lists(st.integers(), max_size=5))
    def test_prepend(self, value):
        lst = Single(value)
        old_head = lst.head
        lst.prepend(self.str_insert_test_value)
        assert lst.head.value == self.str_insert_test_value
        if old_head:
            assert old_head.value == lst.head.next.value
        else:
            assert lst.head.next is None

    @given(st.lists(st.integers(), max_size=5))
    def test_insert(self, value):
        value_len = len(value)
        random_index = random.randint(0, value_len + value_len // 3)
        lst = Single([value])
        lst.insert(random_index, self.str_insert_test_value)
        check_index = 0
        current_element = lst.head
        while current_element:
            if current_element.value == self.str_insert_test_value:
                if check_index == random_index:
                    assert True
                elif check_index >= value_len:
                    assert True
                return
            current_element = current_element.next
            check_index += 1

    @given(st.lists(st.integers(), max_size=10))
    def test_append(self, value):
        lst = Single(value)
        lst.append(self.str_insert_test_value)
        assert lst.index(self.str_insert_test_value) == len(lst) - 1

    @given(st.lists(st.integers(), 1, 5))
    def test_pop_from_non_empty(self, value):
        lst = Single(value)
        popped = lst.pop()
        assert popped == value[0]
        assert len(lst) == len(value) - 1

    def test_pop_from_empty(self):
        with pytest.raises(IndexError):
            Single().pop()
            assert True

    @given(st.lists(st.integers(), 1, 5, unique=True))
    def test_remove_present_value(self, value):
        random_value, lst = self.lst_and_its_random_value(value)
        lst.remove(random_value)
        assert random_value not in lst

    def test_remove_from_empty(self):
        lst = Single()
        with pytest.raises(ValueError):
            lst.remove(self.str_insert_test_value)
            assert True

    @given(st.lists(st.integers(), 1, 5, unique=True))
    def test_remove_at_index(self, value):
        value_len = len(value)
        random_index = random.randint(0, value_len-1)
        lst = Single(value)
        lst.remove_at_index(random_index)
        value.pop(random_index)
        assert lst == Single(value)

    @given(st.lists(st.integers(), 1, 10))
    def test_remove_last(self, value):
        lst = Single(value)
        lst.remove_last()
        value.pop()
        assert lst == Single(value)

    @given(st.lists(st.integers(0, 9), 1, 10))  # ensuring duplicates
    def test_remove_all_nodes_by_value(self, value):
        random_value, lst = self.lst_and_its_random_value(value)
        lst.remove_all_nodes_by_value(random_value)
        value = [i for i in value if i != random_value]
        assert lst == Single(value)

    @given(st.lists(st.integers(), max_size=10))
    def test_reverse(self, value):
        lst = Single(value)
        lst.reverse()
        value.reverse()
        assert lst == Single(value)

    @int_str_list
    def test_mergesort(self, value):
        sorted_list = sorted(value)
        merge_sorted = Single(value)
        merge_sorted.mergesort()
        assert repr(merge_sorted) == repr(Single(sorted_list))

    @given(st.lists(st.integers(), min_size=1, max_size=15))
    def test_merge_sorted_lists(self, value):
        value_len_slit = len(value) // 2
        lst1 = Single(sorted(value[:value_len_slit]))
        lst2 = Single(sorted(value[value_len_slit:]))
        lst1.merge_sorted_lists(lst2)
        assert lst1 == Single(sorted(value))
