
from .Comparer import Comparer


class Heap:
    def __init__(self, comparer: Comparer):
        self.arr = []
        self.comparer = comparer

    def push(self, val) -> None:
        res = -1
        curr_index = len(self)
        self.arr.append(val)
        parent_index = curr_index//2 - (1 - curr_index % 2)
        while res < 0 and parent_index >= 0:
            res = self.comparer.compare(self[parent_index], self[curr_index])
            if res < 0:
                self.arr[parent_index], self.arr[curr_index] = self[curr_index], self[parent_index]
                curr_index = parent_index
                parent_index = curr_index//2 - (1 - curr_index % 2)

    def __len__(self):
        return len(self.arr)

    def __getitem__(self, index: int):
        return self.arr[index]

    def is_empty(self) -> bool:
        return len(self) == 0

    def pop(self):
        res = self[0]
        self.arr[0], self.arr[-1] = self[-1], self[0]
        self.arr.pop()
        flag = True
        curr_index = 0
        while flag:
            child1_index = curr_index*2+1
            child2_index = curr_index*2+2
            if len(self) > child2_index:
                if self.comparer.compare(self[child1_index], self[child2_index]) < 0:
                    self.arr[curr_index], self.arr[child2_index] = self[child2_index], self[curr_index]
                    curr_index = child2_index
                elif self.comparer.compare(self[child1_index], self[child2_index]) > 0:
                    self.arr[curr_index], self.arr[child1_index] = self[child1_index], self[curr_index]
                    curr_index = child1_index
                else:
                    flag = False
            else:
                if len(self) > child1_index:
                    if self.comparer.compare(self[child1_index], self[curr_index]) > 0:
                        self.arr[curr_index], self.arr[child1_index] = self[child1_index], self[curr_index]
                        curr_index = child1_index
                    else:
                        flag = False
                else:
                    flag = False
        return res

    def __str__(self):
        return str(self.arr)

    def peek(self):
        return self[0]


class MaxHeap(Heap):
    def __init__(self):
        super().__init__(Comparer.GREATER)


class MinHeap(Heap):
    def __init__(self):
        super().__init__(Comparer.SMALLER)


__all__ = [
    "Heap",
    "MaxHeap",
    "MinHeap",
]
