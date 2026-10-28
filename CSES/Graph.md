---
title: CSES Graph Problems
date: 19Jul26
---

# CSES Graph Problems

## Graphs

Aim here is to implement whatever multiple approaches and use this as reference for programming style for future.

### Counting Rooms - components in 2d grid dfs

Note the lambda dfs.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;

    vector<string> v(n);
    for (auto& i : v) cin >> i;

    auto dfs = [&](int i, int j, auto&& dfs) {
        if (i < 0 || j < 0 || i >= n || j >= m || v[i][j] == '#') return;
        v[i][j] = '#';  // reusing
        dfs(i + 1, j, dfs);
        dfs(i - 1, j, dfs);
        dfs(i, j + 1, dfs);
        dfs(i, j - 1, dfs);
    };

    int cnt = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (v[i][j] == '.') {
                dfs(i, j, dfs);
                cnt++;
            }
        }
    }

    cout << cnt;

    return 0;
}
```

### Labyrinth - 2d grid bfs path

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;

    vector<string> v(n);
    for (auto& i : v) cin >> i;

    int sx = -1, sy = -1, ex = -1, ey = -1;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (v[i][j] == 'A') {
                sx = i;
                sy = j;
            }
            if (v[i][j] == 'B') {
                ex = i;
                ey = j;
            }
        }
    }

    vector<vector<pair<int, int>>> par(n, vector<pair<int, int>>(m, {-1, -1}));
    vector<vector<int>> dist(n, vector<int>(m, INF));
    queue<pair<int, int>> q;
    q.push({sx, sy});
    dist[sx][sy] = 0;

    vector<int> dx = {0, 0, 1, -1};
    vector<int> dy = {1, -1, 0, 0};

    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();

        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if (nx < 0 || nx >= n || ny < 0 || ny >= m || v[nx][ny] == '#') continue;
            if (dist[nx][ny] != INF) continue;

            par[nx][ny] = {x, y};
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }

    if (dist[ex][ey] == INF) {
        cout << "NO\n";
    } else {
        cout << "YES\n";
        cout << dist[ex][ey] << "\n";

        string ans = "";
        while (ex != sx || ey != sy) {
            auto [px, py] = par[ex][ey];
            if (px == ex) {
                if (py < ey)
                    ans += 'R';
                else
                    ans += 'L';
            } else {
                if (px < ex)
                    ans += 'D';
                else
                    ans += 'U';
            }
            ex = px;
            ey = py;
        }
        reverse(ans.begin(), ans.end());
        cout << ans << "\n";
    }

    return 0;
}
```

### Building Roads - min edges to make connected

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];
vector<int> vis(N);

int dfs(int u) {
    vis[u] = 1;
    for (auto v : g[u]) {
        if (!vis[v]) dfs(v);
    }
    // return the first elem of component
    return u;
}

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> elems;
    for (int i = 1; i <= n; i++) {
        if (!vis[i]) elems.push_back(dfs(i));
    }

    cout << elems.size() - 1 << "\n";
    for (int i = 0; i < (int)elems.size() - 1; i++) {
        cout << elems[i] << " " << elems[i + 1] << "\n";
    }

    return 0;
}
```

### Message Route - bfs with path

path printing ref

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];
const int INF = 1e18;

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> par(n + 1, -1);
    vector<int> dist(n + 1, INF);
    queue<int> q;
    q.push(1);
    dist[1] = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (auto v : g[u]) {
            if (dist[v] != INF) continue;

            par[v] = u;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }

    if (dist[n] == INF)
        cout << "IMPOSSIBLE\n";
    else {
        vector<int> path;

        int cur = n;
        while (cur != -1) {
            path.push_back(cur);
            cur = par[cur];
        }

        reverse(path.begin(), path.end());

        cout << path.size() << "\n";
        for (auto u : path) cout << u << " ";
        cout << "\n";
    }

    return 0;
}
```

### Building Teams - bipartite

See, bipartite is based on cycle detection

[Cycle Detection](https://app.notion.com/p/Cycle-Detection-703fb44a291b409ab93faee5039abdc3?pvs=21)

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int N = (int)1e5 + 5;
vector<int> g[N];
int n, m;
vector<int> color(N, -1);

bool dfs(int u) {
    for (auto v : g[u]) {
        if (color[v] == -1) {
            color[v] = 1 - color[u];
            if (!dfs(v)) return false;
        } else if (color[v] == color[u])
            return false;
    }
    return true;
}

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    for (int i = 1; i <= n; i++) {
        if (color[i] == -1) {
            color[i] = 0;
            if (!dfs(i)) {
                cout << "IMPOSSIBLE\n";
                return 0;
            }
        }
    }

    for (int i = 1; i <= n; i++) cout << color[i] + 1 << " ";

    return 0;
}
```

### Rount Trip - undirected graph cycle path

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];
int vis[N], par[N];
int cs = -1, ce = -1;

bool dfs(int u) {
    vis[u] = 1;
    for (int v : g[u]) {
        if (!vis[v]) {
            par[v] = u;
            if (dfs(v)) return true;
        } else if (v != par[u]) {
            cs = v;
            ce = u;
            return true;
        }
    }
    return false;
}

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    for (int i = 1; i <= n; i++)
        if (!vis[i] && dfs(i)) break;

    if (cs == -1)
        cout << "IMPOSSIBLE\n";
    else {
        vector<int> path;

        int cur = ce;
        while (cur != cs) {
            path.push_back(cur);
            cur = par[cur];
        }
        path.push_back(cs);
        reverse(path.begin(), path.end());
        path.push_back(cs);

        cout << path.size() << "\n";
        for (int x : path) cout << x << " ";
    }

    return 0;
}
```

### Monsters - multi src bfs, who will reach first

lambda bfs, path gen through dist array, using -dx, -dy for reverse path to make reasoning clear

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

