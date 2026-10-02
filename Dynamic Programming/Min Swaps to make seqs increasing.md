---
leetcode_url: https://leetcode.com/problems/minimum-swaps-to-make-sequences-increasing/
---

# Min swaps to make seqs increasing.

Two sequences a and b, you can do swap(a(i), b(i)) and this counts as 1 move.
Min number of moves ( the problem assures possible but it's easy to detect otherwise ) to
make both a and b individuall increasing.

## Solution

I was having trouble outlining the state even when I guessed that you probably only need the
state of the last position. I was half asleep and was focused on making f(pos, window related)
but wasn't able to figure out the state then.

It's simply `f(pos, prevSwapped)`, note that whether we swap current or not is what we decide
GIVEN this state.

```python
class Solution:
    def minSwap(self, nums1: list[int], nums2: list[int]) -> int:
        n = len(nums1)

        @cache
        def f(i, pswap):
            if i == n:
                return 0

            ans = math.inf
            curr = (nums1[i], nums2[i])
            prev = (nums1[i - 1], nums2[i - 1])
            if pswap:
                prev = prev[::-1]

            valid = lambda cur: all(a > b for a, b in zip(cur, prev))

            if valid(curr):
                ans = min(ans, f(i + 1, False))

            if valid(curr[::-1]):
                ans = min(ans, 1 + f(i + 1, True))

            return ans

        return min(1 + f(1, True), f(1, False))
```
