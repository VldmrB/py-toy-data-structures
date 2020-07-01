from collections import deque
from typing import List, Union


class Tree:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def dfs_recursion(self) -> List['Tree']:
        values = []

        def recurse(node):  # nested function allows not having to explicitly
            # pass a node or having to use a keyword i.e. if None, pass self
            if node.left:
                recurse(node.left)
            values.append(node.value)
            if node.right:
                recurse(node.right)

        recurse(self)
        return values

    def dfs_find(self, value: int) -> 'Tree':
        def recurse(node):
            if not node or node.value == value:
                return node
            elif node.value > value:
                return recurse(node.left)
            elif node.value < value:
                return recurse(node.right)

        return recurse(self)

    def dfs_stack(self) -> List[int]:
        values, stack, current = [], [], self

        while True:
            if current:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                values.append(current.value)
                current = current.right
            else:
                return values

    def dfs_while_find(self, value) -> 'Tree':
        """Without a stack or recursion."""
        current = self

        while current:
            if current.value == value:
                return current
            elif current.value > value:
                current = current.left
            elif current.value < value:
                current = current.right

    def dfs_stack_find(self, value) -> 'Tree':
        """Absolutely unnecessary to do through a stack, merely a proof of concept."""
        current, stack = self, []

        while True:
            if not current or current.value == value:
                return current
            elif current.value > value:
                stack.append(current.left)
            elif current.value < value:
                stack.append(current.right)
            if stack:
                current = stack.pop()

    def iddfs(self, recursion_depth: int) -> List['Tree']:
        """Recursion to the specified depth."""
        values = []

        def recurse(node: 'Tree', depth: int):
            depth -= 1
            if not depth:
                return
            if node.left:
                recurse(node.left, depth)
            values.append(node.value)
            if node.right:
                recurse(node.right, depth)

        recurse(self, recursion_depth)
        return values

    def iddfs_stack_not_working(self, depth: int) -> List[int]:
        """(NOT WORKING!!!) Use a stack to get all the nodes up to the specified depth.

        There's no reason to use a stack for BSTs when it comes to finding a
        concrete value or getting a full path to it. A while loop can easily be
        implemented with the use of a max_depth limit.
        It can still be useful for other types of trees, since those will not
        have their values in a strictly sorted order.

        TL;DR This is not working and I'm no longer fully convinced that it
        is possible. The problem comes down to the fact I can't reliably
        determine depth at any given moment."""
        print('depth is', depth)
        stack, values, current = [], [], self
        current_depth = depth
        last = ''
        while True:
            if current:
                last = 'left'
                stack.append(current)
                current = current.left
                current_depth -= 1
            elif stack:  # todo this is not working right!
                if last != 'left':
                    current_depth += 1
                last = 'right'
                current = stack.pop()
                values.append(current.value)
                current = current.right
            else:
                break
            if not current_depth:
                break

        return values

    def iddfs_find(self, value: int) -> 'Tree':
        def recurse(node: 'Tree', depth: int):
            if not node or node.value == value:
                return node, 'done'  # found the value or the value is not in the tree
            depth -= 1
            if depth:
                return (recurse(node.left, value) if value < node.value
                        else recurse(node.right, depth))
            return None, None

        max_depth = 1
        while max_depth:
            result = recurse(self, max_depth)
            if result[1] == 'done':
                return result[0]
            max_depth += 1

    @staticmethod
    def _print_found_node(found: Union[None, 'Tree'], value):
        if found is None:
            print(f'{value} not in tree')
        elif found.left is None and found.right is None:
            print(f'{found} found; leaf')
        else:
            print(f'{found} found; children: '
                  f'left - {found.left}, '
                  f'right - {found.right}')

    def bfs_queue(self):
        queue, values = deque([self]), []

        while queue:
            current = queue.popleft()
            if current:
                values.append(current.value)
                queue.extend([current.left, current.right])

        return values

    def __str__(self):
        return f'Node({self.value})'

    def insert(self, value):
        def recursion(node):
            if value <= node.value:
                if node.left:
                    recursion(node.left)
                else:
                    node.left = Tree(value)
                    return node.left
            elif value >= node.value:
                if node.right:
                    recursion(node.right)
                else:
                    node.right = Tree(value)
                    return node.right

        return recursion(self)

    def insert_multiple(self, seq: List[int]):
        # seq.sort()
        for i in seq:
            self.insert(i)
        return self

    def delete(self, value):
        # todo figure out why deleting root node takes 3 elements (12-14) with it, test rest of code
        root = node = self
        if node.value == value:  # root node is the one
            if not node.right and not node.left:
                del self  # the tree is gone completely
            elif not node.right:
                return node.left
            elif not node.left:
                return node.right
            else:  # both leaf nodes are present
                right = node.right  # arbitrarily choose the right; either side works if
                # the node to be deleted is the root node
                left_most_of_right = right.left  # looking for the left-most node of the right
                # node that will be the new root
                if not left_most_of_right:  # if there's no lefts, it's extremely simple
                    node.right = node.right.right
                    node.value = node.right.value
                    return self
                previous = left_most_of_right
                while True:
                    if left_most_of_right.left:
                        previous = left_most_of_right
                        left_most_of_right = left_most_of_right.left
                    else:
                        break
                node.value = left_most_of_right.value
                previous.left = None
                return self

        previous = None
        while node:
            if node.value == value:
                if not node.left and not node.right:  # leaf
                    if previous.left is node:
                        previous.left = None
                    else:
                        previous.right = None
                    return root
                elif not node.right:
                    node.value = node.left.value
                    node.left = node.left.left
                    node.left = node.left.right
                    del node.left
                    return root
                elif not node.left:
                    node.value = node.right.value
                    node.left = node.right.left
                    node.right = node.right.right
                    node.right = None
                    return
                elif node.left and node.right:  # arbitrarily pick left
                    right_most_of_left = node.left
                    while True:
                        previous = right_most_of_left
                        if right_most_of_left.right:
                            right_most_of_left = right_most_of_left.right
                        else:
                            node.value = right_most_of_left.value
                            previous.right = None
                            return root

            elif node.value < value:
                node = node.right
            elif node.value > value:
                node = node.left
            previous = node

    def print(self):
        queue = deque([self])
        values = []
        current_level_nodes_amount = 1
        current_level_values = []
        while queue:
            current = queue.popleft()
            if len(current_level_values) == current_level_nodes_amount:
                current_level_nodes_amount *= 2
                values.append(current_level_values)
                current_level_values = []
            value = current.value if current else current
            current_level_values.append(value)
            if current_level_nodes_amount == len(current_level_values) and not any(
                    current_level_values):
                break
            queue.extend([current] * 2 if current is None else [current.left, current.right])

        node_width = max([len(str(max([i for i in values[-1] if i is not None]))), 4])
        last_level_width = (len(values[-1]) * (node_width + 4))
        for level in values[:-1]:
            current_node_width = last_level_width // (len(level) * 2)
            current_space_width = last_level_width // (len(level))
            node_strings = [
                str(value if value is not None else 'N').center(current_node_width - 2, '-')
                .center(current_space_width) for value in level]
            in_between = [('/' + ' ' * (current_node_width - 2) + '\\').center(current_space_width)
                          for _ in level]
            print(''.join(node_strings).center(last_level_width))
            print(''.join(in_between).center(last_level_width))

        print(  # last level
            '    '.join(
                [str(value if value is not None else 'N').center(node_width)
                 for value in values[-1]]
            ).center(last_level_width)
        )


if __name__ == '__main__':
    a = Tree(10).insert_multiple([
        5,
        0,
        15,
        13,
        14,
        12,
        25,
        20,
        23,
        30
    ])
    # print(a.dfs_recursion())
    a.print()
    a = a.delete(10)
    # print(a.dfs_recursion())
    a.delete(13)
    a.print()
