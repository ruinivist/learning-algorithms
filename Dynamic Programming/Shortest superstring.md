# Find shortest superstring

Give words, find smallest string that contains each word.

## Solution

Problem also states that I can assume no word is a substring of another word. Not sure where that'll be useful
at the moment.

Words are <= 12 so this has to be some subset dp.
f(mask) = the actual shortest string. Then I try to iterate and put in a word j that is not there yet.
It must either be present in which case the cost is 0 ( as in formed from the join of two words, across the
boundary ). Of match a suffix of j at the start or a prefix of j at the end.

One problem, my state as f(mask) = actual shortest is just plain wrong, as for a given mask there could be multiple.
Need to differentiate those.

Two more issues.
I mentioned a prefix check for word j being merged at start of word i.
That is not needed as it would be handled by the case where word j comes first and word i is being
added to the suffix.
As for the state then, you only need to know the last word j.
The condition that no word is substring of another is needed as now that I'm only looking at the last
word, I might start to append it even if it was already present.

> Note, offtopic. A push dp in a recursive mem setting is just f(...) that returns "remaining"

```python
class Solution:
    def shortestSuperstring(self, words: list[str]) -> str:
        n = len(words)

        # mask words are done and last was i, what more length is
        # is needed
        @cache
        def f(mask, i):
            if mask == (1 << n) - 1:
                return ""

            ans = ""
            for j in range(n):
                if mask >> j & 1 == 0:
                    # word(i) then word(j), so what prefix of j
                    # is in suffix of i
                    a = "" if i == -1 else words[i]
                    b = words[j]
                    # for all prefix slices of b, try to match a
                    overlap = max(k for k in range(len(b) + 1) if a.endswith(b[:k]))
                    nmask = mask | (1 << j)

                    # note, my f gives the "remaining"
                    tans = b[overlap:] + f(nmask, j)
                    if ans == "" or len(tans) < len(ans):
                        ans = tans

            return ans

        return f(0, -1)
```
