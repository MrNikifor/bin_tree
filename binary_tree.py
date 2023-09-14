from numbers import Number
from types import NoneType


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)

    def __lt__(self, other):
        return self.value.__lt__(other.value)

    def __gt__(self, other):
        return self.value.__gt__(other.value)


class BinaryTree:
    _allowed_types_ = (Node, Number)

    def __init__(self, root=None):
        if isinstance(root, (Node, NoneType)):
            # TODO: check node.value type against self._allowed_types_ ?
            self.root = root
        else:
            self.root = None
            self.add(root)

    def __len__(self):
        raise NotImplementedError

    def add(self, value):
        if not isinstance(value, self._allowed_types_):
            raise ValueError(f"For value expected one of types {[t.__name__ for t in self._allowed_types_]}, got {type(value).__name__}")
        node, parent = self._search_(value, self.root)
        if node is None:
            el = Node(value)
            if parent is None:
                self.root = el
            else:
                if value < parent.value:
                    parent.left = el
                else:
                    parent.right = el
            return True
        else:
            return False

    def remove(self, value):
        raise NotImplementedError

    def _search_(self, value, node, parent=None):
        if node is None or node.value == value:
            return node, parent
        if value < node.value:
            return self._search_(value, node.left, node)
        else:
            return self._search_(value, node.right, node)

    def search(self, value):
        return self._search_(value, self.root)[0]

    @staticmethod
    def _get_as_rows_(node):
        result = list()
        if node is not None:
            next_row = [node.left, node.right]
            result.append([node])
            while len([el for el in next_row if el is not None]) > 0:
                curr_row = next_row
                next_row = list()
                row_data = list()
                for el in curr_row:
                    row_data.append(el)
                    if el:
                        next_row.append(el.left)
                        next_row.append(el.right)
                    else:
                        next_row.append(None)
                        next_row.append(None)
                result.append(row_data)
        return result

    @staticmethod
    def _max_(node):
        if node:
            while node.right:
                node = node.right
            return node
        else:
            return None

    @staticmethod
    def _min_(node):
        if node:
            while node.left:
                node = node.left
            return node
        else:
            return None

    def print(self, node=None, filter_none=False):
        # TODO: is there a way to simplify this?
        if not node:
            node = self.root
        tree_rows = self._get_as_rows_(node)
        if filter_none:
            tree_rows = [[el if el is not None else ' ' for el in row] for row in tree_rows]
        longest_row_len = max((len(row) for row in tree_rows), default=0)
        # max tree element does not have to be the longest
        # so search for longest by checking len(str(el))
        longest_el_size = max((len(str(el)) for row in tree_rows for el in row), default=0)+1
        for row in tree_rows:
            print(''.join(str(el).center(longest_el_size*longest_row_len//len(row)) for el in row))


if __name__ == '__main__':
    tree = BinaryTree()
    tree.add(5)
    tree.add(10)
    tree.add(11)
    tree.add(4)
    tree.add(1)
    tree.add(3)
    tree.add(2)
    print("---")
    tree.print()
    print("---")
    tree.print(filter_none=True)
    print("---")
    tree.print(node=tree.search(4))
    #print(tree.search(8))
    #print(tree.search(4))
