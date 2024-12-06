from utils import *

g = Grid(0)

guard = only(g.indices("^")) # finds the position of ^ and verifies its unique

# This is functools.cache, which caches the results of the function so it is not recomputed next time its called on the same inputs
# As the function is recursive, this results in every point along the path to the next wall being cached
@cache 
def next_wall(p,d):
    if p+d not in g:
        return (p+d,d*Dirs.tR) # still do the turn so we are consistently returning a turned direction
    if g[p+d] == "#":
        return p,d*Dirs.tR 
    return next_wall(p+d,d)

print(next_wall(IVec2(7,7),Dirs.D))
    
def go(extra=None):
    # extra is position to place extra wall 

    path = []
    p,d = guard, Dirs.up 

    while (p,d) not in path and p in g:
        path.append((p,d))
        np,nd = next_wall(p,d)

        if extra and extra in Rectangle(p, np): # Rectangle is my own util class for doing stuff with rectangles
            # stop one point before the extra wall
            diff = extra-p 
            diff = diff/diff.abs()
            assert diff in [Dirs.U,Dirs.D,Dirs.L,Dirs.R]
            np = extra-diff 

        p,d = np,nd
    path.append((p,d))

    looped = p in g 

    if looped:
        print(extra,p,d)

    return path, looped 

def calc_path(path):
    # calculates the path from the list of points 
    res = set()

    for ((p1,_),(p2,_)) in windows(path,2): # windows is my own util to take sliding windows. windows(X,2) is equiv to itertools.pairwise(X)
        rect = Rectangle(p1,p2)
        assert rect.width == 1 or rect.height == 1 
        for p in rect:
            if p in g:
                res.add(p)

    return res 

path,_ = go()
path = calc_path(path) 

# for p in path:
#     g[p] = "X"
# g.draw()

print("Part 1:", len(path))
print("Part 2:", sum(go(p)[1] for p in path if g[p]=="."))