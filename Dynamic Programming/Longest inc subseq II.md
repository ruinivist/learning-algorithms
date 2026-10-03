# Longest Increasing Subsequence II

LIS where diff of adjacent elems is at most k, and still need this in O(nlogn)

## Solution

For a usual LIS you minimise tails but here we can't do that, a tail too short would make us
not be able to continue.

f(i) = lis length s.t you end at i and take i
= max over j < i s.t. val(j) close to val(i)
Note that val(j) is a continuous range, so if for each val in prefix, we can do range max
then we have our solution.

The hard part is just the whole of segment tree impl needed to do the range maxes.

```python
class Solution:
    def lengthOfLIS(self, nums, k):
        # note that n is range based
        n = max(nums) + 1
        seg = [0] * (4 * n)

        def query(i, l, r, ql, qr):
            if qr < l or r < ql:
                return 0
            if ql <= l and r <= qr:
                return seg[i]

            m = (l + r) // 2
            return max(
                query(i * 2, l, m, ql, qr),
                query(i * 2 + 1, m + 1, r, ql, qr)
            )

        def update(i, l, r, pos, val):
            if l == r:
                seg[i] = max(seg[i], val)
                return

            m = (l + r) // 2
            if pos <= m:
                update(i * 2, l, m, pos, val)
            else:
                update(i * 2 + 1, m + 1, r, pos, val)

            seg[i] = max(seg[i * 2], seg[i * 2 + 1])

        ans = 0

        for x in nums:
            cur = 1 + query(1, 0, n - 1, max(0, x - k), x - 1)
            update(1, 0, n - 1, x, cur)
            ans = max(ans, cur)

        return ans
```
