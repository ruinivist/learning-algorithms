---
leetcode_url: https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/
---

# Maximum sum of three subarrays

Partition into three non overlapping, subarrays of lenth k such that the total sum across is the
3 is max possible.

## Solution

The lengths are fixed so I feel like I can have a prefix sum and then just do a state machine
like transition where for i I pick best from i - k and back.

Let's assume it was just two subarrays, then this is just
max over f(i) + max over f(0...i-k)
if f(i) = we use i as one of the partition starts

if you encode that count as state then this is very similar to buy and sell stock problem.

```python
from functools import cache
import math

class Solution:
    def maxSumOfThreeSubarrays(self, nums: list[int], k: int) -> list[int]:
        n = len(nums)

        pref = nums.copy()
        for i in range(1, n):
            pref[i] += pref[i - 1]

        def rsum(l, r):
            return pref[r] - (pref[l - 1] if l > 0 else 0)

        # path is just len 3 here so just store in full
        @cache
        def f(i, parts):
            if parts == 3:
                return 0, ()

            # Not enough space left to finish
            remaining_parts = 3 - parts
            if n - i < remaining_parts * k:
                return -math.inf, ()

            best_sum = -math.inf
            best_path = ()

            # choose starting index j for this partition
            for j in range(i, n - k + 1):
                next_sum, next_path = f(j + k, parts + 1)

                if next_sum == -math.inf:
                    continue

                total = rsum(j, j + k - 1) + next_sum
                path = (j,) + next_path

                if total > best_sum:
                    best_sum = total
                    best_path = path
                elif total == best_sum and path < best_path:
                    best_path = path

            return best_sum, best_path

        return list(f(0, 0)[1])
```

Now this is generalised but O(n^2), obviously TLEs. The solution that works is made specially
for the 3 case and how for 3, you can iterate over middle and optim over prefix and suffix.

> note that once again, you can only do it for the 3 case, atleast cleanly.

```python
class Solution:
    def maxSumOfThreeSubarrays(self, nums: list[int], k: int) -> list[int]:
        n = len(nums)
        pref = nums.copy()
        for i in range(1, n):
            pref[i] += pref[i - 1]

        def rsum(l, r):
            return pref[r] - (pref[l - 1] if l > 0 else 0)

        # p(i) max sum for a start in 0...i (sum, what start)
        # s(i) max sum for a start in i...n-1 (sum, what start)
        # then you can just iterate

        p, s = [-math.inf] * n, [-math.inf] * n
        for i in range(0, n - k + 1):
            p[i] = (rsum(i, i + k - 1), -i)
            if i > 0:
                p[i] = max(p[i], p[i - 1])

        for i in range(n - k, -1, -1):
            s[i] = (rsum(i, i + k - 1), -i)
            if i < n - k:
                s[i] = max(s[i], s[i + 1])

        max_sum = -math.inf
        ans = (n, 0, 0)
        for st in range(k, n - 2 * k + 1):
            cur_sum = rsum(st, st + k - 1) + p[st - k][0] + s[st + k][0]
            tans = (-p[st - k][1], st, -s[st + k][1])
            if cur_sum > max_sum:
                max_sum = cur_sum
                ans = tans
            elif cur_sum == max_sum:
                ans = min(ans, tans)

        return ans
```

The implementation with all the different indexes to keep track of and get right made this a bit
tricky.
