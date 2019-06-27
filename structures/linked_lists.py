from typing import Union, Any

"""
Linked list and nodes implementations.
To an extent, syntax and logic mirrors that of Python's list.
"""


class SingleNode:

    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        value = f'{self.value!r}' if isinstance(self.value, str) else self.value
        return f'{self.__class__.__name__}({value})'

    def __str__(self):
        _next = self.next
        _next_repr = _next if not _next else repr(self.next)
        return f'{self.__repr__()} --> {_next_repr}'

    def __eq__(self, node):
        if isinstance(node, SingleNode):
            if node.value == self.value:
                return True
        return False


class Single:

    def __init__(self, values: Union[list, tuple, SingleNode, Any] = None):
        """
        :param values: lists/tuples will be iterated over, with each element
        getting added as a separate node. To add a node with a list/tuple as a
        value, pass in a node with its value set to one
        """
        self.head = None
        if values is not None:
            if isinstance(values, SingleNode):
                self.head = values
            elif isinstance(values, (list, tuple)):
                for i in range(len(values) - 1, -1, -1):
                    self.prepend(values[i])
            else:
                self.head = SingleNode(values)

    def __bool__(self):
        return self.head is not None

    def _list_elements(self):
        elements = []
        current_element = self.head
        while current_element:
            if isinstance(current_element.value, Single):
                elements.append(current_element.value.__str__())
            else:
                elements.append(current_element.value)
            current_element = current_element.next
        return elements

    def __repr__(self):
        return f'{self.__class__.__name__}({self._list_elements()})'

    def __len__(self):
        length = 0
        if not self:
            return length
        current_element = self.head
        while current_element:
            current_element = current_element.next
            length += 1
        return length

    def __eq__(self, other):
        if isinstance(other, Single):
            if self._list_elements() == other._list_elements():
                return True

    @staticmethod
    def _raise_value_error(value):
        value_desc = value if not isinstance(value, str) else f'{value!r}'
        raise ValueError(f'{value_desc} not in list')

    def __contains__(self, value):
        if not self:
            return False
        current_element = self.head
        while current_element:
            if current_element.value == value:
                return True
            current_element = current_element.next
        return False

    def index(self, value, start: int = None, stop: int = None):
        current_element = self.head
        _index = 0
        while current_element:
            if current_element.value == value:
                if start is None and stop is None:
                    return _index
                elif start is not None and stop is None:
                    if start <= _index:
                        return _index
                elif stop is not None and start is None:
                    if _index <= stop:
                        return _index
                else:
                    if start <= _index <= stop:
                        return _index
            current_element = current_element.next
            _index += 1
        else:
            value_desc = self._raise_value_error(value)
            raise ValueError(f'{value_desc} not in list')

    def prepend(self, value):  # O(1)
        head = SingleNode(value)
        if not self:
            self.head = head
        else:
            head.next = self.head
            self.head = head

    def insert(self, index, value):  # O(i)
        new_node = SingleNode(value)
        if not self:
            self.head = new_node
            return
        _index = 0

        previous_element = None
        current_element = self.head
        while current_element:
            if _index == index:
                if previous_element:
                    new_node.next = current_element
                    previous_element.next = new_node
                    return
                else:
                    new_node.next = current_element
                    self.head = new_node
                    return
            previous_element = current_element
            current_element = current_element.next
            _index += 1
        previous_element.next = new_node

    def append(self, value):  # O(n)
        new_node = SingleNode(value)
        if not self:
            self.head = new_node
            return
        current_element = self.head
        while current_element.next:
            current_element = current_element.next
        current_element.next = new_node

    def pop(self):  # O(1)
        if not self:
            raise IndexError('pop from empty list')
        value = self.head.value
        self.head = self.head.next
        return value

    def remove(self, value):  # worst - O(n)
        current_element = self.head
        previous_element = None
        while current_element:
            if current_element.value == value:
                if previous_element:
                    previous_element.next = current_element.next
                else:
                    self.head = self.head.next
                return
            previous_element = current_element
            current_element = current_element.next
        else:
            self._raise_value_error(value)

    def remove_at_index(self, index: int):  # O(i)
        _index = 0
        current_element = self.head
        previous_element = None

        while current_element:
            if _index == index:
                if previous_element:
                    previous_element.next = current_element.next
                else:
                    self.head = current_element.next
                return
            previous_element = current_element
            current_element = current_element.next
            _index += 1

        raise IndexError('index out of range')

    def remove_last(self):  # O(n)
        current_element = self.head
        previous_element = None
        while current_element.next:
            previous_element = current_element
            current_element = current_element.next
        if previous_element:
            previous_element.next = None
        else:
            self.head = None

    def remove_all_nodes_by_value(self, val):
        current_element = self.head
        previous_element = None
        while current_element:
            if current_element.value == val:
                if previous_element:
                    previous_element.next = current_element.next
                else:
                    self.head = current_element.next
            else:
                previous_element = current_element
            current_element = current_element.next
        return self.head

    def reverse(self):
        current_element = self.head
        previous_element = None
        while current_element:
            next_element = current_element.next
            current_element.next = previous_element
            previous_element = current_element
            current_element = next_element
        self.head = previous_element

    def mergesort(self):
        """
        Inplace Mergesort algorithm for a singly-linked list
        O(N log N) time, O(1) space

        Translation of listsort() by jfs from SO; from C to Python

        https://gist.github.com/zed/5651186
        http://www.chiark.greenend.org.uk/~sgtatham/algorithms/listsort.html
        """
        if not self.head:
            return
        head = self.head  # used for marking the start of the 'left' list
        # as well as referencing the first node in the fully sorted list
        l_size = 1  # lists of size 1 are sorted first. After the whole list is
        # iterated over, size is increased, much like in mergesort used for
        # arrays. That is, if the orginal list length > 2

        while True:  # responsible for increasing sizes of lists to be
            # 'merged'
            l1 = head
            head, tail = None, None  # reset the pointers from the previous loop
            merge_count = 0  # for knowing when to break the enclosing loop

            while l1:  # sets starting points of left and right lists,
                # 'merges' them
                merge_count += 1  # if <= 1, this was the final merge of the
                # two halves of the whole list

                l2 = l1  # below lines set the start of the right list l_size
                # away from the start of the left list

                l1_len = 0
                l2_len = l_size
                while l1_len < l_size:
                    if not l2:
                        break
                    l2 = l2.next
                    l1_len += 1

                while l1_len or (l2_len and l2):
                    if not l1_len:
                        current, l2 = l2, l2.next
                        l2_len -= 1
                    elif not l2_len or not l2:
                        current, l1 = l1, l1.next
                        l1_len -= 1
                    elif l1.value <= l2.value:
                        current, l1 = l1, l1.next
                        l1_len -= 1
                    else:
                        current, l2 = l2, l2.next
                        l2_len -= 1

                    if tail:
                        tail.next = current
                    else:
                        head = current  # used as start of the left list in
                        # the next loop, or if this is the final one, points
                        # to the actual start of the newly sorted list
                    tail = current  # moves the tail pointer to the current el

                l1 = l2  # moves the pointer of the start of left list to the
                # node just after the last one in the right list

            tail.next = None  # prevents a potential closed loop because of
            # two nodes having each other as .next
            if merge_count <= 1:
                self.head = head
                return
            else:
                l_size *= 2

    def merge_sorted_lists(self, l2: 'Single'):
        if not self:
            self.head = l2.head
            return
        if not l2:
            return
        cur1, cur2 = self.head, l2.head

        if cur1.value <= cur2.value:
            result = self.head
            cur1 = self.head.next
        else:
            result = l2.head
            cur2 = cur2.next

        temp = result

        while cur1 and cur2:
            if cur1.value <= cur2.value:
                temp.next = cur1
                cur1 = cur1.next
            else:
                temp.next = cur2
                cur2 = cur2.next

            temp = temp.next

        if not cur1:
            temp.next = cur2
        else:
            temp.next = cur1

        self.head = result
