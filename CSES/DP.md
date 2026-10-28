---
date: 19Jul26
---

# Dynamic Programming

## Dice Combinations

### way to make sum n by using a(i) repeatedly -> what is f?

- **defn**: f(i) = no of throws to make i
- **base**: f(<=0) = 1
- **trans**: f(i) = sum over throw in 1..6 : f(i-throw)

---

## Min Coins

### min number of a(i) needed ( rep ) to make sum n

Problem is framed as coins
- **def**: min no of coins needed
- **base**: f(<=0) = 0
- **trans**: f(i) = 1 + min{ f(i-coin) foreach coin  s.t. i-coin >=0  }

### implementation tricks

**sort** so that you can early break when current coin becomes too large so that all subequent coins are useless

---

## Coin Combinations 1

### distinct ways to make sum n from a(i)

**same as 1**
distinct is just that 1 + 2 is different from 2 + 1 which is what 1 has too

---

## Coin Combinations 2

### distinct "combinations" to make sum n using a(i)

1 + 2 is same as 2 + 1

**idea**: _sort_ and loop over coins first

- **def**: f(i) = no of ways
- **base**: f(0) = 1
- **trans**: for coin c, for sum x: f(i) += f(i-c) s.t. i-c >= 0

---

## Removing Digits

### given n, n' = n - some digit of n, needed min steps to make 0

First doubt I had was that this cannot be done iterative. But that's easy.

- **def**: f(i) = min steps to make i
- **base**: f(0) = 0
- **trasn**: f(i) = min{ i - d for each digit in i }
- **order**: calc f(i) from 1 to n

### Alt greedy solution

**idea**: always subtract largest since f(i) is increasing in nature as i increases

**why correct**:
Induction:
- base: f(0)<f(1)<=f(2)
- for k and k+1, I assume it holds for k

example: 24 -> 25 digit to be substracted increases by 1
example: 29 -> 30 digit to be subtracted ( 3 ) increase by 1

this at the surface means I have a better subtraction if I go up
n - (d+1) = (n-1) - d
so even if I go up, I would end up at the same number
for above n = 30, d = 2, so 30 - (3) = 29 - 2

---

## Grid Paths

### 2d grid with some blocks, no of paths from tl to br

trivial

---

## Bookshop

### N^2 knapsack ( 1 use items )

two attributes, maximise one, constraint other by <= .
I was initially tricked by the O(nx) being 10^6 but that's fine apparently

vars are usually val and wt

**def**: f(i,w) : max val using first i s.t. total weight <= w
**base**: f(0,any) = 0
**trans**: loop over items, loop over weights : f(i,w) = max(this, val + f(i-1,w-item)) where w-item >= 0

