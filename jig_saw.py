import numpy as np
from PIL import Image
from math import inf

class neighbor:
    def __init__(self, l, d, r, u, l_cost, d_cost, r_cost, u_cost):
        self.left = l
        self.down = d
        self.right = r
        self.up = u
        self.l_cost = inf
        self.d_cost = inf
        self.r_cost = inf
        self.u_cost = inf

def cmp_left(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[i][0][j]
            curr_b = b[i][p - 1][j]
            if curr_a > curr_b:
                ans += (curr_a - curr_b)**2
            else:
                ans += (curr_b - curr_a)**2
    return ans

def cmp_down(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[p - 1][i][j]
            curr_b = b[0][i][j]
            if curr_a > curr_b:
                ans += (curr_a - curr_b)**2
            else:
                ans += (curr_b - curr_a)**2
    return ans

def cmp_right(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[i][p - 1][j]
            curr_b = b[i][0][j]
            if curr_a > curr_b:
                ans += (curr_a - curr_b)**2
            else:
                ans += (curr_b - curr_a)**2
    return ans

def cmp_up(a, b, p):
    ans = 0
    for i in range(p):
        for j in range(3):
            curr_a = a[0][i][j]
            curr_b = b[p - 1][i][j]
            if curr_a > curr_b:
                ans += (curr_a - curr_b)**2
            else:
                ans += (curr_b - curr_a)**2
    return ans

def expand(grid, index, last, hor, ver, m, p, x):
    line = [None] * m
    _i = last[0]
    _j = last[1]

    curr = [_i, _j]
    j = _j
    for i in range(_i, _i + m * ver, ver):
        line[i - _i] = curr

        index[i][j] = (curr[0], curr[1])
        grid[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]

        Next = None
        if ver == 1:
            Next = neighbors[curr[0]][curr[1]].down
        elif ver == -1:
            Next = neighbors[curr[0]][curr[1]].up
        curr = Next

    for j in range(_j + hor, _j + m * hor, hor):
        for i in range(_i, _i + m * ver, ver):
            prev = line[i - _i]
            neighbor = neighbors[prev[0]][prev[1]]
            if hor == 1:
                curr = neighbor.right
            elif hor == -1:
                curr = neighbor.left

            index[i][j] = (curr[0], curr[1])
            grid[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]

            line[i - _i] = curr

def correct(grid, index, cost, neighbors, last, hor, ver):
    _i = last[0]
    _j = last[1]

    j = _j
    for i in range(_i + hor, _i + m * hor, hor):
        curr_min = inf
        i_ind = index[i]
        j_ind = index[j]
        # curr_min = min(curr_min, cot)

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

if __name__ == "__main__":
    img_index = "4"

    # problem A
    p = 64
    m = 8
    k = 112
    x = Image.open(img_index + ".jpeg", 'r')
    x = np.array(x)

    # jigsaw_net = JigsawNet()
    # x = jigsaw_net.forward(x, p, m)

    neighbors = [[None for j in range(m)] for i in range(m)]

    # discover corners

    max_l_u = -inf
    max_l_d = -inf
    max_r_d = -inf
    max_r_u = -inf
    l_u = [0, 0, 0]
    l_d = [0, 0, 1]
    r_d = [0, 0, 2]
    r_u = [0, 0, 3]

    for i in range(m):
        for j in range(m):
            curr = x[p*i : p*(i + 1), p*j : p*(j + 1)]
            # print(curr)

            # evaluate neighbors
            left_min = inf
            curr_left = [-1, -1]

            down_min = inf
            curr_down = [-1, -1]

            right_min = inf
            curr_right = [-1, -1]

            up_min = inf
            curr_up = [-1, -1]

            for _i in range(m):
                for _j in range(m):
                    if _i == i and _j == j: continue
                    _curr = x[p*_i : p*(_i + 1), p*_j : p*(_j + 1)]

                    # evaluate neighbors
                    left = cmp_left(curr, _curr, p)
                    if left < left_min:
                        left_min = left
                        curr_left = [_i, _j]
                    
                    down = cmp_down(curr, _curr, p)
                    if down < down_min:
                        down_min = down
                        curr_down = [_i, _j]

                    right = cmp_right(curr, _curr, p)
                    if right < right_min:
                        right_min = right
                        curr_right = [_i, _j]

                    up = cmp_up(curr, _curr, p)
                    if up < up_min:
                        up_min = up
                        curr_up = [_i, _j]

            # discover corners
            sum_l_u = left_min + up_min
            if sum_l_u > max_l_u:
                max_l_u = sum_l_u
                l_u = [i, j, 0]

            sum_l_d = left_min + down_min
            if sum_l_d > max_l_d:
                max_l_d = sum_l_d
                l_d = [i, j, 1]

            sum_r_d = right_min + down_min
            if sum_r_d > max_r_d:
                max_r_d = sum_r_d
                r_d = [i, j, 2]

            sum_r_u = right_min + up_min
            if sum_r_u > max_r_u:
                max_r_u= sum_r_u
                r_u = [i, j, 3]

            neighbors[i][j] = neighbor(curr_left, curr_down, curr_right, curr_up, left_min, down_min, right_min, up_min)


    grid = np.copy(x)
    grid = np.concatenate((grid, grid), axis=0)
    grid = np.concatenate((grid, grid), axis=1)
    
    index = [[None for j in range(2 * m - 1)] for i in range(2 * m - 1)]

    last = [m - 1, m - 1]

    # propagate from top-left
    expand(grid, index, last, 1, 1, m, p, x)
    img = Image.fromarray(grid, 'RGB')
    img.save(img_index + "_restored_0.jpeg")

    # propagate from bottom-left
    expand(grid, index, last, 1, -1, m, p, x)
    img = Image.fromarray(grid, 'RGB')
    img.save(img_index + "_restored_1.jpeg")

    # propagate from top-right
    expand(grid, index, last, -1, 1, m, p, x)
    img = Image.fromarray(grid, 'RGB')
    img.save(img_index + "_restored_2.jpeg")

    # propagate from bottom-right
    expand(grid, index, last, -1, -1, m, p, x)
    img = Image.fromarray(grid, 'RGB')
    img.save(img_index + "_restored_3.jpeg")

    cost = [[0 for j in range(2 * m - 1)] for i in range(2 * m - 1)]

    correct(grid, index, cost, neighbors, last, 1, 1)
    correct(grid, index, cost, neighbors, last, 1, -1)
    correct(grid, index, cost, neighbors, last, -1, 1)
    correct(grid, index, cost, neighbors, last, -1, -1)
    
    [i, j] = get_min_cost(cost, m)

    ans = grid[i : i + p * m, j : j + p * m]
    # ans = grid

    img = Image.fromarray(ans, 'RGB')
    img.save(img_index + "_ans.jpeg")