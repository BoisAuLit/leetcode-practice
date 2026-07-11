from typing import List, Optional
from ListNode import ListNode

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def spiralMatrix(
        self, m: int, n: int, head: Optional[ListNode]
    ) -> List[List[int]]:
        matrix = [[-1] * n for _ in range(m)]
        direction = 1  # Starting off going right
        i, j = 0, -1
        while head:
            k = 0
            while k < n and head:
                j += direction
                matrix[i][j] = head.val
                head = head.next
                k += 1
            m -= 1
            k = 0
            while k < m and head:
                i += direction
                matrix[i][j] = head.val
                head = head.next
                k += 1
            n -= 1
            direction *= -1
        return matrix


s = Solution()

# Expecting [[3, 0, 2, 6, 8], [5, 0, -1, -1, 1], [5, 2, 4, 9, 7]]
m = 3
n = 5
head = ListNode.from_list([3, 0, 2, 6, 8, 1, 7, 9, 4, 2, 5, 5, 0])

result = s.spiralMatrix(m, n, head)
print(result)

"""

"""
