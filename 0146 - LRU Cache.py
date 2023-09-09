import collections

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dic = collections.OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.dic:
            return -1
        
        self.dic.move_to_end(key)
        return self.dic[key]
        
    def put(self, key: int, value: int) -> None:
        if key in self.dic:
            self.dic.move_to_end(key)
        
        self.dic[key] = value
        if len(self.dic) > self.capacity:
            self.dic.popitem(False)

#########################################################################
#########################################################################

class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dict = {}
        self.head = ListNode(-1, -1)
        self.tail = ListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.dict:
            return -1

        node = self.dict[key]
        self.remove(node)
        self.add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.dict:
            old_node = self.dict[key]
            self.remove(old_node)

        node = ListNode(key, value)
        self.dict[key] = node
        self.add(node)

        if len(self.dict) > self.capacity:
            node_to_delete = self.head.next
            self.remove(node_to_delete)
            del self.dict[node_to_delete.key]

    def add(self, node):
        previous_end = self.tail.prev
        previous_end.next = node
        node.prev = previous_end
        node.next = self.tail
        self.tail.prev = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev




# Testing scenarios 2
cache = LRUCache(2)
cache.put(2, 1)
print(cache.dict.items())  # Expecting [(2, 1)]

cache.put(1, 1)
print(cache.dict.items())  # Expecting [(2, 1), (1, 1)]

cache.put(2, 3)
print(cache.dict.items())  # Expecting [(1, 1), (2, 3)]

cache.put(4, 1)
print(cache.dict.items())  # Expecting [(2, 3), (4, 1)]

print(cache.get(1))  # Expecting -1
print(cache.get(2))  # Expecting 3


# Testing scenarios 1
# cache = LRUCache(2)
# cache.put(1, 1)
# print(cache.dict)  # Expecting {1=1}
# cache.put(2, 2)
# print(cache.dict)  # Expecting {1=1, 2=2}
# print(cache.get(1))  # Expecting 1
# cache.put(3, 3)
# print(cache.dict)  # Expecting {1=1, 3=3}
# print(cache.get(2))  # Expecting 2
# cache.put(4, 4)
# print(cache.dict)  # Expecting {4=4, 3=3}
# print(cache.get(1))  # Expecting -1
# print(cache.get(3))  # Expecting 3
# print(cache.get(4))  # Expecting 4

"""

"""