vector<int> dx = {0, 0, 1, -1};
vector<int> dy = {1, -1, 0, 0};

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<string> v(n);
    for (auto& i : v) cin >> i;

    auto bfs = [&](vector<pair<int, int>> srcs) {
        queue<pair<int, int>> q;
        vector<vector<int>> dist(n, vector<int>(m, INF));

        for (auto [sx, sy] : srcs) q.push({sx, sy}), dist[sx][sy] = 0;

        while (!q.empty()) {
            auto [x, y] = q.front();
            q.pop();

            for (int i = 0; i < 4; i++) {
                int nx = x + dx[i], ny = y + dy[i];
                if (nx < 0 || nx >= n || ny < 0 || ny >= m || v[nx][ny] == '#') continue;

                if (dist[nx][ny] == INF) {
                    dist[nx][ny] = dist[x][y] + 1;
                    q.push({nx, ny});
                }
            }
        }

        return dist;
    };

    vector<pair<int, int>> player, monsters;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (v[i][j] == 'A')
                player.push_back({i, j});
            else if (v[i][j] == 'M')
                monsters.push_back({i, j});
        }
    }

    auto dist_player = bfs(player);
    auto dist_monsters = bfs(monsters);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (i == 0 || i == n - 1 || j == 0 || j == m - 1) {
                if (dist_player[i][j] < dist_monsters[i][j]) {
                    cout << "YES\n";
                    cout << dist_player[i][j] << "\n";

                    string ans = "";
                    int curx = i, cury = j;
                    while (dist_player[curx][cury] != 0) {
                        for (int k = 0; k < 4; k++) {
                            int nx = curx - dx[k], ny = cury - dy[k];
                            if (nx < 0 || nx >= n || ny < 0 || ny >= m || v[nx][ny] == '#') continue;

                            if (dist_player[nx][ny] == dist_player[curx][cury] - 1) {
                                if (k == 0)
                                    ans += 'R';
                                else if (k == 1)
                                    ans += 'L';
                                else if (k == 2)
                                    ans += 'D';
                                else
                                    ans += 'U';

                                curx = nx, cury = ny;
                                break;
                            }
                        }
                    }

                    reverse(ans.begin(), ans.end());
                    cout << ans << "\n";

                    return 0;
                }
            }
        }
    }

    cout << "NO\n";

    return 0;
}
```

### Shortest Routes 1 - Djikstra (SSSP)

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<pair<int, int>> g[N];
const int INF = 1e18;

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }

    vector<int> dist(n + 5, INF);
    vector<int> par(n + 5, -1);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> q;
    q.push({0, 1});
    dist[1] = 0;

    while (!q.empty()) {
        auto [curd, u] = q.top();
        q.pop();

        if (dist[u] != curd) continue;

        for (auto [v, wt] : g[u]) {
            if (dist[u] + wt < dist[v]) {
                dist[v] = dist[u] + wt;
                q.push({dist[v], v});
                par[v] = u;
            }
        }
    }

    for (int i = 1; i <= n; i++) cout << dist[i] << " ";

    return 0;
}
```

### Shortest Routes 2 - All pairs SP

N^3logN djikstra and N^3 floyd warshall, lambda djikstra

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m, q;
const int N = 1e5 + 5;
vector<pair<int, int>> g[N];
const int INF = 1e18;

signed main() {
    fast_io;

    cin >> n >> m >> q;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }

    auto sssp = [&](int src) {
        vector<int> dist(n + 5, INF);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> q;
        q.push({0, src});
        dist[src] = 0;

        while (!q.empty()) {
            auto [curd, u] = q.top();
            q.pop();

            if (dist[u] != curd) continue;

            for (auto [v, wt] : g[u]) {
                if (dist[u] + wt < dist[v]) {
                    dist[v] = dist[u] + wt;
                    q.push({dist[v], v});
                }
            }
        }

        return dist;
    };

    vector<vector<int>> dists(n + 5);
    for (int i = 1; i <= n; i++) {
        dists[i] = sssp(i);
    }

    while (q--) {
        int u, v;
        cin >> u >> v;
        if (dists[u][v] == INF)
            cout << -1 << "\n";
        else
            cout << dists[u][v] << "\n";
    }

    return 0;
}
```

```cpp
#include <bits/stdc++.h>
using namespace std;
 
#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);
 
int n, m, q;
const int N = 1e5 + 5;
vector<pair<int, int>> g[N];
const int INF = 1e18;
 
signed main() {
    fast_io;
 
    cin >> n >> m >> q;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
 
    auto sssp = [&](int src) {
        vector<int> dist(n + 5, INF);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> q;
        q.push({0, src});
        dist[src] = 0;
 
        while (!q.empty()) {
            auto [curd, u] = q.top();
            q.pop();
 
            if (dist[u] != curd) continue;
 
            for (auto [v, wt] : g[u]) {
                if (dist[u] + wt < dist[v]) {
                    dist[v] = dist[u] + wt;
                    q.push({dist[v], v});
                }
            }
        }
 
        return dist;
    };
 
    vector<vector<int>> dists(n + 5);
    for (int i = 1; i <= n; i++) {
        dists[i] = sssp(i);
    }
 
    while (q--) {
        int u, v;
        cin >> u >> v;
        if (dists[u][v] == INF)
            cout << -1 << "\n";
        else
            cout << dists[u][v] << "\n";
    }
 
    return 0;
}
```

### High Score - Bellman Ford, negative cycle reachable from src

bellman ford then dfs from the bad nodes, ie nodes whose distance changed in the nth step. Look at the nm complexity dfs which uses edges only.



Another way would be to get the bad nodes. Adn then on the transpose graph, do a dfs from dest n. This is reachability from kind of dfs. If from any of the bad nodes, n is reachable, then -INF.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int INF = 1e18;
const int N = 2505;
vector<int> gg[N];

signed main() {
    fast_io;

    cin >> n >> m;

    vector<array<int, 3>> g(m);

    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[i] = {u, v, -w};
        gg[u].push_back(v);
    }

    vector<int> dist(n + 1, INF);
    dist[1] = 0;

    vector<int> cycle;
    for (int i = 0; i < n; i++) {
        bool any = false;
        for (auto [a, b, wt] : g) {
            if (dist[a] != INF) {
                if (dist[b] > dist[a] + wt) {
                    dist[b] = dist[a] + wt;

                    if (i == n - 1) {
                        cycle.push_back(b);
                    }

                    any = true;
                }
            }
        }

        if (!any) break;
    }

    auto dfs = [&](int u, auto&& dfs) -> void {
        dist[u] = -INF;
        for (int v : gg[u]) {
            if (dist[v] == -INF) continue;
            dfs(v, dfs);
        }
    };

    for (int x : cycle) {
        if (dist[x] != -INF) dfs(x, dfs);
    }

    if (dist[n] == -INF) {
        cout << -1;
    } else {
        cout << -dist[n];
    }

    return 0;
}
```

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int INF = 1e18;

