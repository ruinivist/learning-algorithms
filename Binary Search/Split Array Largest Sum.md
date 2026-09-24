# Split Array Largest Sum

split into k subarrays such that the max sum across subarrays is minimum

## Solution

maximise the minimums, really hints at a possible binary search so we try that first
and it seems it fits quite well, as I can very very easily answer this
"can I split into subarrays such that all sums are <= mid and we get k segments"
Notice that all the numbers are non-negative and that's needed for monotonicity the answer to
the problem above
For example for this case, length 2 can be valid while 1 will not [100, -100].

```python
class Solution:
    def splitArray(self, nums: list[int], k: int) -> int:
        n = len(nums)
        l, r = 0, sum(nums)

        def can(s):
            ok = True
            splits = 1  # note
            run = 0
            for x in nums:
                if x > s:
                    return False
                if run + x > s:
                    # that early check would handle if even
                    # this is past limits
                    run = x
                    splits += 1
                else:
                    run += x
            # we cannot do a split == k
            # as that breaks the monotonicty of the problem,
            # my loop above will take all elems for a very
            # large s
            # for splits being underutilised, we can always
            # break them to get to k
            return splits <= k

        # not possible
        ans = -1
        while l <= r:
            m = (l + r) // 2
            # can I split into k segments, such that s
            if can(m):
                r = m - 1
                ans = m
            else:
                l = m + 1

        return ans
```
