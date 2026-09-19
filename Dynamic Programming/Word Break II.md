# Word Break II

what you need is a fast check for if i...j is in dictionary, the rest is same
as any partitioning problem, you can iterate over all possible ends for the
next partition.

One classis mistake that I did was to use a "built" array and do a backtracking
style push. If you do it this way, you cannot memoise it cleanly as you now
depend on that build. A memo only works if you store the full state, by saving
on retvals aka having none, I do not at all memoise and return a result early.

> for python, just use sets, they use hash tables for contains checks

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        n = len(s)
        # python has it via hash tables
        words = set(wordDict)

        @cache
        def f(i):
            if i == n:
                return [[]]

            res = []

            for j in range(i, n):
                word = s[i:j+1]
                if word in words:
                    for rem in f(j+1):
                        res.append([word] + rem)

            return res

        return [" ".join(ans) for ans in f(0)]
```
