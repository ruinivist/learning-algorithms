# Frog Jump

the only thing worth nothing is the python @cache usage
I have a habit using indexes from cpp as even a recursive memo is backed by an
index.
You don't need that when doing @cache, in fact if you truly go all the way
with python syntax, you can JUST write the recurrence as code

```python
class Solution:
    def canCross(self, stones: list[int]) -> bool:
        n = len(stones)
        stones_set = set(stones)

        @cache
        def f(at, k):
            if at == stones[-1]:
                return True

            return any(
                f(nat, nk)
                for nk in [k - 1, k, k + 1]
                if (nat := at + nk) and nat != at and nat in stones_set
            )

        # that 2nd 0 is makes it so that the first jump is always 1
        # if even that
        return f(0, 0)
```

Note the any, the walrus operator the stones_set