**impl trick**: can just use a dp(wt) array and overwrite from right to left ( as 1 use )

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, W;
    cin >> n >> W;

    vector<int> wt(n), val(n);
    for (int &x : wt)
        cin >> x;
    for (int &x : val)
        cin >> x;

    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        int w = wt[i], v = val[i];
        for (int j = W; j >= w; j--) {
            dp[j] = max(dp[j], dp[j - w] + v);
        }
    }

    cout << dp[W] << "\n";

    return 0;
}
```

---

## Array Description

### a(i) = 0 to m ( m <= 100 ), constraint abs(a(i)-a(i+1))<=1, 0 means a(i) can be 1 to m anything. Count num arrays

O(nm) solution is obvious

- **def**: f(i,m) = ith value, filled with m, no of ways
- **base**: f(1,j) = 1 if a(1) == 0 || a(1) == j
- **trans**: f(i,j) = f(i-1,k) where k = valid values based on a(j)

There is an active window optimisation that does a better average case run time but same worst.
There is also some sparse window optims in case array has a lot of zeroes.

---

## Counting Towers

### unlim supply of int x int towers, now of ways to build a h x 2 tower

- **def**: f(n,2): built upto height n ( flat top ) such that the last row is joined (0), broken (1)
- **base**: f(1,0) = f(1,1) = 1

**trans**

when joined:
place a broken split -> to 1 with f(i-1) ways
place a joined split -> to 0 with f(i-1) ways
extend the join -> to 0 with f(i-1) ways

so to 1 -> f(i-1) ways
to 0 -> 2f(i-1) ways

when broken:
the first two above repeat ( they are basically you don't extend the segments )
extend the split -> to 1, only left, only right or both => 3*f(i-1) ways

so to 1 in 4f(i-1) ways
to 0 in f(i-1) ways

---

## Edit Distance

### edit distance (ops are: del from a, del from b, convert some char to other)

- **def**: f(i,j) = edit dist for prefix len i and prefix len j
- **base**: f(0,j) = j, f(i,0) = i
- **trans**: for i, for j : f(i,j) = min{ f(i-1,j), f(i,j-1), f(i-1,j-1) + a(i-1)!=b(j-1) }

---

## LCS

### lcs, calculate and print

similar to edit dist

- **def**: f(i,j) : length of lcs using prefix of len i, and prefix of len j
- **base**: f(i,0) = f(0,j) = 0
- **trans**: for i, for j : if a(i-1) == b(j-1) 1 + f(i-1,j-1) else max( f(i-1,j), f(i,j-1) )

**print**: visualise the 2d grid, row, col,
if both same both decrease else go in the direction where lcs remains max

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define in long long
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (int &x : a)
        cin >> x;
    for (int &x : b)
        cin >> x;
    vector<vector<in>> dp(n + 1, vector<in>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i - 1] == b[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    cout << dp[n][m] << "\n";

    vector<int> ans;
    while (dp[n][m] > 0) {
        if (a[n - 1] == b[m - 1]) {
            ans.push_back(a[n - 1]);
            n--;
            m--;
        } else if (dp[n - 1][m] > dp[n][m - 1]) {
            n--;
        } else {
            m--;
        }
    }
    reverse(ans.begin(), ans.end());
    for (int x : ans)
        cout << x << " ";
    cout << "\n";
#undef int
}
```

---

## Rectangle Cutting

### a x b, can cut horizontally or vertically, min cuts to make all cuts squares

**O(n^3)**

this is not dp just brute force and mem

- **def**: f(i,j) ans for i,j
- **base**: f(i,0) = f(0,j) = 0, rest = INF

**trans**: for i, for j
if i==j, that's square, f(i,j) is 0
else
f(i,j) = min self with
	for horizontal cut : f(x,j) + f(i-x,j) + 1
	for verti cut      : f(i,y) + f(i,j-u) + 1

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n, m;
    cin >> n >> m;
    const int inf = (int)1e18;
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (i == j) {
                dp[i][j] = 0;
            } else {
                dp[i][j] = inf;
                for (int k = 1; k < i; k++) {
                    dp[i][j] = min(dp[i][j], dp[k][j] + dp[i - k][j] + 1);
                }
                for (int k = 1; k < j; k++) {
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[i][j - k] + 1);
                }
            }
        }
    }
    cout << dp[n][m] << "\n";

#undef int
}
```

---

## Minimal Grid Path

### 2d grid of chars, lexico min path from tl to br

**greedy with tied states/bfs dp**

The idea is very greedy like.

All paths are of same len, so must pick smaller.
What if same? Maintain a candidate set, off all nexts from a candidate, pick the minimum.
Cull candidates so that all next are with that minimum.

Tricks ( 2 ):
neighbor visit order, right then down, this makes range sorted
since sorted order of visites, if same as prev, don't insert

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n;
    cin >> n;
    vector<string> v(n);
    for (auto &x : v)
        cin >> x;

    vector<pair<int, int>> candidates, new_candidates;
    candidates.push_back({0, 0});

    // order matters, right then down makes (0,0)->(0,1)->(1,1)->(1,2) which is
    // sorted
    vector<int> dx = {0, 1};
    vector<int> dy = {1, 0};

    int steps = 2 * n - 1;
    while (steps--) {
        char mn = 'Z' + 1;
        int sz = (int)candidates.size();
        for (auto &[x, y] : candidates) {
            mn = min(mn, v[x][y]);
        }

        cout << mn;

        new_candidates.clear();
        for (auto &[x, y] : candidates) {
            if (v[x][y] != mn)
                continue;
            for (int dir = 0; dir < 2; dir++) {
                int nx = x + dx[dir];
                int ny = y + dy[dir];
                if (nx < n && ny < n &&
                    (new_candidates.empty() ||
                     new_candidates.back() != make_pair(nx, ny))) {
                    new_candidates.push_back({nx, ny});
                }
                // at each step there can be too many duplicates so filter those
            }
        }

        swap(candidates, new_candidates);
    }
    cout << '\n';

#undef int
}
```

