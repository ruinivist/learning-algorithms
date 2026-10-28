---
date: 19Jul26
---

# Trees

## Company Queries

```cpp
// problem: go up k levels
// tag: bin lift

#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
	int n, q;
	cin >> n >> q;
	vector<vector<int>> g(n + 1);
	for (int i = 2; i <= n; i++) {
		int u;
		cin >> u;
		g[u].push_back(i);
		// now in this I'm given u -> i as input
		// so I could've filled up(u, 0) directly with no
		// dfs but in general if you given bidirectional
		// edges, you would need a "rooting" ( here it's
		// baked into the direction )
		// NOTE: think of what would dfs from 1 do,
		// you need top to down edges
	}

	const int D = (int)ceill(log2l(2e5 + 5));
	vector<vector<int>> up(n + 1, vector<int>(D + 1));

	auto fill0 = [&](auto &&f, int u, int par) -> void {
		// in this I use the convencion of 0 as no par
		// I've always used -1 but I think this new one is good too
		if (par)
			up[u][0] = par;
		for (int v : g[u])
			if (v != par)
				f(f, v, u);
	};
	fill0(fill0, 1, 0);

	for (int d = 1; d <= D; d++) {
		for (int i = 1; i <= n; i++) {
			// go 2^(d-1) up and then 2^(d-1) from there
			// using 0 to represent as NO more up is good implementationally
			// over say -1 as then the 0 naturally flows to up(0) which has
			// all elems 0 naturally
			up[i][d] = up[up[i][d - 1]][d - 1];
		}
	}

	auto lift = [&](int u, int k) {
		// the idea being you can represent k as powers of 2 -> binary
		// so going k up can be split into multiple steps of going up
		for (int i = 0; i <= D; i++) {
			if ((k >> i) & 1) {
				u = up[u][i];
			}
		}
		return u;
	};

	while (q--) {
		int u, k;
		cin >> u >> k;
		int res = lift(u, k);
		res = res == 0 ? -1 : res;
		cout << res << "\n";
	}

#undef int
}
```

## Company Queries 2

```cpp
// problem: lca
// tag: bin lift

#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
	int n, q;
	cin >> n >> q;
	vector<vector<int>> g(n + 1);

	const int D = (int)ceill(log2l(2e5 + 5));
	vector<vector<int>> up(n + 1, vector<int>(D + 1));

	for (int i = 2; i <= n; i++) {
		int u;
		cin >> u;
		g[u].push_back(i);
		up[i][0] = u;
	}

	for (int d = 1; d <= D; d++) {
		for (int i = 1; i <= n; i++) {
			up[i][d] = up[up[i][d - 1]][d - 1];
		}
	}

	auto lift = [&](int u, int k) {
		for (int i = 0; i <= D; i++) {
			if ((k >> i) & 1) {
				u = up[u][i];
			}
		}
		return u;
	};

	vector<int> h(n + 1);
	auto hfill = [&](auto &&f, int u, int par) -> void {
		if (par)
			h[u] = h[par] + 1;
		for (int v : g[u])
			if (v != par)
				f(f, v, u);
	};
	hfill(hfill, 1, 0);

	auto lca = [&](int u, int v) {
		if (h[u] < h[v])
			swap(u, v);
		// invariant, h(u) >= h(v)

		int diff = h[u] - h[v];
		u = lift(u, diff);

		// WARN: remember, otherwise you start from the current lca
		// and the invariant that both are not same used in loop ahead
		// breaks
		if (u == v)
			return u;

		// now at same level
		// there MUST exist some k such that
		// moving just one level up from k, they both become same
		// and I have information about the bits of such k by the
		// fact that bit i is 1 if after moving that level up they
		// are both NOT same ( once you reach lca both must be same )

		// note that we cannot go in the other direction as it's
		// greedily searching for jumps ( think that we are ruling out
		// suffixes here ), if a suffix is ruled out in the MAX jump case
		// where we had not reduced the distance in any other way
		// that it's ruled out for good
		// if on the other hand many incorrect small jumps can make
		// a later larger jump impossible to make
		// you can even say this is binary search ( the 2^n variation )
		// where I try say 32 then 16 then 8 and so on
		for (int i = D; i >= 0; i--) {
			if (up[u][i] != up[v][i]) {
				u = up[u][i];
				v = up[v][i];
			}
		}

		return up[u][0]; // one above is the lca
	};

	while (q--) {
		int u, v;
		cin >> u >> v;
		cout << lca(u, v) << "\n";
	}

#undef int
}
```

## Distance Queries

