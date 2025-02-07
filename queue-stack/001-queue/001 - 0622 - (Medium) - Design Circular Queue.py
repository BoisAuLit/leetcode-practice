"""
动态图: https://leetcode.com/explore/learn/card/queue-stack/228/first-in-first-out-data-structure/1396/
"""


class MyCircularQueue:
    def __init__(self, k: int):
        self.capacity = k
        self.data = [None] * k
        self.head = self.tail = -1
        self.size = 0

    def enQueue(self, value: int) -> bool:
        if self.head == -1:
            self.head = self.tail = 0
            self.data[0] = value
            self.size += 1
            return True
        if self.isFull():
            return False
        self.tail = (self.tail + 1) % self.capacity
        self.data[self.tail] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        if self.size == 1:
            self.head = self.tail = -1
            self.size -= 1
            return True

        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return True

    # ! Get most recently enqueued element
    def Front(self) -> int:
        if self.head == -1:
            return -1
        return self.data[self.head]

    # ! Get oldest enqueued element
    def Rear(self) -> int:
        if self.tail == -1:
            return -1
        return self.data[self.tail]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity

    # def print(self) -> None:
    #     # print("\n")
    #     print("\tData:", self.data)
    #     print("\tSize:", self.size)
    #     print("\tCapacity:", self.capacity)
    #     print("\tHead:", self.head)
    #     print("\tTail:", self.tail)
    #     print("\tIs full:", self.isFull())
    #     # print("\n")


# ! Test case 1
# obj = MyCircularQueue(3)
# print(obj.enQueue(1))  # Return True
# print(obj.enQueue(2))  # Return True
# print(obj.enQueue(3))  # Return True
# print(obj.enQueue(4))  # Return False
# print(obj.Rear())  # Return 3
# print(obj.isFull())  # Return True
# print(obj.deQueue())  # Return True
# print(obj.enQueue(4))  # Return True
# print(obj.Rear())  # Return 4

# ! Test case 2
obj = MyCircularQueue(2)
print(obj.enQueue(1))  # Return True
print(obj.enQueue(2))  # Return True
print(obj.deQueue())  # Return True
print(obj.enQueue(3))  # Return True
print(obj.deQueue())  # Return True
print(obj.enQueue(3))  # Return True
print(obj.deQueue())  # Return True
print(obj.enQueue(3))  # Return True
print(obj.deQueue())  # Return True
print(obj.Front())