signed main() {
    fast_io;

    cin >> n >> m;

    vector<array<int, 3>> g(m);

    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[i] = {u, v, -w};
    }

    vector<int> dist(n + 1, INF);
    dist[1] = 0;

    for (int i = 0; i < n; i++) {
        bool any = false;
        for (auto [a, b, wt] : g) {
            if (dist[a] != INF) {
                if (dist[b] > dist[a] + wt) {
                    dist[b] = dist[a] + wt;

                    if (i == n - 1) {
                        dist[b] = -INF;
                    }

                    any = true;
                }
            }
        }

        if (!any) break;
    }

    for (int i = 0; i < n; i++) {
        for (auto [u, v, wt] : g) {
            if (dist[u] == -INF) dist[v] = -INF;
        }
    }

    if (dist[n] == -INF) {
        cout << -1;
    } else {
        cout << -dist[n];
    }

    return 0;
}
```

### Flight Discount - Djikstra additional state

Just add more states after dist and use it like a dp



Another way would be to interate over the edge where discount is applied then do ans=min over d(st,a) + wt/2 + d(b,en)

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int N = 1e5 + 5;
vector<pair<int, int>> g[N];
const int INF = 1e18;

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }

    vector<vector<int>> dist(n + 1, vector<int>(2, INF));
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> q;
    dist[1][0] = 0;
    q.push({0, 0, 1});

    while (!q.empty()) {
        auto [curd, used, u] = q.top();
        q.pop();

        if (curd != dist[u][used]) continue;

        for (auto [v, wt] : g[u]) {
            // dont use discount, used remains as it was
            if (dist[u][used] + wt < dist[v][used]) {
                dist[v][used] = dist[u][used] + wt;
                q.push({dist[v][used], used, v});
            }

            // use if possible
            if (!used) {
                if (dist[u][0] + wt / 2 < dist[v][1]) {
                    dist[v][1] = dist[u][0] + wt / 2;
                    q.push({dist[v][1], 1, v});
                }
            }
        }
    }

    cout << dist[n][1];

    return 0;
}
```

### Cycle Finding - Bellman Ford, any negative cycle

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<array<int, 3>> edges;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.push_back({u, v, w});
    }

    vector<int> dist(n + 1, 0);
    vector<int> par(n + 1, -1);

    int neg = -1;
    for (int i = 0; i < n; i++) {
        neg = -1;
        for (auto [u, v, w] : edges) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                par[v] = u;

                if (i == n - 1) neg = v;
            }
        }
    }

    if (neg == -1) {
        cout << "NO\n";
    } else {
        cout << "YES\n";
        for (int i = 0; i < n; i++) neg = par[neg];

        vector<int> cycle;
        int cur = neg;
        while (cur != neg || cycle.empty()) {
            cycle.push_back(cur);
            cur = par[cur];
        }
        cycle.push_back(neg);
        reverse(cycle.begin(), cycle.end());

        for (auto x : cycle) cout << x << " ";
        cout << "\n";
    }

    return 0;
}
```

### Flight Routes - Djikstra additional state, k shortest paths

Add another dimension to dist i.e. all the k shortest paths instead of just the shortest. Also note the nv calc, now it is using curd not dist[u] as what rank dist is curd is not known. Similar for continue condition.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m, k;
const int N = 1e5 + 5;
vector<pair<int, int>> g[N];
const int INF = 1e18;

signed main() {
    fast_io;

    cin >> n >> m >> k;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }

    vector<priority_queue<int>> dist(n + 1);
    priority_queue<array<int, 2>, vector<array<int, 2>>, greater<>> q;
    q.push({0, 1});
    dist[1].push(0);

    while (!q.empty()) {
        auto [curd, u] = q.top();
        q.pop();

        if (curd > dist[u].top()) continue;

        for (auto [v, wt] : g[u]) {
            int nv = curd + wt;
            if ((int)dist[v].size() < k) {
                dist[v].push(nv);
                q.push({nv, v});
            } else if (nv < dist[v].top()) {
                dist[v].pop();
                dist[v].push(nv);
                q.push({nv, v});
            }
        }
    }

    vector<int> ans;
    while (!dist[n].empty()) {
        ans.push_back(dist[n].top());
        dist[n].pop();
    }
    reverse(ans.begin(), ans.end());

    for (int x : ans) cout << x << " ";

    return 0;
}
```

### Rount Trip 2 - Directed graph cycle path

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
    }

    vector<int> vis(n + 1, 0);
    vector<int> par(n + 1, -1);

    int start = -1, end = -1;
    auto dfs = [&](int u, auto&& dfs) -> bool {
        vis[u] = 1;
        for (int v : g[u]) {
            if (!vis[v]) {
                par[v] = u;
                if (dfs(v, dfs)) return true;
            } else if (vis[v] == 1) {
                start = v;
                end = u;
                return true;
            }
        }
        vis[u] = 2;
        return false;
    };

    for (int i = 1; i <= n; i++) {
        if (!vis[i] && dfs(i, dfs)) break;
    }

    if (start == -1) {
        cout << "IMPOSSIBLE\n";
    } else {
        vector<int> path;

        int cur = end;
        while (cur != start) {
            path.push_back(cur);
            cur = par[cur];
        }
        path.push_back(start);
        reverse(path.begin(), path.end());
        path.push_back(start);

        cout << path.size() << "\n";
        for (int x : path) cout << x << " ";
    }

    return 0;
}
```

### Course Schedule - Topo sort

Note that the indeg method for topo sort is actually more useful as it can be modified for a wider range of problems. The dfs method is easier to implement though.

There is no real outdegree based method though. When going by outdegree=0, you have to use the transpose graph and reverse the ans so in reality it is indegree=0 method on the transpose graph and using that reverse of topo sort is the topo sort of transpose graph.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];
vector<int> indeg(N);

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        indeg[v]++;
    };

    vector<int> q;
    for (int i = 1; i <= n; i++) {
        if (indeg[i] == 0) {
            q.push_back(i);
        }
    }

    vector<int> topo;
    while (!q.empty()) {
        int u = q.back();
        q.pop_back();
        topo.push_back(u);

        for (int v : g[u]) {
            indeg[v]--;
            if (indeg[v] == 0) {
                q.push_back(v);
            }
        }
    }

    if ((int)topo.size() != n) {
        cout << "IMPOSSIBLE\n";
    } else {
        for (int i : topo) cout << i << " ";
    }

    return 0;
}
```

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];
vector<int> topo;
vector<int> vis(N);
bool ok = true;

