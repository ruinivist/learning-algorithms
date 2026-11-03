# Inversion count

leetcode: https://leetcode.com/problems/count-of-smaller-numbers-after-self/

## Solution

You can always use ft but in general you would want the dnc solution

This build ENTIRELY over the merge sort solution as you NEED to have sorted ranges
to be able to count inversions fast.

Start with the trivial merge sort

```python
class Solution:
    def countSmaller(self, nums: list[int]) -> list[int]:
        inv = [0] * len(nums)
        nums = [(v, i) for i, v in enumerate(nums)]

        def inplace_merge(a, b, c):
            # a...b...c
            # where [a...b) and [b....c) are sorted
            res = []
            i1, i2 = a, b
            while i1 < b and i2 < c:
                if nums[i1][0] <= nums[i2][0]:
                    # WHAT CHANGES FOR INVERSION COUNTING IS HERE
                    # notice all elements already consumed from right
                    # are smaller than the current element in left
                    inv[nums[i1][1]] += i2 - b

                    res.append(nums[i1])
                    i1 += 1
                else:
                    res.append(nums[i2])
                    i2 += 1

            # THIS AS WELL, remaining elements in left are greater than
            # all elements already consumed from right
            while i1 < b:
                inv[nums[i1][1]] += i2 - b
                res.append(nums[i1])
                i1 += 1

            res += nums[i2:c]
            nums[a:c] = res

        def m_sort(st, en):
            if en - st <= 1:
                # single item
                return
            mid = (st + en) // 2
            m_sort(st, mid)
            m_sort(mid, en)

            inplace_merge(st, mid, en)

        m_sort(0, len(nums))
        return inv
```
