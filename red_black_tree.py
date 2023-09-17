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
        recolor_root = False
        if self.root is None:
            recolor_root = True
        super().add(value)
        if recolor_root:
            self.root.change_color()
        else:
            self._rebalance_(self.root)

    def remove(self, value: _allowed_types_) -> None:
        super().remove(value)
        self._rebalance_(self.root)

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
        return right_child_node

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
        return left_child_node

    def _color_swap_(self, parent_node):
        child_nodes_exist = parent_node.left is not None and parent_node.right is not None
        assert child_nodes_exist and parent_node.left.is_red and parent_node.right.is_red
        if parent_node != self.root:
            parent_node.change_color()
        parent_node.left.change_color()
        parent_node.right.change_color()

    def _rebalance_(self, node):
        if node.left is None and node.right is None:
            return node
        if node.left:
            node.left = self._rebalance_(node.left)
        if node.right:
            node.right = self._rebalance_(node.right)
        rotation_happened = False
        left_child_exist = node.left is not None
        right_child_exist = node.right is not None
        both_child_exist = left_child_exist and right_child_exist

        if both_child_exist and node.left.is_red and node.right.is_red:
            self._color_swap_(node)

        left_child_not_exist_or_black = not left_child_exist or left_child_exist and not node.left.is_red
        if left_child_not_exist_or_black and right_child_exist and node.right.is_red:
            node = self._left_rotation_(node)
            rotation_happened = True

        if left_child_exist and node.left.is_red and node.left.left is not None and node.left.left.is_red:
            node = self._right_rotation_(node)
            rotation_happened = True

        if rotation_happened:
            return self._rebalance_(node)

        return node


if __name__ == '__main__':
    rbt = RedBlackTree()
    rbt.add(24)
    rbt.add(5)
    rbt.add(1)
    rbt.add(15)
    rbt.add(3)
    rbt.add(8)
    rbt.print()
    rbt.remove(5)
    rbt.print()