void dfs(int u) {
    vis[u] = 1;
    for (int v : g[u]) {
        if (!vis[v]) {
            dfs(v);
        } else if (vis[v] == 1) {
            ok = false;
        }
    }
    vis[u] = 2;
    topo.push_back(u);
}

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
    };

    for (int i = 1; i <= n && ok; i++) {
        if (!vis[i]) dfs(i);
    }

    if (!ok) {
        cout << "IMPOSSIBLE\n";
    } else {
        reverse(topo.begin(), topo.end());
        for (int i : topo) cout << i << " ";
    }

    return 0;
}
```

### Game Routes - Dp on Dag, count ways to reach

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int mod = 1e9 + 7;

int n, m;
const int N = 1e5 + 5;
vector<int> g[N];
int dp[N], vis[N];
vector<int> topo;

void dfs(int u) {
    vis[u] = 1;
    for (int v : g[u])
        if (!vis[v]) dfs(v);
    topo.push_back(u);
}

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
    }

    for (int i = 1; i <= n; i++)
        if (!vis[i]) dfs(i);
    reverse(topo.begin(), topo.end());

    dp[1] = 1;
    for (int u : topo)
        for (int v : g[u]) (dp[v] += dp[u]) %= mod;

    cout << dp[n];

    return 0;
}
```

### Investigation - Djikstra additional state (similar to par array)

Note that often, the state can just reside in the dist itself. You only need it in priority queue when that state differentiates the distance. Flight discount had different distances for whether coupon used or not. For the k shortest paths problem, we cleverly skipped it. Here, the only path is the shortest path, that’s all, its just we are having additional meta data associated to each path instead of just the distance. Think of this as the par array. But now we have more data.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;
vector<pair<int, int>> g[N];
const int INF = 1e18;
const int MOD = 1e9 + 7;

signed main() {
    fast_io;

    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }

    // state : {dist, cnt, min len, max len,  u}
    vector<array<int, 5>> dist(n + 5, {INF, -1, -1, -1, -1});
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> q;
    q.push({0, 1});
    dist[1] = {0, 1, 0, 0, 1};

    while (!q.empty()) {
        auto [curd, u] = q.top();
        q.pop();

        if (dist[u][0] != curd) continue;

        for (auto [v, wt] : g[u]) {
            if (curd + wt < dist[v][0]) {
                dist[v] = {curd + wt, dist[u][1], dist[u][2] + 1, dist[u][3] + 1, v};
                q.push({dist[v][0], v});
            } else if (curd + wt == dist[v][0]) {
                (dist[v][1] += dist[u][1]) %= MOD;
                dist[v][2] = min(dist[v][2], dist[u][2] + 1);
                dist[v][3] = max(dist[v][3], dist[u][3] + 1);
            }
        }
    }

    for (int i = 0; i < 4; i++) cout << dist[n][i] << " ";

    return 0;
}
```

### Planet queries 1 - Functional graph, kth successor

Wierd tle issue here where 2d vector was causing tle but not 2d array.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int D = 32;
const int N = 2e5 + 5;
int to[N][D];

signed main() {
    fast_io;

    int n, q;
    cin >> n >> q;

    for (int i = 1; i <= n; ++i) cin >> to[i][0];

    for (int d = 1; d < D; d++) {
        for (int i = 1; i <= n; i++) {
            to[i][d] = to[to[i][d - 1]][d - 1];
        }
    }

    while (q--) {
        int x, k;
        cin >> x >> k;

        int cur = x;
        for (int i = 0; i < D; i++) {
            if ((k >> i) & 1) {
                cur = to[cur][i];
            }
        }

        cout << cur << "\n";
    }

    return 0;
}
```

### Planet queries 2 - Functional graph decomposition, distance queries

A very generalised approach for solving almost anything related to functional graphs. You get so much info from the stuff implemented in this.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, q;
const int N = 2e5 + 5;
const int D = 32;
int g[N];
int up[N][D];
int vis[N], cyc_node[N], depth[N], in_cycle[N], group[N];
int dist[N];
map<int, int> cyc_len;

bool dfs_in_tree = true;
void dfs(int u) {
    vis[u] = 1;

    int v = g[u];

    if (!vis[v]) {
        dfs(v);
    } else if (vis[v] == 1) {
        group[v] = v;
        in_cycle[v] = 1;
        dfs_in_tree = false;
    } else {
        assert(group[v]);
    }

    vis[u] = 2;
    group[u] = group[v];

    in_cycle[u] = !dfs_in_tree;

    if (!in_cycle[u]) {
        depth[u] = depth[v] + 1;
        cyc_node[u] = cyc_node[v];
    } else {
        cyc_node[u] = u;
        depth[u] = 0;
    }

    if (group[u] == u) {
        dfs_in_tree = true;
    }
}

signed main() {
    fast_io;

    cin >> n >> q;
    for (int i = 1; i <= n; i++) {
        cin >> g[i];
        up[i][0] = g[i];
    }

    // binary lifting
    for (int j = 1; j < D; j++) {
        for (int i = 1; i <= n; i++) {
            up[i][j] = up[up[i][j - 1]][j - 1];
        }
    }

    // find cycle groups
    for (int i = 1; i <= n; i++) {
        if (!vis[i]) {
            dfs_in_tree = true;
            dfs(i);
        }
    }

    // set cycle distance
    memset(dist, -1, sizeof(dist));
    for (int i = 1; i <= n; i++) {
        if (dist[i] == -1 && in_cycle[i]) {
            int cur = i;
            dist[cur] = 0;
            while (dist[g[cur]] == -1) {
                dist[g[cur]] = dist[cur] + 1;
                cur = g[cur];
            }
            cyc_len[group[i]] = dist[cur] + 1;
        }
    }

    auto goup = [&](int u, int k) {
        for (int i = 0; i < D; i++) {
            if (k & (1 << i)) {
                u = up[u][i];
            }
        }
        return u;
    };

    auto cycle_dist = [&](int a, int b) {
        int diff = dist[b] - dist[a];
        if (diff >= 0) return diff;

        return cyc_len[group[a]] + diff;
    };

    while (q--) {
        int a, b;
        cin >> a >> b;

        if (group[a] != group[b]) {
            cout << "-1\n";
        } else if (in_cycle[a]) {
            if (in_cycle[b]) {
                cout << cycle_dist(a, b) << "\n";
            } else {
                cout << "-1\n";
            }
        } else {
            if (in_cycle[b]) {
                int ans = depth[a];
                ans += cycle_dist(cyc_node[a], b);
                cout << ans << "\n";
            } else {
                if (depth[b] > depth[a] || goup(a, depth[a] - depth[b]) != b) {
                    cout << "-1\n";
                } else {
                    cout << depth[a] - depth[b] << "\n";
                }
            }
        }
    }

    return 0;
}
```

### Planet cycles - Functional graph decomposition,

Simpler solutions may be possible but function graph decomposition is the one hit answer for everything functional graph.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n;
const int N = 2e5 + 5;
const int D = 32;
int g[N];
int up[N][D];
int vis[N], depth[N], in_cycle[N], group[N];
int dist[N];
map<int, int> cyc_len;

bool dfs_in_tree = true;
void dfs(int u) {
    vis[u] = 1;

    int v = g[u];

    if (!vis[v]) {
        dfs(v);
    } else if (vis[v] == 1) {
        group[v] = v;
        in_cycle[v] = 1;
        dfs_in_tree = false;
    } else {
        assert(group[v]);
    }

    vis[u] = 2;
    group[u] = group[v];

    in_cycle[u] = !dfs_in_tree;

    if (!in_cycle[u]) {
        depth[u] = depth[v] + 1;
    } else {
        depth[u] = 0;
    }

    if (group[u] == u) {
        dfs_in_tree = true;
    }
}

signed main() {
    fast_io;

    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> g[i];
        up[i][0] = g[i];
    }

    // find cycle groups
    for (int i = 1; i <= n; i++) {
        if (!vis[i]) {
            dfs_in_tree = true;
            dfs(i);
        }
    }

    // set cycle distance
    memset(dist, -1, sizeof(dist));
    for (int i = 1; i <= n; i++) {
        if (dist[i] == -1 && in_cycle[i]) {
            int cur = i;
            dist[cur] = 0;
            while (dist[g[cur]] == -1) {
                dist[g[cur]] = dist[cur] + 1;
                cur = g[cur];
            }
            cyc_len[group[i]] = dist[cur] + 1;
        }
    }

    for (int i = 1; i <= n; i++) {
        int ans = depth[i] + cyc_len[group[i]];
        cout << ans << " ";
    }

    return 0;
}
```

