# Longest Valid Parantheses

**Parantheses ~ stack**, with you just matching and popping till you can.
This asks for a substring so what is "dynamic" about it? That if you are
at position p, the start can be anything, and you can't just pop to match it;
need linear here.

There's another idea to such matches, the "imbalance" one where you keep track
of the imbalance formed due to matching, here this one is easier.

Def $im(i) = \text{imbalance with ( increating it and ) decreating it}$
At any pos $p$, if you are at imbalance $im$, if you look at the last position where
it was $im$ before, then you can say the subrange has 0 imbalance.

A naive solution that tries to just match imbalance fails to account for `()(()` case.
You'll match `)(()` based on im of 1 matching twice. The missing constraint is that
the im MUST always be >=0 for every prefix of a valid substring.

What this second contraint gives you is that if started accumulating from 0, and the im
goes negative, you MUST shift the start. Since it's now negative, there is just not
enough "(" in the prefix to match, you MUST ditch the entire prefix and start from HERE
as the new boundary.

The solution is suprisingly short if you use this idea. It also uses the fact that
imbalance at one step ONLY changes by 1.

> what we're doing is DECOMPOSING the input to contiguous matching ranges

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        # stk(i) = index of the last boundary, increasing
        # 0 based so -1
        # this stk keeps track of boundaries
        stk = [-1]
        ans = 0

        for idx, ch in enumerate(s):
            # can only inc
            if ch == "(":
                stk.append(idx)
            else:
                # can be unconditional as invariant:
                # some boundary always there
                stk.pop()

                # if empty
                if not stk:
                    # no boundaries exist, we popped too
                    # many times to get to an invalid state
                    # new boundary
                    # "forever" boundaries
                    stk.append(idx)
                else:
                    ans = max(ans, idx - stk[-1])

        return ans
```

Invariants

- `stk[0]` is the most recent index that CANNOT be crossed by a valid substring
- if it ever contains a `)` then that will remain forever, except only be incremented
  by say another `)` that pops it and then pushes it's own index.

Or

- `stk[0]` is the most recent `)` or `-1`. This is always a forever boundary, if you ever
  empty it, you push.
- `stk[1:]` are unmatched `(`