---

## Money Sums

### n integers, num of distinct sums possible ( n ~ 100, a(i) ~ 1000 )

**subset sum**

- knapsack like iteration
- single bool array of if possible

f(0) = 1
for each cur, for tgt (reversed) : f(tgt) |= f(tgt-cur)

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n;
    cin >> n;
    vector<int> v(n);
    for (int &x : v)
        cin >> x;

    const int N = (int)1e5 + 5;
    vector<int> dp(N, 0);
    dp[0] = 1;

    int ans = 0;
    for (int cur : v) {
        for (int i = N - 1; i >= cur; i--) {
            if (dp[i - cur] && !dp[i])
                dp[i] = 1, ans++;
        }
    }

    cout << ans << "\n";
    for (int i = 1; i < N; i++) {
        if (dp[i]) {
            cout << i << " ";
        }
    }
    cout << "\n";

#undef int
}
```

Futher:
count distinct ways, bounded case where 2 2 2 should give way as 1 for 4

---

## Removal Game

### array of ints, remove from ends, who wins and score?

**minimax** trick ( maximise the minimum, it's inverted )
what u need? constant/0 sum (of scores) and symmetric rules

trick is to instead of max score, max my - other score
aka other's points are -ve and score is basically my sum - other sum

- **def**: f(i,j) = max score (per mine - other), segment i to j
- **base**: f(i,i) = a(i)
- **trans**: f(i,j) = max{ v(i) + f(i-1,j), v(j) + f(i,j-1) }

finding score: s1 - s2 = dp ans, s1 + s2 = known constant sum

**fill order**: small to large segments

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n;
    cin >> n;
    vector<int> v(n);
    for (int &x : v)
        cin >> x;

    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int i = 0; i < n; i++)
        dp[i][i] = v[i];
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            dp[i][j] = max(v[i] - dp[i + 1][j], v[j] - dp[i][j - 1]);
        }
    }

    int ans = dp[0][n - 1];
    int sum = accumulate(v.begin(), v.end(), 0LL);
    cout << (sum + ans) / 2 << "\n";

#undef int
}
```

---

## Two Sets 2

### num ways to partition 1..n in two sets of same sum

**1/0 subset sum - no of ways**
**no soln case**

---

## Mountain Range

### mountain range: dp on cartesian tree ( dag )

**processing order** : there has to be some order of processing, usually it's index based in dp problems, but can be some prop too

**process by heights** is the trick here

### method one - inversion

if I jump from a higher one to a lower one, I have branching as my set is all smaller ones. For 5 1 4, I can jump from 5 to 1 and have more range later
or to 4 and have better height too.

**inversion**, instead jump from 1 and look to go higher, greedy is best, you always want to go the next higher to the left or right, so once you
are on u, you know you can only go left or right the next higher => dp must end at u

- **def**: dp(u) => max range ending at u
- **base**: dp(u) = 1
- **trans**: in dec heights ( so sort ), dp(u) = max{ self, 1 + dp(left higher), dp(right higher) }

### method two - tree break + dp

make a cartesian tree out of it ( dag ) and then do dp on dap ( similar ). The tree is same as above, for each node, you have two neigbors, next higher
to left and right.

The processing order is same as dp, it's exactly a tree of dp states, so you do a recursion ( or get a topo order and iteration ).

### mono stack template?

loop -> ensure mono -> if has elem, update pos -> push cur

