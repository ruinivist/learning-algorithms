# Count the repetitions

really bad statement for the problem but here is the simplied one.

(str, n) is str repeated n times and joined

str1 = (s1,n1)
str2 = (s2,n2)

Find max m such that (str2,m) is a subseqeunce of str1

## Solution

first observation is to note that ((s2,n2),m) is just (s2,n2 m)

So the problem becomes

(s1,n1) is the larger string. What is the max m copies of s2 can I match
as a subsequence of this larger string?

Now this is just a subsequence check but s1, n1 is quite large. I cannot naively
iterate.

Let's say that now we naively start matching, j being index in s2 of where I'm at in the
match. After one match I'm at some j' and start to match again, I might be at j'' again.
Also increasing a count if I match full of s2 and loop over. Note that for full iteration
of s1 to match, all that matters is where in s2 I started. I can have it return a count
as to how many times over are we able to match on s2 if we start a some given j.
Let the state then return, if I start at j, for new full s2, what is j' and count of loop
overs.
Then I can skip the s1 iteration and just iterate n1 instead.

```python
class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        @cache
        def f(j):
            # start at j in s2 and a fresh start in s1
            loops = 0
            for ch in s1:
                if s2[j] == ch:
                    j += 1
                    if j == len(s2):
                        loops += 1
                        j = 0

            return j, loops

        # now of the n1 times, how many copies of s2 are there
        copies = 0
        j = 0
        for i in range(n1):
            j, cur_copies = f(j)
            copies += cur_copies

        # so I can make copies number of s2
        # but this should be n2 x m <= copies
        return copies // n2
```

Another optimisation is possible where you also record how many s1 loops we completed between
seeing a given j the first time and seeing it a second time, and then using that to jump
over multiple iterations.
