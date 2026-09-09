class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # map key to node

        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    # * Remove any node within the Doubly Linked List
    def remove(self, node):
        # ! First, get the previous and next nodes
        prev = node.prev
        next_ = node.next
        # ! Then connnect the previous and next nodes
        prev.next = next_
        next_.prev = prev

    # * Insert the node to the end of the Doubly Linked List
    def insert(self, node):
        # ! First, get the previous and next nodes
        prev = self.right.prev
        next_ = self.right
        # ! Then, create links between prev, curr, next nodes
        prev.next = node
        next_.prev = node

        node.next = next_
        node.prev = prev

    def get(self, key: int) -> int:
        # ! When we get a node by key, we always deem it as most recently used
        if key in self.cache:
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key: int, value: int) -> None:
        # ! When we insert a key/value pair, we always deem it as most recently used
        if key in self.cache:
            self.remove(self.cache[key])
        # * Here we update the cache
        self.cache[key] = Node(key, value)
        self.insert(self.cache[key])

        # ! Only after inserting a node will it be possible to overflow
        if len(self.cache) > self.cap:
            lru = self.left.next
            self.remove(lru)
            # ! Don't forget about this deletion
            # * Here we update the cache
            del self.cache[lru.key]
