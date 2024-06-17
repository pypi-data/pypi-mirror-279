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


"""Sophisticate Stack"""


__all__: list = [
    "linkedStack",
    "CapacityError",
    "StackOverflowError",
    "StackUnderflowError",
]


from linkedit import doublyLinkedList, _red, _green, _blue
from tabulate import tabulate


class CapacityError(Exception):
    pass


class StackOverflowError(Exception):
    pass


class StackUnderflowError(Exception):
    pass


class linkedStack:
    """Stack Using Static Non Circular Doubly Linked List"""

    def __init__(
        self: "linkedStack",
        data: object = None,
        *,
        capacity: int,
        detail: bool = False,
    ) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.detail: bool = detail
        self.stack: doublyLinkedList = data

    @property
    def capacity(self: "linkedStack") -> int:
        return self._capacity

    @capacity.setter
    def capacity(self: "linkedStack", capacity: int) -> None:
        if not isinstance(capacity, int):
            raise CapacityError("Capacity must be an integer !")
        elif capacity < 0:
            raise CapacityError("Capacity must ba positif integer !")
        elif capacity == 0:
            raise CapacityError("Capacity must be greater than zero !")
        else:
            self._capacity: int = capacity

    @property
    def stack(self: "linkedStack") -> doublyLinkedList:
        return self._stack

    @stack.setter
    def stack(
        self: "linkedStack",
        data: object,
    ) -> None:
        try:
            if len(data) > self._capacity:
                raise CapacityError(
                    "Capacity must be greater than or equal the len of data"
                )
            else:
                self._stack = doublyLinkedList(detail=self.detail)
                for i in data:
                    if i is not None:
                        self._stack.append(i)
                        self.size += 1
                for _ in range(self._capacity - self.size):
                    self._stack.append(None)
                self.push_index: object = self._stack._head
                for _ in range(self.size):
                    self.push_index: object | None = self.push_index.next
                self.pop_index: None | object = self.push_index.prev
        except TypeError as e1:
            if data is not None:
                self.stack: list = [data]
            else:
                self.stack: list = []
        except AttributeError as e2:
            self.pop_index: object = self._stack._tail

    def push(
        self: "linkedStack",
        data: object,
    ) -> None:
        if self.size != self._capacity:
            if data is not None:
                self.push_index.data = data
                self.size += 1
                self.push_index: object | None = self.push_index.next
                if self.pop_index is not None:
                    self.pop_index: object = self.pop_index.next
                else:
                    self.pop_index: object = self._stack._head
        else:
            raise StackOverflowError("Stack is full !")

    def pop(self: "linkedStack") -> None:
        if not self.size:
            raise StackUnderflowError("Stack is empty !")
        else:
            returned_value: object = self.pop_index.data
            self.pop_index.data = None
            self.size -= 1
            self.pop_index: object | None = self.pop_index.prev
            if self.push_index is None:
                self.push_index: object = self._stack._tail
            else:
                self.push_index: object = self.push_index.prev
            return returned_value

    def __str__(self: "linkedStack") -> str:
        stack: list = []
        if self.detail:
            stack.append(
                [
                    _green("ENTER")
                    + _red("  ^")
                    + "\n"
                    + " " * len("En")
                    + _green("|")
                    + " " * len("er  ")
                    + _red("|")
                    + "\n"
                    + " " * len("En")
                    + _green("v")
                    + " " * len("er ")
                    + _red("EXIT")
                ]
            )
            for _ in range(self._capacity - self.size):
                stack.append([""])
            tracker: object = self.pop_index
        else:
            tracker: object = self._stack._head
        for _ in range(self.size):
            if self.detail:
                if not isinstance(tracker.data, str):
                    stack.append([_blue(f"{tracker.data}")])
                else:
                    if len(tracker.data) == 0:
                        stack.append([tracker.data])
                    elif len(tracker.data) == 1:
                        stack.append([_blue(f"'{tracker.data}'")])
                    else:
                        stack.append([_blue(f'"{tracker.data}"')])
                tracker: object | None = tracker.prev
            else:
                stack.append(tracker.data)
                tracker: object | None = tracker.next
        if self.detail:
            return tabulate(stack, tablefmt="fancy_grid")
        else:
            return f"{stack}"

    def __len__(self: "linkedStack") -> int:
        return self.size

    def isEmpty(self: "linkedStack") -> bool:
        return not self.size

    def isFull(self: "linkedStack") -> bool:
        return self.size == self._capacity

    def peek(
        self: "linkedStack",
    ) -> object:
        if self.pop_index is not None:
            return self.pop_index.data
        else:
            raise StackUnderflowError("Stack is empty !")

    def top(
        self: "linkedStack",
    ) -> object:
        return self.peek()

    def clear(self: "linkedStack") -> None:
        self._stack.clear()
        self._stack *= self._capacity
        self.push_index: object = self._stack._head
        self.pop_index: None = None
        self.size: int = 0


def _main() -> None:
    print("lstack")


if __name__ == "__main__":
    _main()
