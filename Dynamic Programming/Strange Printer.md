---
leetcode_url: https://leetcode.com/problems/strange-printer/
---

# Strange Printer

In one move you can assign the same char to any subrange. Number of moves to make a string s from "".

## Solution

contraints are really small, hinting at an interval dp.

I can assume the original string to just be "\_" \* len(s).
Then f(l,r) is just min steps to match this range, the transition are a bit tricky.

One I can see is for each character, pain the whole range with that char and sum over the splits that
are a different color. I think this is ALL that you need really.
Then in fact you can even operate on a run length encoding of the string, deleting the runlength itself
as the number of moves will remain the same.

I was initially doing something like => paint the entire range and then recurse where the colors don't
match but then there were flaws in it the biggest one being there is not much choice, it is just a greedy.

The cleaner idea is noticing that you of course want to paint s[l], so that will need one turn,
the only difference is do we paint s[l] and extend it all the way to some later s[t] as well, and to which
s[t]. This gives you the k to iterate over and the splits to sum over.
Since we use run length encoding, l+1 and t-1 are bound to be a different character so what to recurse on
is easy to see as well.

Another trap I fell into was not getting the recurrence right.
I did something like `1 + f(part been l and k) + f(part after k)`. It breaks for this case

```text
abaca
you pain all with and then recurse asking f(bac) as if it's from scratch when one a is already
painted
```

The recurrence instead should skip the current l as it'll piggyback on a future paint, that future
paint being k ( so you MUST paint that k by a turn making the subproblem being f(k,r))

```python
class Solution:
    def strangePrinter(self, s: str) -> int:
        s = [ord(ch) - ord("a") for ch, _ in groupby(s)]
        n = len(s)

        @cache
        def f(l, r):
            if l > r:
                return 0
            if l == r:
                return 1

            # no extension to any other range
            ans = 1 + f(l + 1, r)
            for k in range(l + 1, r + 1):
                if s[l] == s[k]:
                    # extend till k, the 1 to be counted
                    # would come from k, so not counted here
                    # it won't be k+1 for the same reason as you
                    # do want to count that one
                    # unless that k piggybacks as well
                    # but we leave that to the next state
                    ans = min(ans, f(l + 1, k - 1) + f(k, r))

            return ans

        return f(0, n - 1)
```