```cpp
// problem: fast pair distances
// tag: lca decomposition

#include <bits/stdc++.h>
using namespace std;

int main() {
	// finally needed to put these in for this problem
	cin.tie(nullptr);
	ios_base::sync_with_stdio(false);

#define int long long
	int n, q;
	cin >> n >> q;
	vector<vector<int>> g(n + 1);

	const int D = (int)ceill(log2l(2e5 + 5));
	vector<vector<int>> up(n + 1, vector<int>(D + 1));

	for (int i = 0; i < n - 1; i++) {
		int u, v;
		cin >> u >> v;
		g[u].push_back(v);
		g[v].push_back(u);
	}
	vector<int> h(n + 1);
	auto hfill = [&](auto &&f, int u, int par) -> void {
		if (par) {
			h[u] = h[par] + 1;
			up[u][0] = par;
		}
		for (int v : g[u])
			if (v != par)
				f(f, v, u);
	};
	hfill(hfill, 1, 0);

	for (int d = 1; d <= D; d++) {
		for (int i = 1; i <= n; i++) {
			up[i][d] = up[up[i][d - 1]][d - 1];
		}
	}

	auto lift = [&](int u, int k) {
		for (int i = 0; i <= D; i++) {
			if ((k >> i) & 1) {
				u = up[u][i];
			}
		}
		return u;
	};

	auto lca = [&](int u, int v) {
		if (h[u] < h[v])
			swap(u, v);

		int diff = h[u] - h[v];
		u = lift(u, diff);

		if (u == v)
			return u;

		for (int i = D; i >= 0; i--) {
			if (up[u][i] != up[v][i]) {
				u = up[u][i];
				v = up[v][i];
			}
		}

		return up[u][0]; // one above is the lca
	};

	auto dist = [&](int u, int v) -> int {
		// say h(u) >= h(v) then two cases
		// lca(u,v) is v in which case ans is just a level diff(u,v)
		// = l(u) - l(v)
		// OR
		// lca(u,v) = a ( some diff node ) then it's simply
		// level diff(u,a) + level diff(v,a)
		// = l(u) - l(a) + l(v) - l(a)
		// notice that when a = v, this too collapse to first case
		// so can just use result from case 2
		return h[u] + h[v] - 2 * h[lca(u, v)];
	};

	// INFO: what is special about the lca here?
	// it's the common parent from which we can use some info
	// it decomposes the dfs direction into two parts cleanly

	while (q--) {
		int u, v;
		cin >> u >> v;
		cout << dist(u, v) << "\n";
	}

#undef int
}
```

## Distance Queries (Centroid Decomposition)

