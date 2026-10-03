# Constrained subseq sum

max subset sum such that index difference of consec elements in the subseq <= k

## Solution

Simple problem, if you know to use mono dq to keep max in a window.

```python
class Solution:
    def constrainedSubsetSum(self, nums: list[int], k: int) -> int:
        dq = deque()
        dp = [0] * len(nums)

        for i, x in enumerate(nums):
            # Remove indices outside [i-k, i-1]
            while dq and dq[0] < i - k:
                dq.popleft()

            dp[i] = x
            if dq and dp[dq[0]] > 0:
                dp[i] += dp[dq[0]]

            # Keep dp values decreasing in deque
            while dq and dp[dq[-1]] < dp[i]:
                dq.pop()

            dq.append(i)

        return max(dp)
```
