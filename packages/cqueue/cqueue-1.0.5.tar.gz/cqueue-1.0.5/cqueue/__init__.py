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


"""Sophisticate Circular Queue"""


__all__: list = [
    "circularQueue",
    "linkedCircularQueue",
    "CapacityError",
    "QueueOverflowError",
    "QueueUnderflowError",
]


from linkedit import singlyLinkedList, _red, _green, _blue
from tabulate import tabulate


class CapacityError(Exception):
    pass


class QueueOverflowError(Exception):
    pass


class QueueUnderflowError(Exception):
    pass


class _capacity:
    def __init__(self: "_capacity", capacity: int) -> None:
        self.capacity = capacity

    @property
    def capacity(self: "_capacity") -> int:
        return self._capacity

    @capacity.setter
    def capacity(self: "_capacity", capacity: int) -> None:
        if not isinstance(capacity, int):
            raise CapacityError("Capacity must be an integer !")
        elif capacity < 0:
            raise CapacityError("Capacity must ba positif integer !")
        elif capacity == 0:
            raise CapacityError("Capacity must be greater than zero !")
        else:
            self._capacity: int = capacity


class circularQueue(_capacity):
    """Circular Queue Using Static Array"""

    def __init__(
        self: "circularQueue",
        data: object = [],
        *,
        capacity: int,
        detail: bool = False,
    ) -> None:
        super().__init__(capacity)
        self.size: int = 0
        self.detail: bool = detail
        self.queue: list = data

    @property
    def queue(self: "circularQueue") -> list:
        return self._queue

    @queue.setter
    def queue(
        self: "circularQueue",
        data: object,
    ) -> None:
        cqueue: list = []
        try:
            if self._capacity >= len(data):
                for i in data:
                    if i is not None:
                        cqueue.append(i)
                        self.size += 1
                for _ in range(self._capacity - self.size):
                    cqueue.append(None)
                self.enqueue_index: int = 0
                self.dequeue_index: int = 0
                for _ in range(self.size):
                    self.enqueue_index: int = (self.enqueue_index + 1) % self._capacity
                self._queue: list = cqueue
            else:
                raise CapacityError(
                    "Capacity must be greater than or equal the len of data"
                )
        except TypeError as e1:
            if data is not None:
                self.queue: list = [data]
            else:
                self.queue: list = []

    def enqueue(
        self: "circularQueue",
        data: object,
    ) -> None:
        if data is not None:
            if self.queue[self.enqueue_index] is None:
                self.queue[self.enqueue_index] = data
                self.size += 1
                self.enqueue_index: int = (self.enqueue_index + 1) % self._capacity
            else:
                raise QueueOverflowError("Queue is full !")

    def dequeue(
        self: "circularQueue",
    ) -> object:
        if self.queue[self.dequeue_index] is not None:
            returned_value: object = self.queue[self.dequeue_index]
            self.queue[self.dequeue_index] = None
            self.dequeue_index: int = (self.dequeue_index + 1) % self._capacity
            self.size -= 1
            return returned_value
        else:
            raise QueueUnderflowError("Queue is empty !")

    def peek(
        self: "linkedCircularQueue",
    ) -> object | object | bool:
        if self._queue[self.dequeue_index] is not None:
            return self._queue[self.dequeue_index]
        else:
            raise QueueUnderflowError("Queue is Empty !")

    def top(
        self: "linkedCircularQueue",
    ) -> object | object | bool:
        return self.peek()

    def isEmpty(self: "circularQueue") -> bool:
        return not self.size

    def isFull(self: "circularQueue") -> bool:
        return self.size == self._capacity

    def clear(self: "circularQueue") -> None:
        self._queue: list = [None] * self._capacity
        self.enqueue_index: int = 0
        self.dequeue_index: int = 0
        self.size: int = 0

    def __len__(self: "circularQueue") -> int:
        return self.size

    def __str__(self: "circularQueue") -> str:
        cqueue: list = [[] for _ in range(1) if self.detail]
        if self.detail:
            cqueue[0].append(_red("<- EXIT"))
        tracker_index: int = self.dequeue_index
        for _ in range(self._capacity):
            if self.queue[tracker_index] is not None:
                if not self.detail:
                    cqueue.append(self.queue[tracker_index])
                else:
                    if isinstance(self.queue[tracker_index], str):
                        if len(self.queue[tracker_index]) == 0:
                            cqueue[0].append(self.queue[tracker_index])
                        elif len(self.queue[tracker_index]) == 1:
                            cqueue[0].append(_blue(f"'{self.queue[tracker_index]}'"))
                        else:
                            cqueue[0].append(_blue(f'"{self.queue[tracker_index]}"'))
                    else:
                        cqueue[0].append(_blue(f"{self.queue[tracker_index]}"))
            else:
                if self.detail:
                    cqueue[0].append("")
            tracker_index: int = (tracker_index + 1) % self._capacity
        if self.detail:
            cqueue[0].append(_green("<- ENTER"))
            return f"{tabulate(cqueue, tablefmt='fancy_grid')}"
        return f"{cqueue}"