### code

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n;
    cin >> n;
    vector<pair<int, int>> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i].first;
        v[i].second = i;
    }

    auto mono_stack = [](const auto &arr, auto first, auto last, auto should_pop) {
        int n = arr.size();
        vector<int> res(n, -1);
        vector<int> st;

        for (auto it = first; it != last; ++it) {
            while (!st.empty() && should_pop(arr[st.back()].first, (*it).first)) {
                st.pop_back();
            }
            int i = &(*it) - arr.data();

            if (!st.empty())
                res[i] = st.back();
            st.push_back(i);
        }
        return res;
    };

    auto gt_left = mono_stack(v, v.begin(), v.end(), less_equal<int>());
    auto gt_right = mono_stack(v, v.rbegin(), v.rend(), less_equal<int>());

    sort(v.begin(), v.end(), greater<>());

    vector<int> ans(n, 1);
    for (auto [h, idx] : v) {
        if (gt_left[idx] != -1) {
            ans[idx] = max(ans[idx], 1 + ans[gt_left[idx]]);
        }
        if (gt_right[idx] != -1) {
            ans[idx] = max(ans[idx], 1 + ans[gt_right[idx]]);
        }
    }

    cout << *max_element(ans.begin(), ans.end()) << endl;

#undef int
}
```

---

## Increasing Subsequence

### lis

**tails idea**

f(u) = min ending element of lis of len u + 1

Idea is greedy based, for an element, you extend the range if you can ( when cur is higher and all existing ) or try to min the end of
some existing length so that some future elem can benefit ( equivalent swap, same lenght better future possibility )

```c++
#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n;
    cin >> n;
    vector<int> v(n);
    for (int &x : v)
        cin >> x;

    vector<int> lis;
    for (int x : v) {
        auto it = lower_bound(lis.begin(), lis.end(), x);
        if (it == lis.end()) {
            lis.push_back(x);
        } else {
            *it = x;
        }
    }

    cout << (int)lis.size() << "\n";
#undef int
}
```

### change for l non-decreasing s?

use upper bound, that's it

---

## Projects

### prefix max optim dp

usual pattern is f(j) = max f(i) for i <= some limit

**thinking compression? you can use sorting and indexes instead of values**

### implementation niceness

can use this type of logic to process evens based on keypoints and type

```c++
for (auto [time, project, is_end] : events) {
	if (is_end) {
	    result = max(result, money[project]);
	} else {
	    money[project] = result + p[project];
	}
}
```

---

## Elevator Rides

### n people, one move only allows wt sum <= W, min no of moves

**bitmask dp => n ~ <= 20**

### 3^n trick

naive is => for each bitmask, for each subset (3 ^ n)

```c++
for (int m = 0; m < (1 << N); ++m) {
    for (int s = m; s > 0; s = (s - 1) & m) {
    	// empty subset is not here
    }
}
```

### optimising to n.2^n

maintain a greedy, similar to how lis does it.
for a set of people, you have a fixed wt

**keep min wt for last ride ( for each subset of people reached )**

### imp trick

seq min needed here, min rides, if same min over wt ( f1, f2, f3..) based on priority

can just do min( aggregate pair/array/vector ) after making the tans entry

### code

```c++
#include <bits/stdc++.h>
using namespace std;
 
