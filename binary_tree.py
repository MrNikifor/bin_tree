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

    def print(self, node=None):
        raise NotImplementedError


if __name__ == '__main__':
    tree = BinaryTree()
    tree.add(5)
    tree.add(10)
    tree.add(4)
    tree.add(1)
    print(tree)
    print(tree.search(8))
    print(tree.search(4))
