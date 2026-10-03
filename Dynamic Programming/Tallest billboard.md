# Tallest billboard

Given a multiset of numbers. Find the max k such that you can carve out two disjoint multisets
of sum k.

## Solution

The size of set is small, the sum across the set is too.

I don't think an approach of finding ONE set will work ( so something like mitm )
since the partition is not coverting, some are bound to get left.

I can instead do something like a subset sum where I count subsets.
Since sum is max 5k, I only need to check till half of that.
O(nS) would be fine.

This above is incorrect, I missed that this way I'll not be making disjoint subsets.

That 20 elem size seems more useful now, let me try something with subset masking.
For each mask, let it's sum be s, can I make s from mask complement?
This last part I believe I can just pre-compute? f(mask, sum), but if you could then you
could count as well.

---

The actual approach was quite different than what I was doing.
Instead of tracking counts, track imbalance = abs(diff)

Also, no need of masks, that count of 20 threw me way off.

f(i, diff) => I'm at i and have made difference as diff so far. What is the max total length
of rods so I end up with diff = 0.

Then for ith, you have 3 choices, unused, increase diff or decrease diff.
Note that the diff is always positive, define as abs(left-right). If you add to left, the abs
increases by that. If you add to right, the gap is still "correct" even though this is not
true
$abs(left-(right+x)) = abs(abs(left-right)-x)$
Why? left and right might get swapped on LHS to make it work.
Think of this op on the number line and the diff change will be clearer.

```python
class Solution:
    def tallestBillboard(self, a: list[int]) -> int:
        n = len(a)

        @cache
        def f(i, diff):
            if i == n:
                return 0 if diff == 0 else -math.inf

            return max(
                f(i + 1, diff),
                a[i] + f(i + 1, a[i] + diff),
                a[i] + f(i + 1, abs(diff - a[i])),
            )

        return f(0, 0) // 2
```