```cpp
// problem: fast (u,v) distance queries
// tag: centroid decomp

#include <bits/stdc++.h>
using namespace std;

int main() {
	// finally needed to put these in for this problem
	cin.tie(nullptr);
	ios_base::sync_with_stdio(false);

#define int long long
	int n, q;
	cin >> n >> q;
	vector<vector<int>> g(n + 1);

	for (int i = 0; i < n - 1; i++) {
		int u, v;
		cin >> u >> v;
		g[u].push_back(v);
		g[v].push_back(u);
	}

	vector<int> sz(n + 1), removed(n + 1), cd_par(n + 1), cd_depth(n + 1);
	// centroid_dist ( not cd_dist as it's not centroid decomposition dist )
	vector<vector<int>> c_dist(n + 1);

	auto fsz = [&](auto &&f, int u, int par) -> int {
		sz[u] = 1;
		for (int v : g[u]) {
			if (v == par || removed[v])
				continue;
			sz[u] += f(f, v, u);
		}
		return sz[u];
	};

	auto fcentroid = [&](auto &&f, int u, int par, int tot) -> int {
		for (int v : g[u]) {
			if (v == par || removed[v])
				continue;
			if (sz[v] > tot / 2)
				return f(f, v, u, tot);
		}
		return u;
	};

	auto fdist = [&](auto &&f, int u, int par, int d) -> void {
		// for each node in the component with the centroid, centroid
		// starts as root and we fill in a dist
		// note that for same node, this dfs will never push twice
		c_dist[u].push_back(d);
		for (int v : g[u]) {
			if (v == par || removed[v])
				continue;
			f(f, v, u, d + 1);
		}
	};

	auto fcd = [&](auto &&f, int u, int par) -> void {
		// note that par IS 0 as these are just individual trees and
		// meant to be treated as such
		int tot = fsz(fsz, u, 0);
		int c = fcentroid(fcentroid, u, 0, tot);

		// USE the centroid to fill info, note that you CANNOT remove
		// it yet
		fdist(fdist, c, 0, 0);
		if (par) {
			cd_depth[c] = cd_depth[par] + 1;
			cd_par[c] = par;
		}

		// now remove
		removed[c] = 1;

		for (int v : g[c]) {
			// this v == par is redundant as parent must be SOME centroid
			// and MUST have been removed in the prev iteration
			if (v == par || removed[v])
				continue;
			f(f, v, c);
		}
	};
	fcd(fcd, 1, 0);

	vector<int> seen(n + 1);
	int ctr = 0;
	auto dist = [&](int u, int v) -> int {
		// the idea is that you do ramp trick here for seen
		// and find the lowest centroid ancestor ( cca )
		// ^ is the centroid that split it into two components ( so u,v split to
		// siblinds trees now ). so if you decompose the path alon that, and you
		// have distances in both, you can sum them up

		++ctr;
		for (int x = u; x; x = cd_par[x]) {
			seen[x] = ctr;
		}

		// from v go up till you hit seen
		for (int x = v; x; x = cd_par[x]) {
			if (seen[x] == ctr) {
				// hit a seen
				// note that for the cd tree, root is the first elem in cd dist
				// then for the node, next is dist to whatever is NEXT centroid
				// in the child tree and so on, so dist(u) => {c0, c1, c2...}
				// where ci is the ith node as you move from root to the current
				// node IN the cd tree. to summarise for each original node u,
				// dist_to_cd[u] stores distances to the centroid ancestors of
				// u, ordered by centroid depth:
				//
				// now ^ isn't self evident, after all, the depth DOES not
				// depent on u, where we started from, even though we are
				// checking u's dist array. Depth in cd tree would be the entry
				// in cd_dist(u). This is not obvious why -- but it's due to the
				// fill
				//
				// this of it as, x MUST be a a centroid ancestor, that is by
				// contruction here if this is then at dep 2 in the cd tree,
				// then at dep 1, and at dep 0, we also had a centroid ancestor,
				// and they TOO must've pushed a dist value corresponding to
				// them so this cd_depth is VERY much rooted into x being an
				// ancestor in cd tree
				int ans = c_dist[u][cd_depth[x]] + c_dist[v][cd_depth[x]];
				return ans;
			}
		}

		return -1ll;
	};

	while (q--) {
		int u, v;
		cin >> u >> v;
		cout << dist(u, v) << "\n";
	}

#undef int
}
```

## Subordinates

```cpp
// problem: subtree size for each node

#include <bits/stdc++.h>
using namespace std;

int main() {
	int n;
	cin >> n;
	vector<vector<int>> g(n + 1);
	for (int i = 2; i <= n; i++) {
		int v;
		cin >> v;
		// boss is v
		g[v].push_back(i);
	}

	vector<int> sizes(n + 1);
	auto f = [&](auto &&f, int u) -> int {
		auto &sz = sizes[u];
		for (int v : g[u])
			sz += f(f, v);
		return ++sz;
	};
	f(f, 1);

	for (int i = 1; i <= n; i++)
		cout << sizes[i] - 1 << " ";
	cout << "\n";
}
```

## Tree Diameter

```cpp
// problem: max distance bw two nodes
// once more a postorder dp with global optim

#include <bits/stdc++.h>
using namespace std;

int main() {
	int n;
	cin >> n;
	vector<vector<int>> g(n + 1);
	for (int i = 0; i < n - 1; i++) {
		int u, v;
		cin >> u >> v;
		g[u].push_back(v);
		g[v].push_back(u);
	}

	// there is the usual graph algorithm but for a tree I can do
	// I can do the usual postorder dp where I optimise a global
	// max and return localised best dp states

	int ans = 0;
	auto f = [&](auto &&f, int u, int par) -> int {
		array<int, 2> top2{};
		for (int v : g[u]) {
			if (v == par)
				continue;
			int cur = f(f, v, u);
			if (cur >= top2[0]) {
				top2[1] = top2[0];
				top2[0] = cur;
			} else if (cur > top2[1]) {
				top2[1] = cur;
			}
		}
		ans = max(ans, top2[0] + top2[1] + 1);
		return 1 + top2[0];
	};
	f(f, 1, -1);

	// I calc dist as nodes count
	cout << ans - 1 << "\n";
}
```

## Tree Distances 1

