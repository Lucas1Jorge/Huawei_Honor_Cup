import numpy as np
from PIL import Image
from math import inf
import heapq

def index(i, j, m):
    return m * i + j

def inv_index(i, m):
    _i = i // m
    _j = i % m
    return [_i, _j]

def direction(d):
    if d == "u": return [0, -1]
    if d == "l": return [-1, 0]
    if d == "r": return [1, 0]
    if d == "d": return [0, 1]

def cmp_left(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[i][0][j]
            curr_b = b[i][p - 1][j]
            if curr_a > curr_b:
                ans += curr_a - curr_b
            else:
                ans += curr_b - curr_a
    return ans

def cmp_down(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[p - 1][i][j]
            curr_b = b[0][i][j]
            if curr_a > curr_b:
                ans += curr_a - curr_b
            else:
                ans += curr_b - curr_a
    return ans

def cmp_right(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[i][p - 1][j]
            curr_b = b[i][0][j]
            if curr_a > curr_b:
                ans += curr_a - curr_b
            else:
                ans += curr_b - curr_a
    return ans

def cmp_up(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[0][i][j]
            curr_b = b[p - 1][i][j]
            if curr_a > curr_b:
                ans += curr_a - curr_b
            else:
                ans += curr_b - curr_a
    return ans

def get_min_cost(cost, m):
    ans = [0, 0]
    ans_cost = inf

    for i in range(len(cost)):
        for j in range(len(cost[i])):
            if i > 0:
                cost[i][j] += cost[i - 1][j]
            if j > 0:
                cost[i][j] += cost[i][j - 1]
            if i > 0 and j > 0:
                cost[i][j] -= cost[i - 1][j - 1]

    for i in range(m - 1, len(cost)):
        for j in range(m - 1, len(cost[i])):
            curr = cost[i][j]

            if i >= m:
                curr -= cost[i - m][j]
            if j >= m:
                curr -= cost[i][j - m]
            if i >= m and j >= m:
                curr += cost[i - m][j - m]

            if curr < ans_cost:
                ans_cost = curr
                ans = [i - m + 1, j - m + 1]
    
    return ans

class edge:
    def __init__(self, u, v, w, src, dest):
        self.u = u
        self.v = v
        self.w = w
        self.src = src
        self.dest = dest

class cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.children = {}

def get_edges(x, p, m, edges_matrix):
    edges = []

    for i in range(m):
        for j in range(m):
            curr = x[p*i : p*(i + 1), p*j : p*(j + 1)]

            for _i in range(m):
                for _j in range(m):
                    if _i == i and _j == j: continue

                    _curr = x[p*_i : p*(_i + 1), p*_j : p*(_j + 1)]

                    # evaluate neighbors
                    left = cmp_left(curr, _curr, p)
                    down = cmp_down(curr, _curr, p)
                    right = cmp_right(curr, _curr, p)
                    up = cmp_up(curr, _curr, p)

                    l = edge(index(i, j, m), index(_i, _j, m), left, "r", "l")
                    d = edge(index(i, j, m), index(_i, _j, m), down, "u", "d")
                    r = edge(index(i, j, m), index(_i, _j, m), right, "l", "r")
                    u = edge(index(i, j, m), index(_i, _j, m), up, "d", "u")

                    edges.append((l.w, i, j, _i, _j, 0, l))
                    edges.append((d.w, i, j, _i, _j, 1, d))
                    edges.append((r.w, i, j, _i, _j, 2, r))
                    edges.append((u.w, i, j, _i, _j, 3, u))

    return edges

def dfs(graph, grid, x, i, j, _i, _j, visited, LEFT, TOP, RIGHT, DOWN):
    visited[_i][_j] = True

    LEFT[0] = min(LEFT[0], j)
    TOP[0] = min(TOP[0], i)
    RIGHT[0] = max(RIGHT[0], j)
    DOWN[0] = max(DOWN[0], i)

    grid[p*i : p*(i+1), p*j : p*(j+1)] = x[p*_i : p*(_i+1), p*_j : p*(_j+1)]

    for key, val in graph[_i][_j].children.items():
        if not visited[val[0]][val[1]]:
            d = direction(key)
            dfs(graph, grid, x, i + d[1], j + d[0], val[0], val[1], visited, LEFT, TOP, RIGHT, DOWN)

def bfs_refine(graph, grid, x, i, j, _i, _j, visited):
    pass

if __name__ == "__main__":
    img_index = "2404"

    # problem A
    p = 64
    m = 8
    k = 112
    x = Image.open(img_index + ".png", 'r')
    x = np.array(x)

    edges_matrix = None
    edges = get_edges(x, p, m, edges_matrix)
    heapq.heapify(edges)

    visited = {}

    cost = 0
    ans = []
    while len(edges) > 0:
        curr = heapq.heappop(edges)
        w = curr[0]
        i = curr[1]
        j = curr[2]
        _i = curr[3]
        _j = curr[4]
        pos = curr[6]

        hash_1 = (i, j, pos.src)
        hash_2 = (_i, _j, pos.dest)

        if hash_1 in visited or hash_2 in visited:
            if not hash_1 in visited:
                visited[hash_1] = hash_2
            if not hash_2 in visited:
                visited[hash_2] = hash_1
            continue

        visited[hash_1] = hash_2
        visited[hash_2] = hash_1

        cost += w

        ans.append(curr)

    # print(len(ans))
    # print(cost)

    last = (m - 1, m - 1)

    graph = [[None for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            graph[i][j] = cell(-1, -1)

    visited = {}
    visited[last] = last

    while len(visited) < m * m:
        for k in range(len(ans)):
            curr = ans[k]
            w = curr[0]
            i = curr[1]
            j = curr[2]
            _i = curr[3]
            _j = curr[4]
            pos = curr[6]
            # print(len(ans), i, j, _i, _j)

            if (i, j) in visited:
                if not (_i, _j) in visited:
                    d = direction(pos.dest)
                    visited[(_i, _j)] = (i, j, d)
                    ans.pop(k)

                    graph[i][j].children[pos.dest] = (_i, _j)
                    graph[_i][_j].children[pos.src] = (i, j)

                    break

            elif (_i, _j) in visited:
                if not (i, j) in visited:
                    d = direction(pos.src)
                    visited[(i, j)] = (_i, _j, d)
                    ans.pop(k)

                    graph[i][j].children[pos.dest] = (_i, _j)
                    graph[_i][_j].children[pos.src] = (i, j)

                    break

    grid = np.copy(x)
    grid = np.concatenate((grid, grid), axis=0)
    grid = np.concatenate((grid, grid), axis=1)

    LEFT = [inf]
    TOP = [inf]
    RIGHT = [inf]
    DOWN = [inf]

    visited = [[False for j in range(m)] for i in range(m)]
    dfs(graph, grid, x, 7, 7, 7, 7, visited, LEFT, TOP, RIGHT, DOWN)

    # for row in visited:
    #     print(row)
    # for i in range(m):
    #     for j in range(m):
    #         print(graph[i][j].children)
            
    #         if not visited[i][j]:
    #             dfs(graph, grid, x, i, j, visited)

    # print(ans)
    # for key, val in visited.items():

    grid = grid[p*TOP[0] : p*(TOP[0] + m), p*LEFT[0] : p*(LEFT[0] + m)]

    img = Image.fromarray(grid, 'RGB')
    img.save(img_index + "_grid.jpeg")