# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.abderrezzak@gmail.com>


"""Sophisticate Tree"""


__all__: list = ["binarySearchTree", "completeBinaryTree"]


from linkedit import singlyLinkedList, _red, _green, _blue, _yellow, _cyan, _white
from tabulate import tabulate


class _binaryTreeNode:
    def __init__(self: "_binaryTreeNode", data: int) -> None:
        self.lchild: None = None
        self.rchild: None = None
        self.data: int = data

    def left_child(self: "_binaryTreeNode") -> "_binaryTreeNode":
        return self.lchild

    def right_child(self: "_binaryTreeNode") -> "_binaryTreeNode":
        return self.rchild

    def get_data(self: "_binaryTreeNode") -> int:
        return self.data


class _binaryTree:
    def __init__(
        self: "_binaryTree",
        data: int | list | tuple | set | dict | bool | None = None,
        *,
        algorithm: str = "level-order",
    ) -> None:
        self.algorithm: str = algorithm
        self.counter: dict = {}
        self.root: _binaryTreeNode = data

    def __len__(self: "_binaryTree") -> int:
        return sum(self.counter.values())

    def __str__(self: "_binaryTree") -> str:
        if self._root:
            items: list = [
                [
                    _white("Current node"),
                    _white("Current node ") + _green("@") + _white("ddress"),
                    _white("Left child"),
                    _white("Left child ") + _green("@") + _white("ddress"),
                    _white("Right child"),
                    _white("Right child ") + _green("@") + _white("ddress"),
                ]
            ]
            counter: int = 0
            if self.algorithm == "pre-order":
                stack: list = [self._root]
                while stack:
                    node: _binaryTreeNode = stack.pop()
                    current_data: str = (
                        (
                            _blue(f"{node.data}")
                            if self.counter[node.data] == 1
                            else _blue(f"{node.data} ")
                            + _green("(")
                            + _red(f"{self.counter[node.data]}")
                            + _green(")")
                        )
                        if node.data != self._root.data
                        else (
                            (
                                _blue(f"{node.data} ")
                                + _green("(")
                                + _red("Root")
                                + _green(") ")
                            )
                            + (
                                (
                                    _green("(")
                                    + _red(f"{self.counter[node.data]}")
                                    + _green(")")
                                )
                                if self.counter[node.data] > 1
                                else ""
                            )
                        )
                    )
                    try:
                        left_data: str = _blue(f"{node.lchild.data} ") + (
                            (
                                _green("(")
                                + _red(f"{self.counter[node.lchild.data]}")
                                + _green(")")
                            )
                            if self.counter[node.lchild.data] > 1
                            else ""
                        )
                    except AttributeError as e1:
                        left_data: str = _blue("None")
                    try:
                        right_data: str = _blue(f"{node.rchild.data} ") + (
                            (
                                _green("(")
                                + _red(f"{self.counter[node.rchild.data]}")
                                + _green(")")
                            )
                            if self.counter[node.rchild.data] > 1
                            else ""
                        )
                    except AttributeError as e2:
                        right_data: str = _blue("None")
                    current_address: str = (
                        _yellow(f"{hex(id(node))}")
                        if counter % 2 == 0
                        else _red(f"{hex(id(node))}")
                    )
                    counter += 1
                    left_address: str = (
                        (
                            _yellow(f"{hex(id(node.lchild))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(node.lchild))}")
                        )
                        if node.lchild is not None
                        else _cyan(f"{hex(id(node.lchild))} ")
                        + _yellow("(")
                        + _red("nil")
                        + _yellow("/")
                        + _red("0x0")
                        + _yellow(")")
                    )
                    counter += 1
                    right_address: str = (
                        (
                            _yellow(f"{hex(id(node.rchild))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(node.rchild))}")
                        )
                        if node.rchild is not None
                        else _cyan(f"{hex(id(node.rchild))} ")
                        + _yellow("(")
                        + _red("nil")
                        + _yellow("/")
                        + _red("0x0")
                        + _yellow(")")
                    )
                    counter += 1
                    items.append(
                        [
                            current_data,
                            current_address,
                            _blue(f"{left_data}"),
                            left_address,
                            _blue(f"{right_data}"),
                            right_address,
                        ]
                    )
                    if node.rchild:
                        stack.append(node.rchild)
                    if node.lchild:
                        stack.append(node.lchild)
            elif self.algorithm == "in-order":
                stack: list = []
                root: _binaryTreeNode = self._root
                while stack or root:
                    while root:
                        stack.append(root)
                        root: _binaryTreeNode | None = root.lchild
                    node: _binaryTreeNode = stack.pop()
                    current_data: str = (
                        (
                            _blue(f"{node.data}")
                            if self.counter[node.data] == 1
                            else _blue(f"{node.data} ")
                            + _green("(")
                            + _red(f"{self.counter[node.data]}")
                            + _green(")")
                        )
                        if node != self._root
                        else (
                            (
                                _blue(f"{node.data} ")
                                + _green("(")
                                + _red("Root")
                                + _green(") ")
                            )
                            + (
                                (
                                    _green("(")
                                    + _red(f"{self.counter[node.data]}")
                                    + _green(")")
                                )
                                if self.counter[node.data] > 1
                                else ""
                            )
                        )
                    )
                    try:
                        left_data: str = _blue(f"{node.lchild.data} ") + (
                            (
                                _green("(")
                                + _red(f"{self.counter[node.lchild.data]}")
                                + _green(")")
                            )
                            if self.counter[node.lchild.data] > 1
                            else ""
                        )
                    except AttributeError as e3:
                        left_data: str = _blue("None")
                    try:
                        right_data: str = _blue(f"{node.rchild.data} ") + (
                            (
                                _green("(")
                                + _red(f"{self.counter[node.rchild.data]}")
                                + _green(")")
                            )
                            if self.counter[node.rchild.data] > 1
                            else ""
                        )
                    except AttributeError as e4:
                        right_data: str = _blue("None")
                    current_address: str = (
                        _yellow(f"{hex(id(node))}")
                        if counter % 2 == 0
                        else _red(f"{hex(id(node))}")
                    )
                    counter += 1
                    left_address: str = (
                        (
                            _yellow(f"{hex(id(node.lchild))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(node.lchild))}")
                        )
                        if node.lchild is not None
                        else _cyan(f"{hex(id(node.lchild))} ")
                        + _yellow("(")
                        + _red("nil")
                        + _yellow("/")
                        + _red("0x0")
                        + _yellow(")")
                    )
                    counter += 1
                    right_address: str = (
                        (
                            _yellow(f"{hex(id(node.rchild))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(node.rchild))}")
                        )
                        if node.rchild is not None
                        else _cyan(f"{hex(id(node.rchild))} ")
                        + _yellow("(")
                        + _red("nil")
                        + _yellow("/")
                        + _red("0x0")
                        + _yellow(")")
                    )
                    counter += 1
                    items.append(
                        [
                            current_data,
                            current_address,
                            left_data,
                            left_address,
                            right_data,
                            right_address,
                        ]
                    )
                    root: _binaryTreeNode | None = node.rchild
            elif self.algorithm == "post-order":
                stack: list = []
                last_visited: None = None
                root: _binaryTreeNode = self._root
                while stack or root:
                    while root:
                        stack.append(root)
                        root: _binaryTreeNode | None = root.lchild
                    top: _binaryTreeNode = stack[-1]
                    if top.rchild and last_visited is not top.rchild:
                        root: _binaryTreeNode = top.rchild
                    else:
                        current_data: str = (
                            (
                                _blue(f"{top.data}")
                                if self.counter[top.data] == 1
                                else _blue(f"{top.data} ")
                                + _green("(")
                                + _red(f"{self.counter[top.data]}")
                                + _green(")")
                            )
                            if top is not self._root
                            else (
                                (
                                    _blue(f"{top.data} ")
                                    + _green("(")
                                    + _red("Root")
                                    + _green(") ")
                                )
                                + (
                                    (
                                        _green("(")
                                        + _red(f"{self.counter[top.data]}")
                                        + _green(")")
                                    )
                                    if self.counter[top.data] > 1
                                    else ""
                                )
                            )
                        )
                        try:
                            left_data: str = _blue(f"{top.lchild.data} ") + (
                                (
                                    _green("(")
                                    + _red(f"{self.counter[top.lchild.data]}")
                                    + _green(")")
                                )
                                if self.counter[top.lchild.data] > 1
                                else ""
                            )
                        except AttributeError as e5:
                            left_data: str = _blue("None")
                        try:
                            right_data: str = _blue(f"{top.rchild.data} ") + (
                                (
                                    _green("(")
                                    + _red(f"{self.counter[top.rchild.data]}")
                                    + _green(")")
                                )
                                if self.counter[top.rchild.data] > 1
                                else ""
                            )
                        except AttributeError as e6:
                            right_data: str = _blue("None")
                        current_address: str = (
                            _yellow(f"{hex(id(top))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(top))}")
                        )
                        counter += 1
                        left_address: str = (
                            (
                                _yellow(f"{hex(id(top.lchild))}")
                                if counter % 2 == 0
                                else _red(f"{hex(id(top.lchild))}")
                            )
                            if top.lchild is not None
                            else _cyan(f"{hex(id(top.lchild))} ")
                            + _yellow("(")
                            + _red("nil")
                            + _yellow("/")
                            + _red("0x0")
                            + _yellow(")")
                        )
                        counter += 1
                        right_address: str = (
                            (
                                _yellow(f"{hex(id(top.rchild))}")
                                if counter % 2 == 0
                                else _red(f"{hex(id(top.rchild))}")
                            )
                            if top.rchild is not None
                            else _cyan(f"{hex(id(top.rchild))} ")
                            + _yellow("(")
                            + _red("nil")
                            + _yellow("/")
                            + _red("0x0")
                            + _yellow(")")
                        )
                        counter += 1
                        items.append(
                            [
                                current_data,
                                current_address,
                                left_data,
                                left_address,
                                right_data,
                                right_address,
                            ]
                        )
                        last_visited: _binaryTreeNode = stack.pop()
            elif self.algorithm == "level-order":
                queue: singlyLinkedList = singlyLinkedList(self._root)
                while queue:
                    node: _binaryTreeNode = queue.pop(0)
                    current_data: str = (
                        (
                            _blue(f"{node.data}")
                            if self.counter[node.data] == 1
                            else _blue(f"{node.data} ")
                            + _green("(")
                            + _red(f"{self.counter[node.data]}")
                            + _green(")")
                        )
                        if node.data != self._root.data
                        else (
                            (
                                _blue(f"{node.data} ")
                                + _green("(")
                                + _red("Root")
                                + _green(") ")
                            )
                            + (
                                (
                                    _green("(")
                                    + _red(f"{self.counter[node.data]}")
                                    + _green(")")
                                )
                                if self.counter[node.data] > 1
                                else ""
                            )
                        )
                    )
                    try:
                        left_data: str = _blue(f"{node.lchild.data} ") + (
                            (
                                _green("(")
                                + _red(f"{self.counter[node.lchild.data]}")
                                + _green(")")
                            )
                            if self.counter[node.lchild.data] > 1
                            else ""
                        )
                    except AttributeError as e7:
                        left_data: str = _blue("None")
                    try:
                        right_data: str = _blue(f"{node.rchild.data} ") + (
                            (
                                _green("(")
                                + _red(f"{self.counter[node.rchild.data]}")
                                + _green(")")
                            )
                            if self.counter[node.rchild.data] > 1
                            else ""
                        )
                    except AttributeError as e8:
                        right_data: str = _blue("None")
                    current_address: str = (
                        _yellow(f"{hex(id(node))}")
                        if counter % 2 == 0
                        else _red(f"{hex(id(node))}")
                    )
                    counter += 1
                    left_address: str = (
                        (
                            _yellow(f"{hex(id(node.lchild))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(node.lchild))}")
                        )
                        if node.lchild is not None
                        else _cyan(f"{hex(id(node.lchild))} ")
                        + _yellow("(")
                        + _red("nil")
                        + _yellow("/")
                        + _red("0x0")
                        + _yellow(")")
                    )
                    counter += 1
                    right_address: str = (
                        (
                            _yellow(f"{hex(id(node.rchild))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(node.rchild))}")
                        )
                        if node.rchild is not None
                        else _cyan(f"{hex(id(node.rchild))} ")
                        + _yellow("(")
                        + _red("nil")
                        + _yellow("/")
                        + _red("0x0")
                        + _yellow(")")
                    )
                    counter += 1
                    items.append(
                        [
                            current_data,
                            current_address,
                            _blue(f"{left_data}"),
                            left_address,
                            _blue(f"{right_data}"),
                            right_address,
                        ]
                    )
                    if node.lchild:
                        queue.append(node.lchild)
                    if node.rchild:
                        queue.append(node.rchild)
            else:
                raise SyntaxError("No algorithm with this name")
            return tabulate(items, headers="firstrow", tablefmt="fancy_grid")
        else:
            raise TypeError("Empty binary tree !")


