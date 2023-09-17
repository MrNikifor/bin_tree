from binary_tree import Node, BinaryTree, Number


class ColoredNode(Node):
    def __init__(self, value: object):
        super().__init__(value)
        self.is_red = True

    def __repr__(self):
        color_name = 'r' if self.is_red else 'b'
        return f"{super().__repr__()}({color_name})"

    def change_color(self):
        self.is_red = not self.is_red


class RedBlackTree(BinaryTree):
    _allowed_types_ = (Number)
    _new_node_ = ColoredNode

    def add(self, value: _allowed_types_) -> None:
        super().add(value)
        print("add balancer here")

    def remove(self, value: _allowed_types_) -> None:
        super().remove(value)
        print("add balancer here")

    def _left_rotation_(self, parent_node):
        assert parent_node.right is not None and parent_node.right.is_red
        right_child_node = parent_node.right
        if parent_node == self.root:
            self.root = right_child_node
        right_child_left_subtree = right_child_node.left
        parent_node.right = right_child_left_subtree
        right_child_node.left = parent_node
        parent_node.change_color()
        right_child_node.change_color()

    def _right_rotation_(self, parent_node):
        assert parent_node.left is not None and parent_node.left.is_red
        left_child_node = parent_node.left
        if parent_node == self.root:
            self.root = left_child_node
        left_child_right_subtree = left_child_node.right
        parent_node.left = left_child_right_subtree
        left_child_node.right = parent_node
        parent_node.change_color()
        left_child_node.change_color()

    def _color_swap_(self, parent_node):
        raise NotImplementedError


if __name__ == '__main__':
    rbt = RedBlackTree()
    rbt.add(5)
    rbt.root.change_color()
    rbt.add(4)
    rbt.add(7)
    rbt.add(6)
    rbt.search(6).change_color()
    rbt.add(8)
    rbt.search(8).change_color()
    rbt.print()
    rbt._left_rotation_(rbt.root)
    rbt.print()
    rbt._right_rotation_(rbt.root)
    rbt.print()
