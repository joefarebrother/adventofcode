from utils import *

g = Grid(0)

guard = only(g.indices("^")) # finds the position of ^ and verifies its unique

points = {complex(p) for p in g}
walls = {complex(p) for p in g.indices("#")}

# This is functools.cache, which caches the results of the function so it is not recomputed next time its called on the same inputs
# As the function is recursive, this results in every point along the path to the next wall being cached
@cache 
def next_wall(p,d):
    if p+d not in points:
        return p+d
    if p+d in walls:
        return p 
    return next_wall(p+d,d)

def on_line(ex, p, np):
    return abs(p-ex)+abs(np-ex) == abs(p-np) # triangle inequality is exact => colinear and on the line
    
def go(extra=None):
    # extra is position to place extra wall 

    path = []
    p,d = complex(guard), -1j 

    while (p,d) not in path and p in points:
        path.append((p,d))
        np,nd = next_wall(p,d), d*1j

        if extra and on_line(extra, p, np): 
            # stop one point before the extra wall
            diff = extra-p 
            diff = diff/abs(diff)
            # assert diff in [Dirs.U,Dirs.D,Dirs.L,Dirs.R]
            np = extra-diff 

        p,d = np,nd
    path.append((p,d))
    
    looped = p in points

    # if looped:
    #     print(extra,p,d)

    return path, looped 

def calc_path(path):
    # calculates the path from the list of points 
    res = set()

    for ((p1,_),(p2,_)) in windows(path,2): # windows is my own util to take sliding windows. windows(X,2) is equiv to itertools.pairwise(X)
        rect = Rectangle(p1,p2)
        assert rect.width == 1 or rect.height == 1 
        for p in rect:
            if p in g:
                res.add(complex(p))

    return res 

path,_ = go()
path = calc_path(path) 

# for p in path:
#     g[p] = "X"
# g.draw()

print("Part 1:", len(path))
print("Part 2:", sum(go(p)[1] for p in path if p != guard))

# time sol_orig.py:
# real    2m18.424s
# user    2m17.360s
# sys     0m0.421s

# time sol_orig.py: with grid fastpath via exception # this seems slightly faster
# real    1m49.247s
# user    1m48.125s
# sys     0m0.322s

# time sol_orig.py: with grid fastpath via double lookup
# real    1m54.352s
# user    1m53.107s
# sys     0m0.330s

# time sol_orig.py: with grid fastpath via sentinel
# real    1m52.815s
# user    1m51.549s
# sys     0m0.316s

# time sol_improved_using_ivec.py
# real    0m15.405s
# user    0m15.276s
# sys     0m0.069s

# time sol.py before removing rect
# real    0m8.318s
# user    0m8.265s
# sys     0m0.051s

# time sol.py before removing debugging print
# real    0m2.651s
# user    0m2.594s
# sys     0m0.056s

# time sol.py
# real    0m1.118s
# user    0m1.072s
# sys     0m0.039s