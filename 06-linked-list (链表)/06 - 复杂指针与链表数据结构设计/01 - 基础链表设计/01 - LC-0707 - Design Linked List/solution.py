# Design using singly linked list


class Node:
    def __init__(self, val: int):
        self.val = val
        self.next = None


class MyLinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    def get(self, index: int) -> int:
        if self.head is None or not 0 <= index <= self.size - 1:
            return -1
        node = self.head
        for _ in range(index):
            node = node.next
        return node.val

    def addAtHead(self, val: int) -> None:
        new_node = Node(val)
        self.size += 1
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def addAtTail(self, val: int) -> None:
        new_node = Node(val)
        self.size += 1
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def addAtIndex(self, index: int, val: int) -> None:
        if index == 0:
            self.addAtHead(val)
        elif index == self.size:
            self.addAtTail(val)
        elif 0 < index < self.size:
            self.size += 1
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            new_node = Node(val)
            new_node.next = prev.next
            prev.next = new_node

    # ! This is the most difficult part of the algorithm
    # ! If the difficulty of this is 999, then other mehtods'
    # ! total difficulty is just 0.1
    def deleteAtIndex(self, index: int) -> None:
        if not 0 <= index < self.size:
            return
        self.size -= 1
        if index == 0:
            self.head = self.head.next

            # ! Make sure to deal with this tail case!!!!!!
            if self.size == 0:
                self.tail = None
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            prev.next = prev.next.next

            # ! Make sure to deal with this case!!!!!!
            if index == self.size:  # If deleting the tail
                self.tail = prev


# obj = MyLinkedList()
# obj.addAtHead(1)
# obj.addAtTail(3)
# obj.addAtIndex(1, 2)

# result = obj.get(1)
# print(result)

# obj.deleteAtIndex(1)

# result = obj.get(1)
# print(result)

# ! ---------------------------
obj = MyLinkedList()
obj.addAtHead(1)
obj.deleteAtIndex(0)
