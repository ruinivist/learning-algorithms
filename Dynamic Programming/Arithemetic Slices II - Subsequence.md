# Arithemetic Slices II - Subsequence

How many AM subsequences are there in the list?
Atleast 3 elements to count as AM subsequence.

## Solution

An initial thought starts at iterating over all differences and just answering, how many
subsequences exist for that given difference d. If I can do it in linear that all I need to do.

f(i) = I'm at i and I'm taking i = sum over f(i-d) in prefix as you are just extending those.
The tricky part is the limit of 3. Maybe you can be very clever on base states of you just make that
as a param so it becomes f(i, size so far including this i one as well)

Then that second param just needs to be 1, 2 and 3 and what you do is that you count all 3 ones.

We're still not in the clear though as the number of such "d"s can be nC2 and n is ~1000 here.

But here's that implementation, note that dp itself has changed to indexes and we are prefix summing
manually, there wasn't a clean way to do it all recursive while still applying the prefix sum optim.

```python
from collections import defaultdict

class Solution:
    def numberOfArithmeticSlices(self, nums: list[int]) -> int:
        n = len(nums)

        all_d = {
            nums[j] - nums[i]
            for i in range(n)
            for j in range(i + 1, n)
        }

        ans = 0

        for d in all_d:
            dp1 = [0] * n
            dp2 = [0] * n
            dp3 = [0] * n

            pref1 = defaultdict(int)
            pref2 = defaultdict(int)
            pref3 = defaultdict(int)

            for i in range(n):
                x = nums[i]
                prev = x - d

                # length exactly 1
                dp1[i] = 1

                # Extend all length-1 subsequences ending in x-d
                dp2[i] = pref1[prev]

                # Extend all length-2 or length>=3 subsequences
                # ending in x-d
                dp3[i] = pref2[prev] + pref3[prev]

                ans += dp3[i]

                # Add this index into the prefix
                pref1[x] += dp1[i]
                pref2[x] += dp2[i]
                pref3[x] += dp3[i]

        return ans
```

But this is n^3 and my bet on all d "happening" to be small enough was just wrong.
So we try to do better.

> python note, `defaultdict(int)` is just `{}` with 0 as missing key fallback, just like cpp
> that "int" is very much needed, it is the "default factory", not givign any makes it same as {}

Note that the innermost loop cannot be simpler than O(n) for a given difference so something needs
to be optimised at that outer n^2 level.

## Ideal solution

f(i,d) = count such that we end at nums i and have difference d such that length is alteast 2

for this entry to exist, some j < i must've been there such that the d in this arg here
is nums[i] - nums[j].

Let's analyse how many d can exist for a given i. Previously we just did a cross product for differences
and it is indeed true that there can be O(n^2) such differences so that state naively looks to be still
n^3.

But those two are clubbed.
dp(0,...) <= 0 as we don't have any j
dp(1,...) <= 1 as we have just 1 sized prefix
dp(i,...) <= i as the prefix lenght is i so we can only choose from that
so summing over, the combined f(i,d) state becomes n^2.

The computation follows that as well.

The recurrences are
f(i,d) = for each j < i => 1 ( start a new len 2 subseq ) + f(j, d = nums[i] - nums[j])
note that the answer needs to be len 3, so what we do is at this level
sum over f(j,d) as well as each previous one was len 2 and now we extended it to become len 3

Another thing to note is the inability for a pure f(i,d) recursion to be
able to the whole thing cleanly. You could have it like f(i) and return
an array but then that's just iterative.

I don't think there is a clear way to do this problem purely via @cache
without a filtered iteration with the rec loop as you need that n^2
f(i,d) call and then you also need to run that loop once inside, so make
the "sum" still constant you need a filter like for this (i,d) only
iterate these j. Problem is not being able to merge the j iteration in
recursive.

```
from collections import defaultdict


class Solution:
    def numberOfArithmeticSlices(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [defaultdict(int) for _ in range(n)]

        ans = 0
        for i in range(n):
            for j in range(i):
                d = nums[i] - nums[j]
                dp[i][d] += 1 + dp[j][d]
                ans += dp[j][d]

        return ans
```
