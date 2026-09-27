# Freedom Trail

The problem is simple, in fact deceptively simple.
You have a ring dial and you want to spell out a word with it. One step is pressing the button
to pick that char at the top end of the dial, as well as one clockwise of counter-clockwise
rotation.

Min moves to spell something out is needed.

## Solution

Initially I was thinking, why not just do a greedy?
But there can be a case where you rotate to a farther off position because all the next ones we
need till the end are much closer and would accumulate a lower cost.
With this, there's no other way but to do a dp.

To represent the dial, all you need is the starting index. Same for the key.
Then for each char in key that I'm looking at, I can jump to any character on the ring
in that number of moves and continue on from key + 1.
It would be faster if you pre-compute the needed jump indexes but not doing that is fine
as well given the contraints.

```python
class Solution:
    def findRotateSteps(self, ring: str, key: str) -> int:
        n, m = len(key), len(ring)

        @cache
        # i = key pos, j = ring pos
        def f(i, j):
            if i == n:
                return 0

            # a littl bit of pruning, since if you are on the
            # same char it's just a constant, the first jump
            # would account for a less optimal position, not
            # any in between
            if key[i] == ring[j]:
                return 1 + f(i + 1, j)

            ans = math.inf
            need = key[i]
            for nj, ch in enumerate(ring):
                if ch == need:
                    non_loop_dist = abs(j - nj)
                    steps = min(non_loop_dist, m- non_loop_dist)
                    # steps to rotate and 1 to press it
                    ans = min(ans, 1 + steps + f(i + 1, nj))

            return ans

        return f(0, 0)
```
