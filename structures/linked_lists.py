class SingleNode:

    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        _next = (str(self.next) if not self.next
                 else 'Node(' + str(self.next.value) + ')')
        return 'Node(' + str(self.value) + ') --> ' + _next


class Single:

    def __init__(self, head_value=None):
        if head_value is not None:
            self.head = SingleNode(head_value)
        else:
            self.head = head_value

    def __bool__(self):
        return self.head is not None

    def __str__(self):  # O(n)
        elements = []
        current_element = self.head
        while current_element:
            elements.append(current_element.value)
            current_element = current_element.next
        return str(elements)

    def __len__(self):
        length = 0
        if not self:
            return length
        current_element = self.head
        while current_element:
            current_element = current_element.next
            length += 1
        return length

    @staticmethod
    def _raise_value_error(value):
        value_desc = value if not isinstance(value, str) else f'{value!r}'
        raise ValueError(f'{value_desc} not in list')

    def _raise_empty_list_del(self):
        if not self:
            raise IndexError('del from empty list')

    def __contains__(self, value):
        if not self:
            return False
        current_element = self.head
        while current_element:
            if current_element.value == value:
                return True
            current_element = current_element.next
        return False

    def pretty_find(self, value):  # worst case: O(n)
        current_element = self.head
        _index = 0
        while current_element:
            if current_element.value == value:
                print('Index[' + str(_index) + ']: ' + str(current_element))
                return
            current_element = current_element.next
            _index += 1
        else:
            value_desc = self._raise_value_error(value)
            raise ValueError(f'{value_desc} not in list')

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

    def insert(self, value):  # O(1)
        head = SingleNode(value)
        if not self:
            self.head = head
        else:
            head.next = self.head
            self.head = head

    def insert_at_index(self, index, value):  # O(i)
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
            previous_element = current_element
            current_element = current_element.next
            _index += 1
        previous_element.next = new_node

    def insert_at_end(self, value):  # O(n)
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
        self._raise_empty_list_del()
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
        self._raise_empty_list_del()
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
        self._raise_empty_list_del()
        current_element = self.head
        previous_element = None
        while current_element.next:
            previous_element = current_element
            current_element = current_element.next
        if previous_element:
            previous_element.next = None
        else:
            self.head = None
