def isBadVersion(version: int) -> bool:
    return version >= 352


class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n
        while left <= right:
            mid = (left + right) // 2

            if isBadVersion(mid):
                if not isBadVersion(mid - 1):
                    return mid
                else:
                    right = mid - 1
            else:
                left = mid + 1


versions = range(1, 11)
s = Solution()
result = s.firstBadVersion(687)
print(result)