class linkedCircularQueue(_capacity):
    """Circular Queue Using Static Circular Singly Linked List"""

    def __init__(
        self: "linkedCircularQueue",
        data: object = [],
        *,
        capacity: int,
        detail: bool = False,
    ) -> None:
        super().__init__(capacity)
        self.size: int = 0
        self.detail: bool = detail
        self.queue: singlyLinkedList = data

    @property
    def queue(self: "linkedCircularQueue") -> singlyLinkedList:
        return self._queue

    @queue.setter
    def queue(
        self: "linkedCircularQueue",
        data: object,
    ) -> None:
        try:
            if self._capacity >= len(data):
                self._queue: singlyLinkedList = singlyLinkedList(
                    circular=True, detail=self.detail
                )
                for i in data:
                    if i is not None:
                        self._queue.append(i)
                        self.size += 1
                for _ in range(self._capacity - self.size):
                    self._queue.append(None)
                self.enqueue_index: object = self._queue._head
                self.dequeue_index: object = self._queue._head
                for _ in range(self.size):
                    self.enqueue_index: object = self.enqueue_index.next
            else:
                raise CapacityError(
                    "Capacity must be greater than or equal the len of data"
                )
        except TypeError as e2:
            if data is not None:
                self.queue: list = [data]
            else:
                self.queue: list = []

    def enqueue(
        self: "linkedCircularQueue",
        data: object,
    ) -> None:
        if self.enqueue_index.data is None:
            if data is not None:
                self.enqueue_index.data = data
                self.enqueue_index: object = self.enqueue_index.next
                self.size += 1
        else:
            raise QueueOverflowError("Queue is full !")

    def dequeue(
        self: "linkedCircularQueue",
    ) -> object | object | bool:
        if self.dequeue_index.data is not None:
            returned_value: object | object | bool = self.dequeue_index.data
            self.dequeue_index.data = None
            self.dequeue_index: object = self.dequeue_index.next
            self.size -= 1
            return returned_value
        else:
            raise QueueUnderflowError("Queue is empty !")

    def peek(
        self: "linkedCircularQueue",
    ) -> object | object | bool:
        if self.dequeue_index.data is not None:
            return self.dequeue_index.data
        else:
            raise QueueUnderflowError("Queue is empty !")

    def top(
        self: "linkedCircularQueue",
    ) -> object | object | bool:
        return self.peek()

    def isEmpty(self: "linkedCircularQueue") -> bool:
        return not self.size

    def isFull(self: "linkedCircularQueue") -> bool:
        return self.size == self._capacity

    def clear(self: "linkedCircularQueue") -> None:
        self._queue.clear()
        self._queue *= self._capacity
        self.enqueue_index: object = self._queue._head
        self.dequeue_index: object = self._queue._head
        self.size: int = 0

    def __len__(self: "linkedCircularQueue") -> int:
        return self.size

    def __str__(self: "linkedCircularQueue") -> str:
        cqueue: list = [[] for _ in range(1) if self.detail]
        if self.detail:
            cqueue[0].append(_red("<- EXIT"))
        now: object = self.dequeue_index
        for _ in range(self._capacity):
            if self.detail:
                if now.data is not None:
                    if isinstance(now.data, str):
                        if len(now.data) == 0:
                            cqueue[0].append(now.data)
                        elif len(now.data) == 1:
                            cqueue[0].append(_blue(f"'{now.data}'"))
                        else:
                            cqueue[0].append(_blue(f'"{now.data}"'))
                    else:
                        cqueue[0].append(_blue(f"{now.data}"))
                else:
                    cqueue[0].append("")
            else:
                if now.data is not None:
                    cqueue.append(now.data)
            now: object = now.next
        if self.detail:
            cqueue[0].append(_green("<- ENTER"))
            return f"{tabulate(cqueue, tablefmt='fancy_grid')}"
        return f"{cqueue}"


def _main() -> None:
    print("cqueue")


if __name__ == "__main__":
    _main()
