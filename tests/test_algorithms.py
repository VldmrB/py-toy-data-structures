from copy import deepcopy

from hypothesis import strategies as st, given

from algorithms.mergesort import merge_sort


class TestMergesort:

    int_str_lists_and_list_of_lists = given(
        st.one_of(st.lists(st.integers()),
                  st.lists(st.text()),
                  st.lists(st.lists(st.integers()), min_size=1),
                  st.lists(st.lists(st.text()), min_size=1)
                  ))

    @int_str_lists_and_list_of_lists
    def test_mergesort_in_place(self, value):
        copied = deepcopy(value)
        merge_sort(value, in_place=True)
        assert value == sorted(copied)

    @int_str_lists_and_list_of_lists
    def test_mergesort_new(self, value):
        assert merge_sort(value, in_place=False) == sorted(value)
