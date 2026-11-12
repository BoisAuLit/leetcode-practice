# Odd Even Linked List 笔记

### 📝 2026-10-04 - retry 1

```python
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummyOdd = currOdd = ListNode()
        dummyEven = currEven = ListNode()

        curr = head
        odd = True
        while curr:
            if odd:
                currOdd.next = curr
                currOdd = currOdd.next
            else:
                currEven.next = curr
                currEven = currEven.next
            odd = not odd
            curr = curr.next
        currOdd.next = dummyEven.next
        # ! 这一行至关重要, 如果不这么做会形成死循环, 请看 asset
        currEven.next = None
        return dummyOdd.next
```
