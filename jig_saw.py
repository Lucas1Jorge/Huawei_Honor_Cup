import numpy as np
from PIL import Image
from math import inf

class neighbor:
    def __init__(self, l, d, r, u):
        self.up = u
        self.down = d
        self.left = l
        self.right = r

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

if __name__ == "__main__":
    img_index = "5"

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

            neighbors[i][j] = neighbor(curr_left, curr_down, curr_right, curr_up)


    ans = np.copy(x)

    # propagate from top-left
    line = [None] * m
    i = 0
    curr = [l_u[0], l_u[1]]

    j = 0
    for i in range(m):
        line[i] = curr
        ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]
        down = neighbors[curr[0]][curr[1]].down
        curr = down

    for j in range(1, m):
        for i in range(m):
            prev = line[i]
            curr = neighbors[prev[0]][prev[1]].right
            ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]

            line[i] = curr

    img = Image.fromarray(ans, 'RGB')
    img.save(img_index + "_restored_0.jpeg")

    # Propagate from bottom-left
    line = []
    i = m - 1
    curr = [l_d[0], l_d[1]]
    line.append(curr)

    for j in range(m):
        ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]
        right = neighbors[curr[0]][curr[1]].right
        curr = right
        line.append(curr)

    for i in range(m - 2, -1, -1):
        for j in range(m):
            prev = line[j]
            curr = neighbors[prev[0]][prev[1]].up
            ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]

            line[j] = curr

    img = Image.fromarray(ans, 'RGB')
    img.save(img_index + "_restored_1.jpeg")

    # Propagate from bottom-right
    line = [None] * m
    i = m - 1
    curr = [r_d[0], r_d[1]]

    for j in range(m - 1, -1, -1):
        ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]
        
        line[j] = curr
        left = neighbors[curr[0]][curr[1]].left
        curr = left

    for i in range(m - 2, -1, -1):
        for j in range(m - 1, -1, -1):
            prev = line[j]
            curr = neighbors[prev[0]][prev[1]].up
            ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]

            line[j] = curr

    img = Image.fromarray(ans, 'RGB')
    img.save(img_index + "_restored_2.jpeg")

    # Propagate from top-right
    line = [None] * m
    i = m - 1
    curr = [r_u[0], r_u[1]]
    line[m - 1] = curr

    for j in range(m - 2, -1, -1):
        ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]
        right = neighbors[curr[0]][curr[1]].right
        curr = right
        line[j] = curr

    for i in range(m - 2, -1, -1):
        for j in range(m - 1, -1, -1):
            prev = line[j]
            curr = neighbors[prev[0]][prev[1]].up
            ans[p*i:p*(i+1), p*j:p*(j+1)] = x[p*curr[0]:p*(curr[0]+1), p*curr[1]:p*(curr[1]+1)]

            line[j] = curr

    img = Image.fromarray(ans, 'RGB')
    img.save(img_index + "_restored_3.jpeg")
