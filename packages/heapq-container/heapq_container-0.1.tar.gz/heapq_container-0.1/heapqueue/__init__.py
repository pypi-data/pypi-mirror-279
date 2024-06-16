import heapq
from collections import UserList
from typing import Iterable


class HeapQueue(UserList):
    """A class wrapper around the heapq library.

    Heaps are binary trees for which every parent node has a value less than or equal
    to any of its children.

    This module follows the python convention of both zero-indexing and pop returning
    the smallest item, not the largest (called a "min heap").

    By wrapping UserList this integrates the methods of `heapq` and presents the
    interface of a Collections-style data container type. `heap[0]` is the smallest
    item, and `heap.sort()` maintains the heap invariant! Note that iterating over the
    `heap` directly, say, in a list comprehension, will not return items in a sorted
    order. However, repeatedly popping the heap to exhaustion will.

    Complex records may be wrapped in a tuple (with careful thought given to ties),
    where tuple elements will be compared in positional order. Records can also be
    wrapped in a custom object. Dataclasses work well for this. See the heapq library
    documentation on the Priority Queue implementation for more, or look in this
    module's test suite for an example.
    """

    def __init__(self, iterable: Iterable = []) -> None:
        self.data = [i for i in iterable]
        heapq.heapify(self.data)

    def push(self, item):
        heapq.heappush(self.data, item)

    def pop(self):
        return heapq.heappop(self.data)

    def pushpop(self, item):
        return heapq.heappushpop(self.data, item)

    def replace(self, item):
        return heapq.heapreplace(self.data, item)

    def nsmallest(self, n):
        return heapq.nsmallest(n, self.data)

    def nlargest(self, n):
        return heapq.nlargest(n, self.data)
