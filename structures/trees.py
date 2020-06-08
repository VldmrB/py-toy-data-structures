from collections import deque
from typing import List, Tuple, Union


class Tree:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def dfs_recursion(self) -> List['Tree']:
        def recurse(node):  # nested function allows not having to explicitly
            # pass a node or having to use a keyword i.e. if None, pass self
            if node.left:
                recurse(node.left)
            values.append(node.value)
            if node.right:
                recurse(node.right)

        values = []
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
        current = self
        values, stack = [], []

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
        def recurse(node: Tree, depth: int):
            depth -= 1
            if node.left and depth:
                recurse(node.left, depth)
            values.append(node.value)
            if node.right and depth:
                recurse(node.right, depth)

        values = []
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

        def recurse(node: 'Tree', depth: int) -> Tuple[Union['Tree', None], str]:
            if not node or value == node.value:
                return node, 'done'
            depth -= 1
            if depth:
                if node.value > value:
                    return recurse(node.left, depth)
                if node.value < value:  # this does not have to be explicit as this tree
                    # implementation doesn't allow duplicates
                    return recurse(node.right, depth)
            return None, ''  # depth exhausted

        max_depth = 1
        while True:
            result = recurse(self, max_depth)
            if result[1] == 'done':
                return result[0]
            max_depth += 1

    @staticmethod
    def _print_found_node(found, value):
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


if __name__ == '__main__':
    pass
