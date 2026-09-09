
# If we have a heap like this:
"""
          1
       /     \
      3       5
     / \     / \
    7   9   8  10
"""
# Then the heap array is 
heap_array = [1, 3, 5, 7, 9, 8, 10]
"""
We can see that it's layer by layer.
It's like that we fill each layer in order,
from left to right.

1st layer: 1
2nd layer: 3 5
3rd layer: 7 9 8 10
"""
