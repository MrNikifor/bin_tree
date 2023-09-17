from binary_tree import Node, BinaryTree, Number


class ColoredNode(Node):
    def __init__(self, value: object):
        super().__init__(value)
        self.is_red = True

    def __repr__(self):
        color_name = 'r' if self.is_red else 'b'
        return f"{super().__repr__()}({color_name})"


class RedBlackTree(BinaryTree):
    _allowed_types_ = (Number)
    _new_node_ = ColoredNode

    def add(self, value: _allowed_types_) -> None:
        super().add(value)
        print("add balancer here")

    def remove(self, value: _allowed_types_) -> None:
        super().remove(value)
        print("add balancer here")


if __name__ == '__main__':
    rbt = RedBlackTree()
    rbt.add(5)
    rbt.print()
