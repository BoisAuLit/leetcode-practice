"""LC-0445 - Add Two Numbers II（第二轮自主新增）

Level 1 · 01 基础指针、Dummy Node 与反转 —— 数字**高位在前**时怎么处理进位
题目在问：和 LC-0002 一样是两个链表相加，但**最高位在链表头部**（7->2->4->3 表示 7243），
         并且题目明确要求：**不允许修改输入链表**（即不能直接反转它们）。

为什么新增它（它补的是哪个缺口）：
  LC-0002 的数字是**低位在前**，所以从头往后扫就是从个位开始加，进位自然向后传 —— 很顺。
  LC-0445 把顺序反过来，**进位的方向和遍历的方向相反**了。
  这就逼出一个通用技巧：**需要逆序访问但又不能反转时，用栈**。
  这个「链表 + 栈」的组合在面试里非常常见，而 LC-0002 完全覆盖不到。

决定性观察：
  1. 加法必须从**最低位**开始（进位只能从低位向高位传）。
  2. 链表只能从头往后走，而头是最高位 ⟹ 需要**逆序**访问 ⟹ 用两个栈装下所有值。
  3. 结果也要「最高位在前」，而我们是从低位开始算出来的 ⟹
     **每算出一位就头插（插到结果链表的最前面）**，天然得到正确顺序，不需要最后再反转。

```
head = None
while 还有位 or carry:
    total = ...
    node = ListNode(total % 10)
    node.next = head        # 头插：新算出的是更高位，放最前面
    head = node
    carry = total // 10
```

三种解法的取舍：
  - **Solution_1（栈）**：O(m+n) 时间、O(m+n) 空间，**不修改输入**，面试首选。
  - **Solution_2（反转输入）**：O(1) 额外空间，但**破坏了输入链表**
    （可以算完再反转回去，但那就不是 O(1) 操作数了，而且在并发/只读场景下不可接受）。
  - **Solution_3（转整数）**：Python 能过，但在 C++/Java 里会溢出 —— 面试不能这么答。

和 LC-0002 的对照（放在同一个 Level 2 就是为了这张表）：

| | LC-0002 | LC-0445 |
|---|---|---|
| 数字顺序 | 低位在前 | **高位在前** |
| 遍历方向 vs 进位方向 | 一致 | **相反** |
| 核心技巧 | 边走边加 | **栈**（或反转） |
| 结果构造 | 尾插 | **头插** |

复杂度：O(m + n) 时间，O(m + n) 空间（栈）。

边界：
  - [7,2,4,3] + [5,6,4] = [7,8,0,7]
  - [2,4,3] + [5,6,4] = [8,0,7]
  - [9,9,9] + [1] = [1,0,0,0]（最高位进位，结果变长）
  - [0] + [0] = [0]
  - 两个链表长度相差很大
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @staticmethod
    def from_list(values: List[int]) -> Optional["ListNode"]:
        dummy = ListNode()
        cur = dummy
        for v in values:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    @staticmethod
    def to_list(head: Optional["ListNode"]) -> List[int]:
        out = []
        while head:
            out.append(head.val)
            head = head.next
        return out


##################################################################################################
##### ! Solution 1: 两个栈逆序取数 + 头插构造结果（不修改输入链表）
##### ! 时间复杂度: O(m + n)   空间复杂度: O(m + n)
##### ! 适用：需要逆序访问单链表、但又不允许反转它时的通用套路
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        s1, s2 = [], []
        while l1:
            s1.append(l1.val); l1 = l1.next
        while l2:
            s2.append(l2.val); l2 = l2.next
        head, carry = None, 0
        while s1 or s2 or carry:                   # ! carry 也要进循环条件，否则漏最高位进位
            total = carry
            if s1: total += s1.pop()               # ! pop 出来的是最低位
            if s2: total += s2.pop()
            node = ListNode(total % 10)
            node.next = head                       # ! 头插：新算出的位更高，放最前
            head = node
            carry = total // 10
        return head


##################################################################################################
##### ! Solution 2: 反转两个输入链表 → 复用 LC-0002 的逻辑 → 反转结果
##### ! 时间复杂度: O(m + n)   空间复杂度: O(1) 额外
##### ! 适用：被追问「能不能 O(1) 空间」时；但它**修改了输入链表**，要主动说明这个代价
##################################################################################################


class Solution_2:
    @staticmethod
    def _reverse(head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        while head:
            nxt = head.next
            head.next = prev
            prev, head = head, nxt
        return prev

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        a, b = self._reverse(l1), self._reverse(l2)   # ! 注意：这一步破坏了调用者的链表
        head, carry = None, 0
        while a or b or carry:
            total = carry
            if a: total += a.val; a = a.next
            if b: total += b.val; b = b.next
            node = ListNode(total % 10)
            node.next = head
            head = node
            carry = total // 10
        return head


##################################################################################################
##### ! Solution 3: 转成整数相加再拆回链表（基准答案，用来对拍）
##### ! 时间复杂度: O(m + n)   空间复杂度: O(m + n)
##### ! 适用：正确性参照。**面试不能这么答** —— C++/Java 会整数溢出，Python 只是碰巧能过
##################################################################################################


class Solution_3:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def to_int(h):
            n = 0
            while h:
                n = n * 10 + h.val
                h = h.next
            return n
        return ListNode.from_list([int(c) for c in str(to_int(l1) + to_int(l2))])


if __name__ == "__main__":
    import random

    cases = [([7, 2, 4, 3], [5, 6, 4]), ([2, 4, 3], [5, 6, 4]), ([9, 9, 9], [1]),
             ([0], [0]), ([1], [9, 9, 9, 9])]
    for x, y in cases:
        a = ListNode.to_list(Solution_1().addTwoNumbers(ListNode.from_list(x), ListNode.from_list(y)))
        b = ListNode.to_list(Solution_2().addTwoNumbers(ListNode.from_list(x), ListNode.from_list(y)))
        c = ListNode.to_list(Solution_3().addTwoNumbers(ListNode.from_list(x), ListNode.from_list(y)))
        assert a == b == c, (x, y, a, b, c)
        print(f"{x} + {y} -> {a}")

    # ! 验证 Solution_1 确实没有修改输入（这是它相对 Solution_2 的关键优势）
    l1 = ListNode.from_list([7, 2, 4, 3])
    l2 = ListNode.from_list([5, 6, 4])
    Solution_1().addTwoNumbers(l1, l2)
    assert ListNode.to_list(l1) == [7, 2, 4, 3] and ListNode.to_list(l2) == [5, 6, 4]
    print("输入未被修改检查通过 ✓（Solution_1 不破坏入参，Solution_2 会）")

    def rand_num():
        # ! 题目保证「除了数字 0 本身，不会有前导零」，随机输入必须遵守同样的约束，
        # ! 否则 Solution_3 转成整数时会丢掉前导零，和链表解法对不上（那是测试的锅，不是解法的锅）
        n = random.randint(1, 6)
        if n == 1:
            return [random.randint(0, 9)]
        return [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(n - 1)]

    for _ in range(1000):
        x = rand_num()
        y = rand_num()
        a = ListNode.to_list(Solution_1().addTwoNumbers(ListNode.from_list(x), ListNode.from_list(y)))
        c = ListNode.to_list(Solution_3().addTwoNumbers(ListNode.from_list(x), ListNode.from_list(y)))
        assert a == c, (x, y, a, c)
    print("随机对拍 1000 组通过 ✓")