int main() {
#define int long long
    int n, w;
    cin >> n >> w;
    vector<int> v(n);
    for (int &x : v)
        cin >> x;
 
    const int INF = (int)1e18 + 5;
    vector<array<int, 2>> dp(1ll << n, {INF, INF});
 
    // f(i) = {min rides, min last ride wt}
    dp[0] = {1, 0}; // extend last keeping rides as 1
 
    for (int i = 1; i < (1ll << n); i++) {
        for (int j = 0; j < n; j++) {
            // skip if unset
            if (!((i >> j) & 1))
                continue;
 
            auto prev = dp[i ^ (1ll << j)];
            if (prev[1] + v[j] <= w) {
                // no new ride
                dp[i] = min(dp[i], {prev[0], prev[1] + v[j]});
            } else {
                dp[i] = min(dp[i], {prev[0] + 1, v[j]});
            }
        }
    }
 
    cout << dp[(1ll << n) - 1][0] << "\n";
 
#undef int
}
```

---

## Counting Tilings

### broken profile / connectivity dp :  10 x 1000 grid, way to fill with 1x2 and 2x1 grids

**bitmask but dp is not subset rather the shape**

**key is to process col by col and maintain a "shape"**

f(i,mask) : filled till col i, mask (row size) => 1 means this cell is filled via extension frol col i-1

### method 1 : subset dp ( 3^n )

for each col, for each cur profile
	prev profile = inverted
	// now some can be filled via vertical and some need to be extensions
	for each submask of vertical ( call that this is what's extension based )
		vertical = complement extension
		if vertical is valid => add

### code 1

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n, m;
    cin >> n >> m;

    vector<int> cur(1ll << n, 0), next(1ll << n, 0);
    cur[0] = 1; // clean profile is 1 way

    // prcompute what masks are fillable by vertical cols
    // basically what bits are vertically fillable
    vector<bool> fillable(1ll << n, false);
    for (int mask = 0; mask < (1ll << n); mask++) {
        bool can = true;
        // idea is that seq of one bits should be even length
        int len = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1ll << i)) {
                len++;
            } else {
                if (len & 1) {
                    can = false;
                    break;
                }
                len = 0;
            }
        }
        // last seq
        if (len & 1)
            can = false;
        fillable[mask] = can;
    }

    const int mod = (int)1e9 + 7;

    for (int j = 0; j < m; j++) { // for each col
        fill(next.begin(), next.end(), 0);
        for (int profile = 0; profile < (1ll << n); profile++) { // for each profile
            int prev_profile = ((1ll << n) - 1) ^ profile;       // inverted

            for (int sub = prev_profile;; sub = (sub - 1) & prev_profile) {
                // submasks of prev_profile, what's not filled should be
                // fillable by vertical cols

                int vertical = prev_profile ^ sub;
                if (fillable[vertical]) {
                    (next[profile] += cur[sub]) %= mod;
                }

                // submask iteration that processes 0 submask too
                if (sub == 0)
                    break;
            }
        }
        cur.swap(next);
    }

    cout << cur[0] << "\n";

#undef int
}
```

### method 2 : precomp transitions

complexity changes based on no of transitions which no depends on the tiles

**from a left mask to right mastk, is the transition possible**
if I have this, I can just jump cols more easily

### code 2
```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n, m;
    cin >> n >> m;

    vector<int> cur(1ll << n, 0), next(1ll << n, 0);
    cur[0] = 1; // clean profile is 1 way
    const int mod = 1e9 + 7;

    // precomp transitions that are valid ( left mask -> right mask )
    vector<pair<int, int>> trans;
    auto gen = [&](auto &&f, int row, int left, int right) -> void {
        if (row > n)
            return;
        if (row == n) {
            trans.emplace_back(left, right);
            return;
        };
        // 1 => is this filled by extension from prev col
        // 1x2 place, left 0, right filled by extension
        f(f, row + 1, left, right | (1ll << row));
        // another valid is when left acceps an extension, in this case right is 0
        // as we place a new 1x2 here
        f(f, row + 1, left | (1ll << row), right);
        // vertical 2x1, set both as 0
        f(f, row + 2, left, right);
    };
    gen(gen, 0, 0, 0);

    for (int j = 0; j < m; j++) { // for each col
        fill(next.begin(), next.end(), 0);
        for (auto &[left, right] : trans) {
            (next[right] += cur[left]) %= mod;
        }
        swap(cur, next);
    }

    cout << cur[0] << "\n";

#undef int
}
```

### method 3: actual broken profile (mn2^n)

moving cell by cell instead of col by col as in previous subset solution

you do the same thing as moving down row by row, except in place

very specific to the 1x2 as it used the marking trick

### code 3

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
    int n, m;
    cin >> n >> m;

    vector<int> cur(1ll << n, 0), next(1ll << n, 0);
    cur[0] = 1;

    const int mod = 1e9 + 7;

    for (int j = 0; j < m; j++) {
        for (int i = 0; i < n; i++) {
            fill(next.begin(), next.end(), 0);
            for (int mask = 0; mask < (1ll << n); mask++) {
                if (!cur[mask]) // not reachable
                    continue;

                // blocked => next is filled via col-1 (cur)
                // so 1 here = do I fill next col too?
                bool blocked = (mask & (1ll << i)) != 0;
                if (blocked) {
                    int next_mask = mask ^ (1ll << i); // must be 0
                    (next[next_mask] += cur[mask]) %= mod;
                } else {
                    // two choices, place vertical or horizontal

                    // horizontal
                    int next_mask = mask | (1ll << i); // next mask if filled by col-1, aka cur
                    (next[next_mask] += cur[mask]) %= mod;

                    // cur is a valid mask for vertical placement
                    if (i + 1 < n && (mask & (1ll << (i + 1))) == 0) {
                        next_mask = mask; // it isn't filled at all
                        // i+1 needs to be marked as filled so that loop
                        // skips it
                        next_mask |= (1ll << (i + 1));
                        (next[next_mask] += cur[mask]) %= mod;
                    }
                }
            }
            cur.swap(next);
        }
    }

    cout << cur[0] << "\n";

