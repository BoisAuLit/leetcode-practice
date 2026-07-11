from collections import Counter


class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts = [0] * 128
        for c in s:
            counts[ord(c)] += 1
        has_odd = any(x % 2 == 1 for x in counts)
        return sum(x - (x % 2) for x in counts) + (+has_odd)


# class Solution:
#     def longestPalindrome(self, s: str) -> int:
#         counts = Counter(s).values()
#         has_odd = any(x % 2 == 1 for x in counts)
#         return sum(x - (x % 2) for x in counts) + (+has_odd)


s = Solution()

# Expecting 983
input_ = "civilwartestingwhetherthatnaptionoranynartionsoconceivedandsodedicatedcanlongendureWeareqmetonagreatbattlefiemldoftzhatwarWehavecometodedicpateaportionofthatfieldasafinalrestingplaceforthosewhoheregavetheirlivesthatthatnationmightliveItisaltogetherfangandproperthatweshoulddothisButinalargersensewecannotdedicatewecannotconsecratewecannothallowthisgroundThebravelmenlivinganddeadwhostruggledherehaveconsecrateditfaraboveourpoorponwertoaddordetractTgheworldadswfilllittlenotlenorlongrememberwhatwesayherebutitcanneverforgetwhattheydidhereItisforusthelivingrathertobededicatedheretotheulnfinishedworkwhichtheywhofoughtherehavethusfarsonoblyadvancedItisratherforustobeherededicatedtothegreattdafskremainingbeforeusthatfromthesehonoreddeadwetakeincreaseddevotiontothatcauseforwhichtheygavethelastpfullmeasureofdevotionthatweherehighlyresolvethatthesedeadshallnothavediedinvainthatthisnationunsderGodshallhaveanewbirthoffreedomandthatgovernmentofthepeoplebythepeopleforthepeopleshallnotperishfromtheearth"
result = s.longestPalindrome(input_)
print(result)

"""

"""
