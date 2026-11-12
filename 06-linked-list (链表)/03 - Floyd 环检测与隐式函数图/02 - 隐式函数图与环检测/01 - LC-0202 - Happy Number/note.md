# Happy Number 笔记（2026-09-10）

信号→模式："一个值由固定规则生成下一个值，反复迭代，问是否终止/循环 → 这是隐式链表，判环用快慢指针（Floyd），或用 set 记录已见"。

NeetCode 上叫 Non-Cyclical Number，LeetCode 上叫 Happy Number (202)，同一题。

## Floyd 写法要点

- `slow = n`，`fast = get_sum(n)`，一开始就错开一步，否则 `while slow != fast` 直接不进循环。
- 每轮 fast 走两步、slow 走一步，相遇即停。
- 相遇后看 `fast == 1`：链尾停在 1（1 → 1 自环）就是 happy，否则掉进别的环。

### 📝 2026-09-14 - retry 1

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def get_sum(n: int) -> int:
            res = 0
            while n:
                n, rem = divmod(n, 10)
                res += rem * rem
            return res
        # 这里千万不能写 slow = fast = n, 因为如果这样写, 下面的 while 循环根本就不开始!
        slow, fast = n, get_sum(n)
        while slow != fast:
            slow = get_sum(slow)
            fast = get_sum(get_sum(fast))

        # 这里无论写 fast == 1 还是 slow == 1 都等价
        # 因为经过上面的 while 循环之后, slow 必然等于 fast
        return fast == 1
```

### 📝 2026-10-03 - retry 2

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def get_sum(k: int) -> int:
            res = 0
            while k:
                k, rem = divmod(k, 10)
                res += rem * rem
            return res

        slow = n
        fast = get_sum(n)
        while slow != fast:
            slow = get_sum(slow)
            fast = get_sum(get_sum(fast))
        # ! 别忘了检测 slow == 1
        return slow == fast and slow == 1
```