### Road Reparation - MST

Could also have done an edge count added == n-1

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;

vector<int> par(N, -1);
int root(int u) { return par[u] < 0 ? u : par[u] = root(par[u]); }
void merge(int u, int v) {
    if ((u = root(u)) == (v = root(v))) return;
    if (-par[u] < -par[v]) swap(u, v);
    par[u] += par[v];
    par[v] = u;
}

signed main() {
    fast_io;

    cin >> n >> m;
    vector<array<int, 3>> edges(m);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.push_back({w, u, v});
    }

    sort(edges.begin(), edges.end());

    int cost = 0;
    for (auto [wt, u, v] : edges) {
        if (root(u) != root(v)) {
            merge(u, v);
            cost += wt;
        }
    }

    if (-par[root(1)] == n)
        cout << cost << endl;
    else
        cout << "IMPOSSIBLE" << endl;

    return 0;
}
```



### Road Constructions - dsu on graph, connectivity on edge adding

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

int n, m;
const int N = 1e5 + 5;

vector<int> par(N, -1);
int root(int u) { return par[u] < 0 ? u : par[u] = root(par[u]); }
void merge(int u, int v) {
    if ((u = root(u)) == (v = root(v))) return;
    if (-par[u] < -par[v]) swap(u, v);
    par[u] += par[v];
    par[v] = u;
}

signed main() {
    fast_io;

    cin >> n >> m;
    vector<array<int, 2>> edges;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        edges.push_back({u, v});
    }

    vector<array<int, 2>> ans;

    int cnt = n, mx_size = 1;
    for (auto [u, v] : edges) {
        if ((u = root(u)) != (v = root(v))) {
            merge(u, v);
            cnt--;
            mx_size = max(mx_size, -par[root(u)]);
        }

        ans.push_back({cnt, mx_size});
    }

    for (auto [u, v] : ans) cout << u << " " << v << "\n";

    return 0;
}
```

### Flight routes check - check strong connectivity

If undirected then all being in same component is enough. Things get a little trickier if its a directed graph though.

One solution is to use the fact that if it is all connected, then from any abitrary vertex src, you can reach any other vertex and from any other vertex you can reach src. If both these are true, then path between any other vertex u,v can be u → src → v. So for this do a can reach and can reach from dfs. Note the reach src from any dfs which uses the transpose graph.



Another solution is to know that the problem is just asking u to check strong connectivity on entire graph. So apply kosaraju and get 1 strongly connected component.



Also note the explicit declaration of lambda type to avoid having &&dfs.



Note that the topo is not exactly “topo” in the sense that we do the same thing even if cycles are present. Here we don’t care about cycles.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1), gt(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        gt[v].push_back(u);
    }

    vector<int> topo;
    vector<int> vis(n + 1, 0);

    function<void(int)> dfs = [&](int u) {
        vis[u] = 1;
        for (int v : g[u]) {
            if (!vis[v]) dfs(v);
        }
        topo.push_back(u);
    };

    for (int i = 1; i <= n; i++)
        if (!vis[i]) dfs(i);

    reverse(topo.begin(), topo.end());

    vector<int> id(n + 1, 0);
    int cnt = 0;

    function<void(int)> scc = [&](int u) {
        id[u] = cnt;
        for (int v : gt[u]) {
            if (!id[v]) scc(v);
        }
    };

    // can use id as vis array
    vector<int> nodes;
    for (int i : topo) {
        if (!id[i]) {
            cnt++;
            scc(i);
            nodes.push_back(i);
        }
    }

    if (cnt == 1) {
        cout << "YES\n";
    } else {
        cout << "NO\n";
        cout << nodes[1] << " " << nodes[0] << "\n";
    }

    return 0;
}
```

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1), gt(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        gt[v].push_back(u);
    }

    vector<int> reach_to(n + 1, 0), reach_from(n + 1, 0);

    function<void(int)> dfs = [&](int u) {
        reach_to[u] = 1;
        for (int v : g[u]) {
            if (!reach_to[v]) dfs(v);
        }
    };

    function<void(int)> dfs2 = [&](int u) {
        reach_from[u] = 1;
        for (int v : gt[u]) {
            if (!reach_from[v]) dfs2(v);
        }
    };

    dfs(1);
    dfs2(1);

    for (int i = 1; i <= n; i++) {
        if (!reach_to[i]) {
            cout << "NO\n";
            cout << 1 << " " << i << "\n";
            return 0;
        }
        if (!reach_from[i]) {
            cout << "NO\n";
            cout << i << " " << 1 << "\n";
            return 0;
        }
    }

    cout << "YES\n";

    return 0;
}
```

