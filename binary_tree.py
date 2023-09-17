from numbers import Number
from types import NoneType


class Node:
    """
    Базовый класс узлов дерева
    Просто сохраняйте значения

    Методы:
    __init__: конструктор
    __repr__: Логика представления Obj для методов print и str
    __lt__ и __gt__: позволяют использовать операции сравнения '<' и '>'
    """
    def __init__(self, value: object):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)

    def __lt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Unable to compare {type(self).__name__} and {type(other).__name__} objects")
        return self.value.__lt__(other.value)

    def __gt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Unable to compare {type(self).__name__} and {type(other).__name__} objects")
        return self.value.__gt__(other.value)


class BinaryTree:
    """
    Класс BinaryTree.
    Реализует двоичное дерево

    Атрибуты:
    _allowed_types_: кортеж[объект]
    Управляйте тем, какие объекты разрешено хранить внутри элементов дерева
    Объекты должны реализовывать по крайней мере методы __lt__ и __gt__
    _new_node_: введите
    Управляет тем, какой объект будет предоставлять элемент узла дерева

    Методы:
    __init__(root: _allowed_types_ | NoneType = Нет)
    Конструктор, создайте пустое дерево, или установите корневой элемент в качестве узла, или создайте корневой элемент с $root в качестве значения
    добавить(значение: _allowed_types_) -> Нет
    Добавьте элементы в дерево. Проверяет тип значения на соответствие _allowed_types_
    удалить(значение: _allowed_types_) -> Нет
    элемента поиска в дереве по значению $ и удалить его
    поиск(значение: _allowed_types_) -> Node | None
    Элемент поиска в дереве и возвращает его или None
    печать(node: Node | None = None, filter_none: bool = False) -> None
    Печать дерева, начиная с $node или tree.root
    Если задано значение $filter_none, то замаскируйте все значения 'None' под пустые элементы
    __len__: разрешить использовать встроенную функцию len() над объектом
    """
    # _allowed_types_ содержит узел в качестве примера
    _allowed_types_ = (Node, Number)
    # TODO: может быть, использовать какой-либо шаблон для создания элементов такого типа? (пока это будет работать)
    _new_node_ = Node

    def __init__(self, root: object | None = None):
        if isinstance(root, (Node, NoneType)):
            # TODO: проверьте тип node.value на соответствие self._ разрешенные_типы_ ?
            self.root = root
        else:
            self.root = None
            self.add(root)

    def __len__(self):
        """
        повторно используйте метод _get_as_rows_ и подсчитывайте непустые элементы
        """
        # TODO: есть ли способ упростить это?
        return len([True for row in self._get_as_rows_(self.root) for el in row if el is not None])

    def add(self, value: _allowed_types_) -> None:
        """
        Добавьте элементы в дерево. Проверяет тип значения на соответствие _allowed_types_

        Параметры:
        значение: Значение для добавления

       Повышения:
       TypeError: при неправильном типе значения
       ValueError: если узел со значением уже находится в дереве
        """
        if not isinstance(value, self._allowed_types_):
            allowed_type_names = [t.__name__ for t in self._allowed_types_]
            raise TypeError(f"For value expected one of types {allowed_type_names}, got {type(value).__name__}")
        node, parent = self._search_(value, self.root)
        if node is None:
            el = self._new_node_(value)
            if parent is None:
                self.root = el
            else:
                if value < parent.value:
                    parent.left = el
                else:
                    parent.right = el
        else:
            raise ValueError(f"Element with value {value} already exists in the tree")

    def remove(self, value: _allowed_types_) -> None:
        """
        Найдите элемент в дереве по значению $ и удалите его

        Параметры:
            значение: Значение для удаления

        Повышения:
            ValueError: если узел со значением не существует в дереве
        """
        node, parent = self._search_(value, self.root)
        if node:
            if node.left is None and node.right is None:
                new_child = None
            elif node.left and node.right:
                right_min_node, right_min_node_parent = self._min_(node.right)
                if right_min_node_parent:
                    right_min_node_parent.left = None
                right_min_node.left = node.left
                if right_min_node != node.right:
                    right_min_node.right = node.right
                new_child = right_min_node
            else:
                new_child = node.left if node.left else node.right
            if node.value < parent.value:
                parent.left = new_child
            else:
                parent.right = new_child
        else:
            raise IndexError(f"Unable to delete value {value} that is not in the tree")

    def _search_(self, value: _allowed_types_,
                 node: Node,
                 parent: Node | None = None) -> tuple[Node | None, Node | None]:
        """
        Метод внутреннего
        поиска Поиск узла со значением $ и его родительского элемента
        Поиск начинается с $node

        Параметры:
            значение: Значение для поиска
            узел: с какого узла начать поиск
            родительский узел (необязательно): точки на текущем родительском узле, используемые для целей рекурсии
        """
        if node is None or node.value == value:
            return node, parent
        if value < node.value:
            return self._search_(value, node.left, node)
        else:
            return self._search_(value, node.right, node)

    def search(self, value: _allowed_types_) -> Node | None:
        """
        Найдите элемент в дереве и верните его или нет
        Поиск всегда начинается с корня дерева

        Параметры:
            значение: Значение для поиска
        """
        return self._search_(value, self.root)[0]

    @staticmethod
    def _get_as_rows_(node: Node) -> list[list[_allowed_types_]]:
        """
        Представлять дерево в виде строк
        Не включающий ни одного элемента

        Параметры:
            узел: с какого узла начинать
        """
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
    def _max_(node: Node) -> tuple[Node | None, Node | None]:
        """
        Sпоиск максимального элемента в дереве, начинающегося с $node

         Параметры:
            узел: с какого узла начинать
        """
        parent = None
        if node:
            while node.right:
                parent = node
                node = node.right
        return node, parent

    @staticmethod
    def _min_(node: Node) -> tuple[Node | None, Node | None]:
        """
        Поиск минимального элемента в дереве, начинающегося с $node

        Параметры:
            узел: с какого узла начинать
        """
        parent = None
        if node:
            while node.left:
                parent = node
                node = node.left
        return node, parent

    def print(self, node: Node | None = None, filter_none: bool = False) -> None:
        """
        Вывести дерево, начиная с $node или корня дерева
        Если задано значение $filter_none, то замаскируйте все значения 'None' под пустые элементы

         Параметры:
            узел (необязательно): с какого узла начать поиск, используйте корень дерева, если не задано
            filter_none(необязательно): маскирует все значения 'None' для пустых элементов при установке
        """
        # TODO: is there a way to simplify this?
        if not node:
            node = self.root
        tree_rows = self._get_as_rows_(node)
        if filter_none:
            tree_rows = [[el if el is not None else ' ' for el in row] for row in tree_rows]
        longest_row_len = max((len(row) for row in tree_rows), default=0)
        # максимальный элемент дерева не обязательно должен быть самым длинным
        # так что ищите самый длинный, проверяя len(str(el))
        longest_el_size = max((len(str(el)) for row in tree_rows for el in row), default=0)+1
        for row in tree_rows:
            print(''.join(str(el).center(longest_el_size*longest_row_len//len(row)) for el in row))


if __name__ == '__main__':
    print("This is internal class, launch main.py")
