# Valid permutations of DI sequence

D = a(i) > a(i+1) and I = a(i) < a(i+1)
You are given a DI sequence, count number of permutations of length n+1 that match the DI ordering.

## Solution

TYhis is a good one for I've seen this idea before. Idea is that you start with ranks, at the end
you have a full rank ordering which is the same as a permutation.

Then at each moment when you hit a D or I, you only need to decide the rank partitioning based on
the LAST rank, say this is q. Then if you wanna append say x, all ranks >= x currenly will need
to shift up by one, in code that's handled implicity since it's a "constant" transform so number
of ways don't change.

```python
class Solution:
    def numPermsDISequence(self, s: str) -> int:
        mod = int(1e9 + 7)
        n = len(s)

        # number of permutations of ranks 0...i+1
        # satisfying s[0...i],
        # with last element having rank j
        @cache
        def f(i, j):
            # Before processing any character,
            # we have one element, whose rank is 0.
            if i == -1:
                return 1 if j == 0 else 0

            ans = 0

            if s[i] == "I":
                # New last rank = j.
                # Previous last rank k must be < j.
                for k in range(j):
                    ans += f(i - 1, k)

            else:  # 'D'
                # New last rank = j.
                # Previous last rank k must be >= j.
                #
                # Previous ranks are 0...i.
                for k in range(j, i + 1):
                    ans += f(i - 1, k)

            return ans % mod

        # Last character is s[n - 1].
        # Final permutation has ranks 0...n.
        return sum(f(n - 1, j) for j in range(n + 1)) % mod
```

This is the basic recursion, you can also add a range sum caching to make i O(n^2).