### Planets and Kingdoms - scc

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1), gt(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        gt[v].push_back(u);
    }

    vector<int> topo;
    vector<int> vis(n + 1, 0);

    function<void(int)> dfs = [&](int u) {
        vis[u] = 1;
        for (int v : g[u]) {
            if (!vis[v]) dfs(v);
        }
        topo.push_back(u);
    };

    for (int i = 1; i <= n; i++)
        if (!vis[i]) dfs(i);

    reverse(topo.begin(), topo.end());

    vector<int> id(n + 1, 0);
    int cnt = 0;

    function<void(int)> scc = [&](int u) {
        id[u] = cnt;
        for (int v : gt[u]) {
            if (!id[v]) scc(v);
        }
    };

    // can use id as vis array
    vector<int> nodes;
    for (int i : topo) {
        if (!id[i]) {
            cnt++;
            scc(i);
            nodes.push_back(i);
        }
    }

    if (cnt == 1) {
        cout << "YES\n";
    } else {
        cout << "NO\n";
        cout << nodes[1] << " " << nodes[0] << "\n";
    }

    return 0;
}
```

### Giant Pizza - 2 sat

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int N = 2e5 + 5;
vector<int> g[N], gt[N];

signed main() {
    fast_io;

    int clauses, vars;
    cin >> clauses >> vars;

    function<void(int, bool, int, bool)> add_clause = [&](int a, bool a_neg, int b, bool b_neg) {
        // idea is that a would be at index 2*a and !a at 2*a+1
        a = 2 * a ^ a_neg;
        b = 2 * b ^ b_neg;
        int neg_a = a ^ 1;
        int neg_b = b ^ 1;

        g[neg_a].push_back(b);
        g[neg_b].push_back(a);
        gt[b].push_back(neg_a);
        gt[a].push_back(neg_b);
    };

    for (int i = 0; i < clauses; i++) {
        char a_sign, b_sign;
        int a, b;
        cin >> a_sign >> a >> b_sign >> b;
        bool a_neg = (a_sign == '-');
        bool b_neg = (b_sign == '-');

        add_clause(a, a_neg, b, b_neg);
    }

    int n = 2 * vars + 1;

    vector<int> topo;
    vector<int> vis(n + 1, 0);

    function<void(int)> dfs_topo = [&](int u) {
        vis[u] = 1;
        for (int v : g[u])
            if (!vis[v]) dfs_topo(v);
        topo.push_back(u);
    };

    for (int i = 1; i <= n; i++) {
        if (!vis[i]) dfs_topo(i);
    }

    reverse(topo.begin(), topo.end());

    vector<int> comp(n + 1, 0);
    int comp_count = 0;

    function<void(int)> dfs_scc = [&](int u) {
        comp[u] = comp_count;
        for (int v : gt[u])
            if (!comp[v]) dfs_scc(v);
    };

    for (int u : topo) {
        if (!comp[u]) {
            comp_count++;
            dfs_scc(u);
        }
    }

    vector<int> ans(vars + 1);
    for (int i = 2; i <= n; i += 2) {
        if (comp[i] == comp[i + 1]) {
            cout << "IMPOSSIBLE\n";
            return 0;
        }

        ans[i / 2] = (comp[i] > comp[i + 1]);
    }

    for (int i = 1; i <= vars; i++) cout << (ans[i] ? "+" : "-") << " ";
}
```



### Coin Collector - dp on scc dag

Had it been a directed graph then we only needed to find the largest sum connected component. But it is a directed graph. Had it been a dag then we could have done dp. Dp in topo order might work maybe if you never revisited nodes. But you might need to backtrack to get more value. The sccs themselves always form a DAG. Had there been a cycle then it would be joined into one scc. So consider the scc clusted sums as nodes, since in an scc you can take all and apply dp on this dag.



One thing to note is that since the scc dfs is done in topo order, the components 1,2,3 and so on are also in topo order.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1), gt(n + 1);
    vector<int> vals(n + 1);
    for (int i = 1; i <= n; i++) cin >> vals[i];

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        gt[v].push_back(u);
    }

    vector<int> vis(n + 1), topo;
    function<void(int)> topo_dfs = [&](int u) {
        vis[u] = 1;
        for (int v : g[u]) {
            if (!vis[v]) topo_dfs(v);
        }
        topo.push_back(u);
    };
    for (int i = 1; i <= n; i++)
        if (!vis[i]) topo_dfs(i);
    reverse(topo.begin(), topo.end());

    vector<int> comp(n + 1), comp_sum(n + 1);
    int comp_cnt = 0;
    function<void(int)> scc_dfs = [&](int u) {
        comp[u] = comp_cnt;
        comp_sum[comp_cnt] += vals[u];
        for (int v : gt[u]) {
            if (!comp[v]) scc_dfs(v);
        }
    };
    for (int x : topo) {
        if (!comp[x]) {
            comp_cnt++;
            scc_dfs(x);
        }
    }

    vector<vector<int>> rev_scc_graph(comp_cnt + 1);

    for (int u = 1; u <= n; u++) {
        for (int v : g[u]) {
            if (comp[u] != comp[v]) {
                rev_scc_graph[comp[v]].push_back(comp[u]);
            }
        }
    }

    vector<int> dp(comp_cnt + 1);
    // since scc generated in topo order, the comps are also in topo order
    for (int i = 1; i <= comp_cnt; i++) {
        dp[i] = comp_sum[i];
        for (int j : rev_scc_graph[i]) {
            dp[i] = max(dp[i], dp[j] + comp_sum[i]);
        }
    }

    int ans = *max_element(dp.begin(), dp.end());
    cout << ans;

    return 0;
}
```

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1), gt(n + 1);
    vector<int> vals(n + 1);
    for (int i = 1; i <= n; i++) cin >> vals[i];

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        gt[v].push_back(u);
    }

    vector<int> vis(n + 1), topo;
    function<void(int)> topo_dfs = [&](int u) {
        vis[u] = 1;
        for (int v : g[u]) {
            if (!vis[v]) topo_dfs(v);
        }
        topo.push_back(u);
    };
    for (int i = 1; i <= n; i++)
        if (!vis[i]) topo_dfs(i);
    reverse(topo.begin(), topo.end());

    vector<int> comp(n + 1), comp_sum(n + 1);
    int comp_cnt = 0;
    function<void(int)> scc_dfs = [&](int u) {
        comp[u] = comp_cnt;
        comp_sum[comp_cnt] += vals[u];
        for (int v : gt[u]) {
            if (!comp[v]) scc_dfs(v);
        }
    };
    for (int x : topo) {
        if (!comp[x]) {
            comp_cnt++;
            scc_dfs(x);
        }
    }

    vector<vector<int>> scc_graph(n + 1), rev_scc_graph(comp_cnt + 1);

    for (int u = 1; u <= n; u++) {
        for (int v : g[u]) {
            if (comp[u] != comp[v]) {
                // scc edge from comp[u] to comp[v]
                scc_graph[comp[u]].push_back(comp[v]);
                rev_scc_graph[comp[v]].push_back(comp[u]);
            }
        }
    }

    topo.clear();
    vis.assign(comp_cnt + 1, 0);
    function<void(int)> scc_topo = [&](int u) {
        vis[u] = 1;
        for (int v : scc_graph[u]) {
            if (!vis[v]) scc_topo(v);
        }
        topo.push_back(u);
    };
    for (int i = 1; i <= comp_cnt; i++) {
        if (!vis[i]) scc_topo(i);
    }
    reverse(topo.begin(), topo.end());

    vector<int> dp(comp_cnt + 1);
    // since scc generated in topo order, the comps are also in topo order
    for (int i : topo) {
        dp[i] = comp_sum[i];
        for (int j : rev_scc_graph[i]) {
            dp[i] = max(dp[i], dp[j] + comp_sum[i]);
        }
    }

    int ans = *max_element(dp.begin(), dp.end());
    cout << ans;

    return 0;
}
```