#undef int
}
```

---

## Counting Numbers

### from a to b where no two adjacent are same

**digit dp**

elements of a template
- reverse
- pos
- tight
- leadzing zeros (lz)
- other state

### template

```c++
int dp(int pos, bool tight, bool lz, int state) {
    if (pos == S.size()) return 1;
    if (MEMO[pos][tight][lz][state] != -1) return MEMO[pos][tight][lz][state];

    int limit = tight ? (S[pos] - '0') : 9;
    int ans = 0;

    for (int digit = 0; digit <= limit; digit++) {
        bool new_tight = tight && (digit == limit);
        bool new_lz = lz && (digit == 0);
        
        int new_state = state;
        if (!new_lz) {
            // new_state update logic
        }

        ans += dp(pos + 1, new_tight, new_lz, new_state);
    }

    return MEMO[pos][tight][lz][state] = ans;
}
```

### code

you almost always want to follow this style

```c++
#include <bits/stdc++.h>
using namespace std;

#define int long long

int MEMO[20][2][2][10];
string s;

int dp(int pos, bool tight, bool lz, int prev) {
    if (pos == (int)s.size())
        return 1;
    if (MEMO[pos][tight][lz][prev] != -1)
        return MEMO[pos][tight][lz][prev];

    int limit = tight ? (s[pos] - '0') : 9;
    int ans = 0;

    for (int digit = 0; digit <= limit; digit++) {
        bool new_tight = tight && (digit == limit);
        bool new_lz = lz && (digit == 0);

        // !new_lz => I placed some digit that makes it non leading zero
        if (digit == prev && !new_lz)
            continue;
        ans += dp(pos + 1, new_tight, new_lz, digit);
    }

    return MEMO[pos][tight][lz][prev] = ans;
}

signed main() {
    int a, b;
    cin >> a >> b;

    auto f = [&](int x) {
        if (x < 0)
            return 0ll;
        if (x == 0)
            return 1ll;
        s = to_string(x);
        memset(MEMO, -1, sizeof(MEMO));
        return dp(0, 1, 1, 0);
    };

    cout << f(b) - f(a - 1) << "\n";
}
```

---

## Increasing Subsequences 2

### inc seq count

lis is max 1 + f(i) for a(i) < a(j). this is sum 1 + f(i) for a(i) < a(j),

**lis general case using ft/st**

- **def**: f(i) = len/cnt of lis ending at i
- **base**: f(i) = 1 (atleast)
- **trans**: for i, f(i) = max self, 1 + f(j) s.t. j < i (prefix, build online) and a(j) < a(i) (coord comp)

### compress steps?

copy -> sort -> unqiue -> assign index by lower bound search

### code

```c++
#include <bits/stdc++.h>
using namespace std;

#define int long long

signed main() {
    int n;
    cin >> n;
    vector<int> v(n);
    for (int &x : v)
        cin >> x;

    // cnt doesn't change on compression
    auto compress = [&](vector<int> &arr) {
        vector<int> sorted = arr;
        sort(sorted.begin(), sorted.end());
        sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());
        for (int &x : arr) {
            x = lower_bound(sorted.begin(), sorted.end(), x) - sorted.begin();
        }
    };
    compress(v);

    const int mod = 1e9 + 7;
    vector<int> ft(n + 1, 0);
    auto add = [&](int i, int val) {
        for (++i; i <= n; i += i & -i)
            (ft[i] += val) %= mod;
    };
    auto sum = [&](int i) {
        int res = 0;
        for (++i; i > 0; i -= i & -i)
            (res += ft[i]) %= mod;
        return res;
    };

    int ans = 0;
    for (int i = 0; i < n; i++) {
        int less = sum(v[i] - 1);
        (ans += 1 + less) %= mod;
        add(v[i], 1 + less);
    }

    cout << ans << '\n';
}
```

