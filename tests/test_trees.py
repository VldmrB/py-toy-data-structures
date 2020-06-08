import pytest
# from hypothesis import given
# from hypothesis import strategies as st

from structures.trees import Tree


class TestTree:

    # variations of the same list; if one changes, the other have to as well
    tree_values = [10, 0, 15, 20, 30, 25, 35, 45]
    tree_values_without_head = [10, 0, 15, 30, 25, 35, 45]
    tree_values_in_order = sorted(tree_values)
    tree_values_in_bfs_order = [20, 10, 30, 0, 15, 25, 35, 45]
    tree_values_some = tree_values[::2]
    tree_values_not_present = [i + 1 for i in tree_values_some[::2]]
    # comprehensions can't access class scoped vars from within the class except
    # in methods: https://stackoverflow.com/a/13913933/7432972

    @pytest.fixture(scope='class')
    def no_mutation_tree(self):
        return Tree(20).insert_multiple(self.tree_values_without_head)

    def test_dfs_recursion(self, no_mutation_tree):
        assert self.tree_values_in_order == no_mutation_tree.dfs_recursion()

    def test_dfs_stack(self, no_mutation_tree):
        assert self.tree_values_in_order == no_mutation_tree.dfs_stack()

    @pytest.mark.parametrize('value', tree_values_some)
    def test_dfs_while_find_value_present(self, no_mutation_tree, value):
        assert no_mutation_tree.dfs_while_find(value).value == value

    @pytest.mark.parametrize('value', tree_values_not_present)
    def test_dfs_while_find_value_missing(self, no_mutation_tree, value):
        assert no_mutation_tree.dfs_while_find(value) is None

    @pytest.mark.parametrize('value', tree_values_some)
    def test_dfs_stack_find_value_present(self, no_mutation_tree, value):
        assert no_mutation_tree.dfs_stack_find(value).value == value

    @pytest.mark.parametrize('value', tree_values_not_present)
    def test_dfs_stack_find_value_missing(self, no_mutation_tree, value):
        assert no_mutation_tree.dfs_stack_find(value) is None

    def test_bfs_queue(self, no_mutation_tree):
        assert self.tree_values_in_bfs_order == no_mutation_tree.bfs_queue()

    def test_iddfs(self, no_mutation_tree):
        assert self.tree_values_in_order == no_mutation_tree.iddfs(
            len(self.tree_values_in_order))  # the depth of this tree is only
        # ~half of the amount of elements in the list, but a change to that
        # might break the test if something like len/2 were to be passed instead

    @pytest.mark.parametrize('value', tree_values_some)
    def test_dfs_find_value_present(self, no_mutation_tree, value):
        assert no_mutation_tree.dfs_find(value).value == value

    @pytest.mark.parametrize('value', tree_values_not_present)
    def test_dfs_find_value_missing(self, no_mutation_tree, value):
        assert no_mutation_tree.dfs_find(value) is None

    @pytest.mark.parametrize('value', tree_values_some)
    def test_iddfs_find_value_present(self, no_mutation_tree, value):
        assert no_mutation_tree.iddfs_find(value).value == value

    @pytest.mark.parametrize('value', tree_values_not_present)
    def test_iddfs_find_value_missing(self, no_mutation_tree, value):
        assert no_mutation_tree.iddfs_find(value) is None
