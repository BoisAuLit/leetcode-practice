"""LC-0148 - Sort List

快慢指针的用途：把链表从中点劈成两半，喂给归并排序
题目在问：O(n log n) 时间排好一条链表（follow-up 还要求 O(1) 额外空间）

为什么链表只能归并排序：快排要随机访问选 pivot，链表做不到；而归并只需要"劈一半"和"合并两条有序链"，
这两件事链表都很擅长（合并甚至比数组更好 —— 不需要额外数组，只改指针）。

劈一半的坑（和 0876 不同！）：
    slow, fast = head, head.next     ← fast 先走一步，slow 停在**第一个**中点
    slow, fast = head, head          ← slow 停在第二个中点，两段长度是 (n/2, n/2)，
                                        但 n == 2 时左半会是空的 → 无限递归爆栈
记法：要劈开就让 fast 先走一步，保证左半至少 1 个节点、右半至少 1 个节点。
劈完一定要 slow.next = None 真的断开，不然两半还连着，递归永远不收敛。
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 快慢指针劈半 + 自顶向下归并
##### ! 时间复杂度: O(n log n)   空间复杂度: O(log n)   递归栈深度 log n
##### ! 适用: 面试标准答案，代码最短最好记；本文件夹要练的就是这个劈半动作
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def sortList(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:  # ! 0 个或 1 个节点天然有序，也是递归的出口
            return head

        # ! fast 先走一步：slow 停在第一个中点，保证劈出来的两半都非空（n == 2 时左 1 右 1）
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        mid, slow.next = slow.next, None  # ! 必须真的断开，否则递归不收敛

        return self.merge(self.sortList(head), self.sortList(mid))

    def merge(self, a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()

        while a and b:
            if a.val <= b.val:  # ! <= 而不是 < ：保证稳定排序
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next

        tail.next = a or b  # ! 哪条还剩就整段接上，不用逐个搬

        return dummy.next


##################################################################################################
##### ! Solution 2: 自底向上归并（step = 1, 2, 4, 8…）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1)   ★ 空间上严格优于 Solution 1，没有递归栈
##### ! 适用: 面试官追问"能不能做到 O(1) 空间"时的答案；代价是代码长一倍、指针操作更容易写错
##### ! 注意: 这个解法用不到快慢指针（长度是数出来的），放在这里是为了把 follow-up 补全
##################################################################################################


class Solution_2:
    def sortList(self, head: ListNode | None) -> ListNode | None:
        n, cur = 0, head
        while cur:
            n += 1
            cur = cur.next

        dummy = ListNode(0, head)
        step = 1

        while step < n:
            prev, cur = dummy, dummy.next
            while cur:
                left = cur
                right = self.cut(left, step)        # ! 切下长度 step 的左块，返回剩下的头
                cur = self.cut(right, step)         # ! 再切下右块，返回下一轮的起点
                prev.next = self.merge(left, right)
                while prev.next:                    # ! prev 推到合并后这一块的尾巴
                    prev = prev.next
            step *= 2

        return dummy.next

    def cut(self, head: ListNode | None, n: int) -> ListNode | None:
        """从 head 往后数 n 个节点后断开，返回后半段的头（不足 n 个就返回 None）。"""
        while n > 1 and head:
            head = head.next
            n -= 1
        if not head:
            return None
        rest, head.next = head.next, None
        return rest

    def merge(self, a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next


##################################################################################################
##### ! Solution 3: 取出所有值排序，再写回节点
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)   一个长度 n 的数组
##### ! 适用: 面试里属于"耍赖"，但如果只问结果不问过程，这是最不容易写错的
##### ! 为什么不推荐: 空间退化成 O(n)，而且完全绕过了链表排序这道题想考的东西
##################################################################################################


class Solution_3:
    def sortList(self, head: ListNode | None) -> ListNode | None:
        vals, cur = [], head
        while cur:
            vals.append(cur.val)
            cur = cur.next

        vals.sort()

        cur = head
        for v in vals:  # ! 只改 val 不动指针，所以原来的节点顺序结构被复用
            cur.val = v
            cur = cur.next

        return head


def build(vals: list[int]) -> ListNode | None:
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    import random

    cases = [[4, 2, 1, 3], [-1, 5, 3, 4, 0], [], [1], [2, 1], [3, 3, 3], [5, 4, 3, 2, 1]]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        ok = all(to_list(sol.sortList(build(c))) == sorted(c) for c in cases)

        rng = random.Random(0)  # ! 随机对拍：和 sorted() 比
        for _ in range(2000):
            c = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
            if to_list(sol.sortList(build(c))) != sorted(c):
                ok = False
                print(f"   Solution_{i} 不一致: {c}")
                break

        print(f"Solution_{i}: {'✅ 固定用例 + 2000 组随机对拍全过' if ok else '❌'}")
