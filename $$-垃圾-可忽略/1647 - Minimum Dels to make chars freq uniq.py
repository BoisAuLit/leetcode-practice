import heapq

class Solution:
    """
    Here, N is the length of the given string,
    and K is the maximum possible number of distinct characters in s.

    Time complexity: O(N+K²)
    Space complexity: O(K)
    """    
    def minDeletions(self, s: str) -> int:
        
        # Store the frequency of each character
        frequency = [0] * 26
        for char in s:
            frequency[ord(char) - ord('a')] += 1
        
        delete_count = 0
        # Use a set to store the frequencies we have already seen
        seen_frequencies = set()
        for i in range(26):
            # Keep decrementing the frequency until it is unique
            while frequency[i] and frequency[i] in seen_frequencies:
                frequency[i] -= 1
                delete_count += 1
                
            # Add the newly occupied frequency to the set
            seen_frequencies.add(frequency[i])
        
        return delete_count


class Solution_Brilliant:
    def minDeletions(self, s: str) -> int:
        """
        Here, N is the length of the given string,
        and K is the maximum possible number of distinct characters in s.

        Time complexity: O(N+KlogK)
        Space complexity: O(K)
        """   
        # Store the frequency of each character
        frequency = [0] * 26
        for char in s:
            frequency[ord(char) - ord('a')] += 1
        frequency.sort(reverse=True)
        
        delete_count = 0
        # Maximum frequency the current character can have
        max_freq_allowed = len(s)
        
        # Iterate over the frequencies in descending order
        for freq in frequency:
            # Delete characters to make the frequency equal the maximum frequency allowed
            if freq > max_freq_allowed:
                delete_count += freq - max_freq_allowed
                freq = max_freq_allowed

            # Update the maximum allowed frequency
            max_freq_allowed = max(0, freq - 1)
            
        return delete_count

s = Solution()
input_ = "ceabaacb"
result = s.minDeletions(input_)
print(result)