### Mail Delivery - eulerian path (undirected)

```cpp
#include <bits/stdc++.h>
using namespace std;
 
#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);
 
signed main() {
    fast_io;
 
    int n, m;
    cin >> n >> m;
    vector<set<int>> g(n + 1);
 
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        g[a].insert(b);
        g[b].insert(a);
    }
 
    for (int i = 1; i <= n; i++) {
        if ((int)g[i].size() % 2) {
            cout << "IMPOSSIBLE";
            return 0;
        }
    }
 
    vector<int> path;
    function<void(int)> dfs = [&](int u) {
        while (!g[u].empty()) {
            int v = *g[u].begin();
            g[u].erase(v);
            g[v].erase(u);
            dfs(v);
        }
        path.push_back(u);
    };
 
    dfs(1);
 
    if ((int)path.size() != m + 1) {
        cout << "IMPOSSIBLE";
        return 0;
    }
 
    for (int x : path) {
        cout << x << " ";
    }
 
    return 0;
}
```

### De Bruijn Sequence - special, euler path

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n;
    cin >> n;

    if (n == 1) {
        cout << "10";
        return 0;
    }

    vector<set<int>> g(1ll << (n - 1));

    // nodes are 0 1 to to 2^(n-1) - 1
    // hence all possible sequences of len n-1

    // when going through 0, left shift by 1
    // when going through 1, left shift by 1 and add 1
    // in both cases 0 the nth index bit and above

    for (int i = 0; i < (1ll << (n - 1)); i++) {
        int prefix_bits_mask = (1ll << (n - 1)) - 1;
        g[i].insert((i << 1) & prefix_bits_mask);
        g[i].insert(((i << 1) + 1) & prefix_bits_mask);
    }

    vector<int> path;
    function<void(int)> dfs = [&](int u) {
        while (!g[u].empty()) {
            int v = *g[u].begin();
            g[u].erase(v);
            dfs(v);
        }
        path.push_back(u);
    };

    dfs(0);

    // at the end you will back at node with val 0,
    // only one 0 is counted in the edge so add the remaining
    // n-2 0s to the path
    for (int i = 0; i < n - 2; i++) path.push_back(0);

    for (int x : path) {
        cout << (x & 1);
    }

    return 0;
}
```

### Teleporters Path - eulerian path (directed)

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;

    vector<set<int>> g(n + 1);
    vector<int> indeg(n + 1);

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        g[a].insert(b);
        indeg[b]++;
    }

    for (int i = 2; i <= n - 1; i++) {
        if (indeg[i] != (int)g[i].size()) {
            cout << "IMPOSSIBLE";
            return 0;
        }
    }

    if ((int)g[1].size() != indeg[1] + 1 || (int)g[n].size() + 1 != indeg[n]) {
        cout << "IMPOSSIBLE";
        return 0;
    }

    vector<int> path;
    function<void(int)> dfs = [&](int u) {
        while (!g[u].empty()) {
            int v = *g[u].begin();
            g[u].erase(v);
            dfs(v);
        }
        path.push_back(u);
    };

    dfs(1);

    // 1 would be pushed last so reverse path
    reverse(path.begin(), path.end());

    if ((int)path.size() != m + 1) {
        cout << "IMPOSSIBLE";
        return 0;
    }

    for (int x : path) {
        cout << x << " ";
    }

    return 0;
}
```

### Hamiltonian Flights - hamiltonian path

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
    }

    vector<vector<int>> dp(1ll << n, vector<int>(n + 1));
    dp[1][1] = 1;

    int mod = 1e9 + 7;

    for (int vis = 0; vis < (1ll << n); vis++) {
        for (int last = 1; last <= n; last++) {
            if (!dp[vis][last]) continue;

            for (int next : g[last]) {
                if ((vis >> (next - 1)) & 1) continue;
                // only visit last if rest all visited
                if (next == n && __builtin_popcountll(vis) != n - 1) continue;

                int nvis = vis | (1ll << (next - 1));
                (dp[nvis][next] += dp[vis][last]) %= mod;
            }
        }
    }

    cout << dp[(1ll << n) - 1][n];

    return 0;
}
```

### Download Speed - max flow

$O(M^2N)$ Eddmond Karp

The idea for this one is simple. Use bfs to find a path. Find the min of that. Reduce that capacity, add it to reversed edge to use later in other direction for reducing flow here.

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);

    vector<vector<int>> capacity(n + 1, vector<int>(n + 1));

    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        g[a].push_back(b);
        g[b].push_back(a);
        capacity[a][b] += w;
        capacity[b][a] += 0;
    }

    auto max_flow = [&](int src, int sink) -> int {
        int flow = 0;
        vector<int> par(n + 1);

        auto find_path = [&]() -> int {
            fill(par.begin(), par.end(), -1);
            par[src] = -2;

            queue<int> q;
            q.push(src);

            while (!q.empty()) {
                int u = q.front();
                q.pop();

                for (int v : g[u]) {
                    if (par[v] == -1 && capacity[u][v]) {
                        par[v] = u;
                        // early terminate
                        if (v == sink) return 1;
                        q.push(v);
                    }
                }
            }

            return 0;
        };

        while (find_path()) {
            int new_flow = INF;

            int cur = sink;
            while (cur != src) {
                int prev = par[cur];
                new_flow = min(new_flow, capacity[prev][cur]);
                cur = prev;
            }

            flow += new_flow;

            cur = sink;
            while (cur != src) {
                int prev = par[cur];
                capacity[prev][cur] -= new_flow;
                capacity[cur][prev] += new_flow;
                cur = prev;
            }
        }

        return flow;
    };

    cout << max_flow(1, n) << "\n";

    return 0;
}
```