class binarySearchTree(_binaryTree):
    @property
    def root(self: "binarySearchTree") -> _binaryTreeNode:
        return self._root

    @root.setter
    def root(
        self: "binarySearchTree", data: int | list | tuple | set | dict | bool | None
    ) -> None:
        valid_data_types: list = [int, list, tuple, set, dict, bool]
        if type(data) not in valid_data_types and data != None:
            raise TypeError("Invalid data type !")
        self._root: None = None
        try:
            if len(data) > 0:
                for i in data:
                    self.add(i)
        except TypeError as e0:
            if isinstance(data, int):
                self.add(data)

    def add(self: "binarySearchTree", value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Just integer supported in binary search tree !")
        if not self._root:
            self._root: _binaryTreeNode = _binaryTreeNode(value)
            self.counter[value] = 1
        else:
            root: _binaryTreeNode = self._root
            while True:
                if value < root.data:
                    if root.lchild is not None:
                        root: _binaryTreeNode = root.lchild
                    else:
                        root.lchild = _binaryTreeNode(value)
                        self.counter[value] = 1
                        break
                elif value > root.data:
                    if root.rchild is not None:
                        root: _binaryTreeNode = root.rchild
                    else:
                        root.rchild = _binaryTreeNode(value)
                        self.counter[value] = 1
                        break
                else:
                    self.counter[value] += 1
                    break

    def search(self: "binarySearchTree", value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("just integer supported in binary search tree !")
        if not self._root:
            raise TypeError("Empty binary search tree !")
        else:
            path: list = []
            root: _binaryTreeNode = self._root
            while root:
                if value < root.data:
                    path.append(root.data)
                    root: _binaryTreeNode | None = root.lchild
                elif value > root.data:
                    path.append(root.data)
                    root: _binaryTreeNode | None = root.rchild
                else:
                    print(
                        f"Found after {len(path)} step"
                        + (f"s with the path : {path}" if len(path) > 1 else "")
                    )
                    break
            else:
                print("Not found")

    def remove(self: "binarySearchTree", value: int) -> None:
        if self._root:
            root: _binaryTreeNode = self._root
            while root:
                if value < root.data:
                    if root.lchild is not None:
                        if root.lchild.data == value:
                            if self.counter[value] == 1:
                                if (
                                    root.lchild.lchild is None
                                    and root.lchild.rchild is None
                                ):
                                    root.lchild = None
                                    self.counter[value] = 0
                                    break
                                else:
                                    if (
                                        root.lchild.lchild is not None
                                        and root.lchild.rchild is None
                                    ):
                                        root.lchild = root.lchild.lchild
                                        self.counter[value] = 0
                                        break
                                    elif (
                                        root.lchild.lchild is None
                                        and root.lchild.rchild is not None
                                    ):
                                        root.lchild = root.lchild.rchild
                                        self.counter[value] = 0
                                        break
                                    else:
                                        helper: _binaryTreeNode = root.lchild.lchild
                                        try:
                                            while helper.rchild.rchild:
                                                helper: _binaryTreeNode = helper.rchild
                                            root.lchild.data = helper.rchild.data
                                            helper.rchild = None
                                            self.counter[value] = 0
                                            break
                                        except AttributeError as e9:
                                            helper2 = root.lchild.rchild
                                            root.lchild = helper
                                            root.lchild.rchild = helper2
                                            self.counter[value] = 0
                                            break
                            else:
                                self.counter[value] -= 1
                                break
                        else:
                            root: _binaryTreeNode | None = root.lchild
                    else:
                        raise ValueError("Not found")
                elif value > root.data:
                    if root.rchild is not None:
                        if root.rchild.data == value:
                            if self.counter[value] == 1:
                                if (
                                    root.rchild.lchild is None
                                    and root.rchild.rchild is None
                                ):
                                    root.rchild = None
                                    self.counter[value] = 0
                                    break
                                else:
                                    if (
                                        root.rchild.lchild is not None
                                        and root.rchild.rchild is None
                                    ):
                                        root.rchild = root.rchild.lchild
                                        self.counter[value] = 0
                                        break
                                    elif (
                                        root.rchild.lchild is None
                                        and root.rchild.rchild is not None
                                    ):
                                        root.rchild = root.rchild.rchild
                                        self.counter[value] = 0
                                        break
                                    else:
                                        helper: _binaryTreeNode = root.rchild.lchild
                                        try:
                                            while helper.rchild.rchild:
                                                helper: _binaryTreeNode = helper.rchild
                                            root.rchild.data = helper.rchild.data
                                            helper.rchild = None
                                            self.counter[value] = 0
                                            break
                                        except AttributeError as e10:
                                            helper2 = root.rchild.rchild
                                            root.rchild = helper
                                            root.rchild.rchild = helper2
                                            self.counter[value] = 0
                                            break
                            else:
                                self.counter[value] -= 1
                                break
                        else:
                            root: _binaryTreeNode | None = root.rchild
                    else:
                        raise ValueError("Not found")
                else:
                    if self.counter[value] == 1:
                        if root.lchild is None and root.rchild is None:
                            self._root: None = None
                            self.counter[value] = 0
                            break
                        elif root.lchild is None and root.rchild is not None:
                            self._root: _binaryTreeNode = root.rchild
                            self.counter[value] = 0
                            break
                        elif root.lchild is not None and root.rchild is None:
                            self._root: _binaryTreeNode = root.lchild
                            self.counter[value] = 0
                            break
                        else:
                            if (
                                root.lchild.lchild is None
                                and root.lchild.rchild is None
                            ):
                                root.data = root.lchild.data
                                root.lchild = None
                                self.counter[value] = 0
                                break
                            else:
                                helper: _binaryTreeNode = root.lchild
                                try:
                                    while helper.rchild.rchild:
                                        helper: _binaryTreeNode = helper.rchild
                                    root.data = helper.rchild.data
                                    helper.rchild = None
                                    self.counter[value] = 0
                                    break
                                except AttributeError as e11:
                                    root.data = helper.data
                                    root.lchild = root.lchild.lchild
                                    self.counter[value] = 0
                                    break
                    else:
                        self.counter[value] -= 1
                        break
        else:
            raise TypeError("Empty binary search tree !")

    def max(self: "binarySearchTree") -> int:
        if self._root:
            root: _binaryTreeNode = self._root
            while root.rchild:
                root: _binaryTreeNode = root.rchild
            return root.data
        else:
            raise TypeError("Empty binary search tree !")

    def min(self: "binarySearchTree") -> int:
        if self._root:
            root: _binaryTreeNode = self._root
            while root.lchild:
                root: _binaryTreeNode = root.lchild
            return root.data
        else:
            raise TypeError("Empty binary search tree !")


class bst(binarySearchTree):
    pass


class completeBinaryTree(_binaryTree):
    @property
    def root(self: "completeBinaryTree") -> _binaryTreeNode:
        return self._root

    @root.setter
    def root(
        self: "completeBinaryTree", data: int | list | tuple | set | dict | bool | None
    ) -> None:
        if isinstance(data[0], int):
            self._root: _binaryTreeNode = _binaryTreeNode(data[0])
            self.counter[data[0]] = 1
            queue: singlyLinkedList = singlyLinkedList(self._root)
        else:
            raise ValueError("Just integer supported in complete binary tree !")
        for i in range(len(data) // 2):
            if isinstance(data[i], int):
                node: _binaryTreeNode = queue.pop(0)
                try:
                    if isinstance(data[(i * 2) + 1], int):
                        if data[(i * 2) + 1] not in self.counter:
                            node.lchild = _binaryTreeNode(data[(i * 2) + 1])
                            queue.append(node.lchild)
                            self.counter[data[(i * 2) + 1]] = 1
                        else:
                            self.counter[data[(i * 2) + 1]] += 1
                    else:
                        raise ValueError(
                            "Just integer supported in complete binary tree !"
                        )
                except IndexError as e12:
                    pass
                try:
                    if isinstance(data[(i * 2) + 2], int):
                        if data[(i * 2) + 2] not in self.counter:
                            node.rchild = _binaryTreeNode(data[(i * 2) + 2])
                            queue.append(node.rchild)
                            self.counter[data[(i * 2) + 2]] = 1
                        else:
                            self.counter[data[(i * 2) + 2]] += 1
                    else:
                        raise ValueError(
                            "Just integer supported in complete binary tree !"
                        )
                except IndexError as e13:
                    pass
            else:
                raise ValueError("Just integer supported in complete binary tree !")


class cbt(completeBinaryTree):
    pass


def _main() -> None:
    print("threes")


if __name__ == "__main__":
    _main()