```cpp
// problem: for each node the max distance to some other node
// tag: edge message dp

#include <bits/stdc++.h>
using namespace std;

int main() {
	int n;
	cin >> n;
	vector<vector<int>> g(n + 1);
	for (int i = 0; i < n - 1; i++) {
		int u, v;
		cin >> u >> v;
		g[u].push_back(v);
		g[v].push_back(u);
	}

	struct top2 {
		array<int, 2> tag{};
		array<int, 2> arr{};
		void add(int key, int val) {
			if (val >= arr[0]) {
				arr[1] = arr[0];
				arr[0] = val;
				tag[1] = tag[0];
				tag[0] = key;
			} else if (val > arr[1]) {
				arr[1] = val;
				tag[1] = key;
			}
		}
		array<int, 2> best() { return {tag[0], arr[0]}; }
		array<int, 2> other(int key) {
			if (key == tag[0])
				return {tag[1], arr[1]};
			return best();
		}
	};

	// now for split on u-v edge, we need up and down
	// now up is fine but down needs to be NOT across the u-v cut that
	// we are making
	vector<int> up(n + 1);
	vector<top2> down(n + 1);

	// if you fill these we can have a final MERGE step
	// this fills msg(u -> par(u))
	auto downf = [&](auto &&f, int u, int par) -> int {
		// by dfs this partition parition would be seprate
		// from parent
		auto &d = down[u];
		for (int v : g[u]) {
			if (v == par)
				continue;
			// you can think of this as the sep even
			// because re-root / messages go in both directions
			d.add(v, 1 + f(f, v, u));
			// READ AS: for u, branch v, produced this value
		}
		return d.best()[1];
	};
	downf(downf, 1, -1);

	// this'll fill msg( u <- par(u) )
	auto upf = [&](auto &&f, int u, int par) -> void {
		if (par != -1) {
			up[u] = 1 + max(up[par], down[par].other(u)[1]);
		}
		for (int v : g[u])
			if (v != par)
				f(f, v, u);
	};
	upf(upf, 1, -1);

	// MERGE, you can think of this as the "re"-root as for a node
	// I consider ALL edges similar to the root case ( par as -1 )
	for (int u = 1; u <= n; u++) {
		cout << max(up[u], down[u].best()[1]) << " ";
	}
	cout << "\n";
}
```

## Tree Distances 2

```cpp
// problem: for each node the sum distance to all others node
// tag: edge message dp

#include <bits/stdc++.h>
using namespace std;

int main() {
#define int long long
	int n;
	cin >> n;
	vector<vector<int>> g(n + 1);
	for (int i = 0; i < n - 1; i++) {
		int u, v;
		cin >> u >> v;
		g[u].push_back(v);
		g[v].push_back(u);
	}

	vector<int> sz(n + 1);
	int ans1 = 0; // for 1 as root
	auto f = [&](auto &&f, int u, int par, int d) -> int {
		ans1 += d;
		auto &a = sz[u] = 1;
		for (int v : g[u])
			if (v != par)
				a += f(f, v, u, d + 1);
		return a;
	};

	f(f, 1, -1, 0);

	vector<int> ans(n + 1);
	ans[1] = ans1;

	// I need to fill it in dfs order
	auto f2 = [&](auto &&f, int u, int par) -> void {
		if (par != -1) {
			ans[u] = ans[par] + n - 2 * sz[u];
		}
		for (int v : g[u])
			if (v != par)
				f(f, v, u);
	};
	f2(f2, 1, -1);

	for (int i = 1; i <= n; i++)
		cout << ans[i] << " ";
	cout << "\n";
#undef int
}
```

## Tree Matching

```cpp
// problem: pick max edges where each node is only on ONE edge
// usual postorder dp

#include <bits/stdc++.h>
using namespace std;

int main() {
	int n;
	cin >> n;
	vector<vector<int>> g(n + 1);
	for (int i = 0; i < n - 1; i++) {
		int u, v;
		cin >> u >> v;
		g[u].push_back(v);
		g[v].push_back(u);
	}

	// f(u,1) => I include an edge from u to u.c
	// f(u,0) => I don't do that
	const int INF = (int)1e9+5;

	auto f = [&](auto &&f, int u, int par) -> array<int,2> {
		array<int,2> ret{};

		vector<array<int,2>> cs;
		for(int v:g[u]){
			if(v==par) continue;
			cs.push_back(f(f,v,u));
		}

		// 0
		for(auto &c:cs){
			ret[0] += max(c[0],c[1]);
		}
		// 1
		int best = -INF; // leaf case
		for(auto& c:cs){
			int tans = ret[0] - max(c[0],c[1]) + c[0];
			best = max(best, tans);
		}
		ret[1] = best == -INF? best : best+1;

		return ret;
	};

	auto ans = f(f,1,-1);
	cout<<max(ans[0],ans[1])<<"\n";
}
```
