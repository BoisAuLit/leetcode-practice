"""LC-0146 - LRU Cache

Level 1 · 06 复杂指针与链表数据结构设计 —— **Hash Map + Doubly Linked List**
题目在问：实现一个容量为 capacity 的 LRU（Least Recently Used）缓存，
         `get` 和 `put` 都要求**平均 O(1)**。

这是整个链表专题最重要的数据结构设计题。

决定性观察（为什么必须是这两个结构的组合）：
  1. 要 O(1) **按 key 找节点** ⟹ 必须有 Hash Map（`key -> node`）。
  2. 要 O(1) **维护「谁最久没用」的顺序** ⟹ 必须有一个有序结构，
     而且要能 O(1) 地把**任意一个**节点挪到最前面。
     - 数组 / 普通链表做不到：把中间元素挪走需要先找到它的前驱，那是 O(n)。
     - **双向链表可以**：节点自己就知道 `prev` 和 `next`，
       `node.prev.next = node.next; node.next.prev = node.prev` 就摘掉了，O(1)。
  3. **这就是为什么必须是「双向」而不是单向**：单向链表删除一个节点需要前驱，
     而我们从 Hash Map 直接拿到的是节点本身，拿不到它的前驱。

Head / Tail 两个哨兵（Sentinel）的作用：
      约定 `head.next` 是最近使用的，`tail.prev` 是最久未使用的。
      有了两个永不删除的哑节点，**插入和删除都不需要判空、不需要特判首尾**，
      每个操作都是固定的 4 行指针赋值。这是这份实现能写得又短又不出错的关键。

三个操作的完整逻辑：
  - `get(key)`：不在 map 里 → -1；在 → **把节点移到最前**（它刚被用过），返回 value。
  - `put(key, value)`：
      - key 已存在 → 更新 value，**移到最前**。
      - key 不存在 → 新建节点、插到最前、写进 map；
        如果超容量 → 删掉 `tail.prev`（最久未使用），**并从 map 里也删掉它的 key**。
  - **最容易漏的一步**：淘汰节点时只从链表摘掉、忘了 `del self.map[node.key]`
    ⟹ map 不断变大、内存泄漏，而且后续 get 会返回一个已经不在链表里的野节点。
    **所以链表节点里必须存 key，不能只存 value** —— 淘汰时要靠它反查 map。

为什么是平均 O(1) 而不是最坏 O(1)：
      链表操作确实是严格 O(1)，但 Hash Map 的查找在最坏情况（大量冲突）下是 O(n)。
      所以标准说法是**平均 / 摊还 O(1)**。面试里这么说会显得更严谨。

复杂度：`get` / `put` 平均 O(1)，空间 O(capacity)。

边界：
  - capacity == 1（每次 put 都淘汰上一个）
  - put 同一个 key 两次（更新而不是新增，**不能让容量计数涨**）
  - get 一个不存在的 key → -1
  - get 之后该 key 变成最近使用的，不应该被下一次淘汰
"""

# ! ============================================================================================
# ! 下面这段 ListNode + LRUCache 是**用户原有的实现**，一字未改。
# ! 后面追加的 LRUCache_1 / LRUCache_2 / LRUCache_3 是本次补充的对照实现与对拍基准。
# ! ============================================================================================

class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dic = {}
        self.head = ListNode(-1, -1)
        self.tail = ListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.dic:
            return -1

        node = self.dic[key]
        self.remove(node)
        self.add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.dic:
            old_node = self.dic[key]
            self.remove(old_node)

        node = ListNode(key, value)
        self.dic[key] = node
        self.add(node)

        if len(self.dic) > self.capacity:
            node_to_delete = self.head.next
            self.remove(node_to_delete)
            del self.dic[node_to_delete.key]

    def add(self, node):
        previous_end = self.tail.prev
        previous_end.next = node
        node.prev = previous_end
        node.next = self.tail
        self.tail.prev = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev


##################################################################################################
##### ! Solution 1: Hash Map + 双向链表 + 头尾哨兵（面试标准答案）
##### ! 时间复杂度: get / put 平均 O(1)   空间复杂度: O(capacity)
##### ! 适用：所有「O(1) 维护使用顺序」的缓存题；LFU、Browser History 都是它的变体
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class DListNode:
    """双向链表节点。**必须存 key**：淘汰尾部节点时要靠它从 map 里删掉对应条目。"""

    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev: "DListNode | None" = None
        self.next: "DListNode | None" = None


class LRUCache_1:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, DListNode] = {}
        self.head = DListNode()          # ! 哨兵：head.next 是最近使用的
        self.tail = DListNode()          # ! 哨兵：tail.prev 是最久未使用的
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DListNode) -> None:
        """从链表中摘掉 node。有哨兵，所以 prev/next 一定存在，不用判空。"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: DListNode) -> None:
        """插到 head 后面，表示「最近使用」。"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if not node:
            return -1
        self._remove(node)               # ! 用过了就移到最前
        self._add_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node:
            node.val = value             # ! 已存在：更新值并移到最前，容量不变
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev         # ! 淘汰最久未使用的
            self._remove(lru)
            del self.map[lru.key]        # ! 关键：map 里也要删，否则内存泄漏 + 野节点
        node = DListNode(key, value)
        self.map[key] = node
        self._add_front(node)


##################################################################################################
##### ! Solution 2: collections.OrderedDict（Python 专用捷径，仅作对照）
##### ! 时间复杂度: get / put 平均 O(1)   空间复杂度: O(capacity)
##### ! 适用：工程里直接用这个就行；**面试写这个基本等于没答** —— 考官要看的就是手写 DLL
##################################################################################################


from collections import OrderedDict


class LRUCache_2:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.od: "OrderedDict[int, int]" = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)         # ! OrderedDict 内部就是一个双向链表
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)  # ! 弹出最久未使用的


##################################################################################################
##### ! Solution 3: 朴素列表模拟（基准答案，用来对拍）
##### ! 时间复杂度: get / put O(n)   空间复杂度: O(capacity)
##### ! 适用：正确性参照，直接按 LRU 的定义写，不做任何优化
##################################################################################################


class LRUCache_3:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.order: list[int] = []       # ! 最近使用的在末尾
        self.data: dict[int, int] = {}

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.order.remove(key)
        elif len(self.data) == self.cap:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)


if __name__ == "__main__":
    import random

    # LeetCode 官方样例
    c = LRUCache_1(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1                 # 1 变成最近使用
    c.put(3, 3)                          # 淘汰 key 2
    assert c.get(2) == -1
    c.put(4, 4)                          # 淘汰 key 1
    assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
    print("官方样例通过 ✓")

    # capacity == 1
    c = LRUCache_1(1)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == -1 and c.get(2) == 2
    print("capacity=1 通过 ✓")

    # 同一个 key put 两次不应该占两个容量
    c = LRUCache_1(2)
    c.put(1, 1); c.put(1, 10); c.put(2, 2)
    assert c.get(1) == 10 and c.get(2) == 2
    print("重复 put 同一 key 通过 ✓")

    for _ in range(300):                 # ! 随机操作序列三方对拍
        cap = random.randint(1, 4)
        a, b, d = LRUCache_1(cap), LRUCache_2(cap), LRUCache_3(cap)
        for _ in range(80):
            if random.random() < 0.5:
                k, v = random.randint(0, 5), random.randint(0, 99)
                a.put(k, v); b.put(k, v); d.put(k, v)
            else:
                k = random.randint(0, 5)
                ra, rb, rd = a.get(k), b.get(k), d.get(k)
                assert ra == rb == rd, (cap, k, ra, rb, rd)
        assert len(a.map) <= cap         # ! map 没有泄漏（淘汰时确实 del 了）
    print("随机对拍 300 组 × 80 次操作通过 ✓（含 map 无泄漏检查）")