$O(M^2log(max\ wt))$ Scaling Dfs

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);

    vector<vector<int>> capacity(n + 1, vector<int>(n + 1));

    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        g[a].push_back(b);
        g[b].push_back(a);
        capacity[a][b] += w;
        capacity[b][a] += 0;
    }

    auto max_flow = [&](int src, int sink) -> int {
        int flow = 0;
        vector<int> par(n + 1);

        int thres = 1e9;  // max of weights

        function<void(int)> dfs = [&](int u) {
            for (int v : g[u]) {
                if (par[v] == -1 && capacity[u][v] >= thres) {
                    par[v] = u;
                    dfs(v);
                }
            }
        };

        while (thres) {
            fill(par.begin(), par.end(), -1);
            par[src] = -2;

            dfs(src);

            if (par[sink] != -1) {
                int cur = sink;
                while (cur != src) {
                    int prev = par[cur];
                    capacity[prev][cur] -= thres;
                    capacity[cur][prev] += thres;
                    cur = prev;
                }
                flow += thres;
            } else {
                thres /= 2;
            }
        }

        return flow;
    };

    cout << max_flow(1, n) << "\n";

    return 0;
}
```

There’s also $O(N^2M)$ Dinic (see cp-algo) that I can use a black box for now. I guess for max flow this is enough. As CPH said, in practice I should always use this scaling dfs.

### Polic Chase - min cut

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

signed main() {
    fast_io;

    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);

    vector<vector<int>> cap(n + 1, vector<int>(n + 1)), orig(n + 1, vector<int>(n + 1));

    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
        cap[a][b]++, cap[b][a]++;
    }

    auto min_cuts = [&](int src, int sink) -> vector<array<int, 2>> {
        int flow = 0;
        vector<int> par(n + 1);

        int thres = 1e9;  // max of weights

        function<void(int)> dfs = [&](int u) {
            for (int v : g[u]) {
                if (par[v] == -1 && cap[u][v] >= thres) {
                    par[v] = u;
                    dfs(v);
                }
            }
        };

        while (thres) {
            fill(par.begin(), par.end(), -1);
            par[src] = -2;

            dfs(src);

            if (par[sink] != -1) {
                int cur = sink;
                while (cur != src) {
                    int prev = par[cur];
                    cap[prev][cur] -= thres;
                    cap[cur][prev] += thres;
                    cur = prev;
                }
                flow += thres;
            } else {
                thres /= 2;
            }
        }

        // what is reachable
        vector<int> vis(n + 1);
        function<void(int)> dfs2 = [&](int u) {
            vis[u] = 1;
            for (int v : g[u]) {
                if (!vis[v] && cap[u][v]) {
                    dfs2(v);
                }
            }
        };
        dfs2(src);

        vector<array<int, 2>> cuts;
        for (int i = 1; i <= n; i++) {
            if (!vis[i]) continue;
            for (int j : g[i]) {
                if (!vis[j] && !cap[i][j]) {
                    cuts.push_back({i, j});
                }
            }
        }

        return cuts;
    };

    auto res = min_cuts(1, n);
    cout << res.size() << "\n";
    for (auto [a, b] : res) {
        cout << a << " " << b << "\n";
    }
    return 0;
}
```

### School Dance - max bipartite matching

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

const int INF = 1e18;

signed main() {
    fast_io;

    int boys, girls, k;
    cin >> boys >> girls >> k;

    int n = boys + girls;

    vector<vector<int>> g(n + 2);
    vector<vector<int>> cap(n + 2, vector<int>(n + 2));

    for (int i = 0; i < k; i++) {
        int a, b;
        cin >> a >> b;
        b += boys;
        g[a].push_back(b);
        g[b].push_back(a);
        cap[a][b]++;
    }

    for (int i = 1; i <= boys; i++) {
        g[0].push_back(i);
        g[i].push_back(0);
        cap[0][i]++;
    }
    for (int i = boys + 1; i <= n; i++) {
        g[i].push_back(n + 1);
        g[n + 1].push_back(i);
        cap[i][n + 1]++;
    }

    auto max_flow = [&](int src, int sink) {
        int flow = 0;
        vector<int> par(n + 2);

        auto bfs = [&]() -> bool {
            fill(par.begin(), par.end(), -1);
            par[src] = -2;

            queue<int> q;
            q.push(src);

            while (!q.empty()) {
                int u = q.front();
                q.pop();

                for (int v : g[u]) {
                    if (par[v] == -1 && cap[u][v]) {
                        par[v] = u;
                        if (v == sink) return true;
                        q.push(v);
                    }
                }
            }

            return false;
        };

        while (bfs()) {
            int new_flow = INF;
            int cur = sink;
            while (cur != src) {
                int p = par[cur];
                new_flow = min(new_flow, cap[p][cur]);
                cur = p;
            }

            flow += new_flow;

            cur = sink;
            while (cur != src) {
                int p = par[cur];
                cap[p][cur] -= new_flow;
                cap[cur][p] += new_flow;
                cur = p;
            }
        }
    };

    max_flow(0, n + 1);

    vector<array<int, 2>> ans;
    for (int i = 1; i <= boys; i++) {
        for (int j = 1; j <= girls; j++) {
            if (cap[j + boys][i]) {
                ans.push_back({i, j});
            }
        }
    }

    cout << ans.size() << "\n";
    for (auto [a, b] : ans) {
        cout << a << " " << b << "\n";
    }

    return 0;
}
```

### Distinct Routes - TODO

## Trees

### Subordinates - subtree size dfs

```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

signed main() {
    fast_io;

    int n;
    cin >> n;
    vector<vector<int>> g(n + 1);
    for (int i = 2; i <= n; i++) {
        int x;
        cin >> x;
        g[x].push_back(i);
    }

    vector<int> sz(n + 1);
    function<int(int)> dfs = [&](int u) {
        sz[u]++;
        for (int v : g[u]) sz[u] += dfs(v);
        return sz[u];
    };
    dfs(1);

    for (int i = 1; i <= n; i++) {
        cout << sz[i] - 1 << " ";
    }

    return 0;
}
```

### Tree Matching - maximum matching in a tree





