# Number of ways to wear differents hats to each other

10 people, 40 hats, the ith one can wear hats that are in the list hats(i).
How many different ways?

## Solution ( inclusion exclusion / mobius inversion )

I'm just leaving this as a note as this is what I was initially thinking in the direction of,
when I first read the problem.

![assign-hats-incl-excl](./assign-hats-incl-excl.png)

## Solution ( assignment counting dp )

The core idea is to iterate over the smaller size via a mask and iterate over the larger one
in a loop.

f(i, mask) => first i hats are processes and mark people are done, retval is the ways
to assign till end from this state.

On the next hat, you can assign it to ANY of the relevant ones and count over the future
transition states.

> since you are iterating in a loop on hats, a collision cannot happen by virtue of ordering

```python
class Solution:
    def numberWays(self, hats: list[list[int]]) -> int:
        mod = int(1e9 + 7)
        n = len(hats)

        @cache
        def f(i, mask):
            if i == 41:
                return 1 if mask == (1 << n) - 1 else 0

            # not using i hat
            ans = f(i + 1, mask)
            # using i hat
            for j in range(n):
                if mask >> j & 1 == 0 and i in hats[j]:
                    # this person has no hat yet, pick one
                    nmask = mask | (1 << j)
                    ans += f(i + 1, nmask)
                    ans %= mod

            return ans

        return f(1, 0)
```
