from collections import Counter

"""
2^29 = 536870912   (9 digits)
2^30 = 1073741824  (10 digits, too big)
"""
class Solution(object):
    def reorderedPowerOf2(self, N):
        count = Counter(str(N))
        """
        1 << 0 --> 2^0
        1 << 5 --> 2^5
        """
        return any(count == Counter(str(1 << b)) for b in range(30))
