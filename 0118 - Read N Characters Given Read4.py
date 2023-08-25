from typing import List


def read4():
    return None


"""
The read4 API is already defined for you.

    @param buf4, a list of characters
    @return an integer
    def read4(buf4):

# Below is an example of how the read4 API can be called.
file = File("abcdefghijk") # File is "abcdefghijk", initially file pointer (fp) points to 'a'
buf4 = [' '] * 4 # Create buffer with enough space to store characters
read4(buf4) # read4 returns 4. Now buf = ['a','b','c','d'], fp points to 'e'
read4(buf4) # read4 returns 4. Now buf = ['e','f','g','h'], fp points to 'i'
read4(buf4) # read4 returns 3. Now buf = ['i','j','k',...], fp points to end of file
"""


# Solution 1 --> No intermidiary buffer
class Solution:
    def read(self, buf: List[str], n: int) -> int:
        copied_chars = 0
        read_chars = 4
        remaining_chars = n
        while remaining_chars >= 4 and read_chars == 4:
            read_chars = read4(buf[copied_chars:])
            copied_chars += read_chars
            remaining_chars -= read_chars
        if remaining_chars and read_chars:
            buf4 = [""] * 4
            read_chars = read4(buf4)
            for i in range(0, min(remaining_chars, read_chars)):
                buf[copied_chars] = buf4[i]
                copied_chars += 1
        return min(n, copied_chars)


# Solutioon 2 --> Internal buffer of 4 charcters
# class Solution:
#     def read(self, buf: List[str], n: int) -> int:
#         copied_chars = 0
#         read_chars = 4
#         buf4 = [''] * 4

#         while copied_chars < n and read_chars == 4:
#             read_chars = read4(buf4)

#             for i in range(read_chars):
#                 if copied_chars == n:
#                     return copied_chars
#                 buf[copied_chars] = buf4[i]
#                 copied_chars += 1

#         return copied_chars
