from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        # Dictionary which keeps a count of all the unique characters in t.
        letter_count_t = Counter(t)

        # Number of unique characters in t, which need to be present in the desired window.
        required = len(letter_count_t)

        """
        formed is used to keep track of how many 
        unique characters in t are present in
        the current window in its desired frequency.

        e.g.
        if t is "AABC",
        then the window must have two A's, one B and one C.
        Thus formed would be = 3 when all these conditions are met.
        """
        formed = 0

        # Count all letters in current window
        window_counts = {}
        window_size = float("inf")
        left = None
        right = None

        # left and right pointer
        l, r = 0, 0
        while r < len(s):
            # Add one character from the right to the window
            character = s[r]
            window_counts[character] = window_counts.get(character, 0) + 1

            """
            If the frequency of the current character added equals
            to the desired count in t then increment the formed count by 1.
            """
            if (
                character in letter_count_t
                and window_counts[character] == letter_count_t[character]
            ):
                formed += 1

            """
            Try and contract the window from the left
            till the point where it stops being 'desirable'.
            """
            while l <= r and formed == required:
                character = s[l]

                # Save the smallest window until now.
                if r - l + 1 < window_size:
                    window_size = r - l + 1
                    left = l
                    right = r

                # The character at the position pointed by the `left` pointer is no longer a part of the window.
                window_counts[character] -= 1
                if (
                    character in letter_count_t
                    and window_counts[character] < letter_count_t[character]
                ):
                    formed -= 1

                # Move the left pointer ahead, this would help to look for a new window.
                l += 1

            # Keep expanding the window on the right side once we are done contracting.
            r += 1
        return "" if window_size == float("inf") else s[left : right + 1]


# Test case 1: Expecting "BANC"
solution = Solution()
s = "ADOBECODEBANC"
t = "ABC"
result = solution.minWindow(s, t)
print()
print(result)

# ! This test case is very important
# # Test case 2: Expecting "a"
# solution = Solution()
# s = "a"
# t = "a"
# result = solution.minWindow(s, t)
# print()
# print(result)


# # Test case 3: Expecting "a"
# solution = Solution()
# s = "ab"
# t = "a"
# result = solution.minWindow(s, t)
# print()
# print(result)
