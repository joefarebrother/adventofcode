from utils import *

rules,ords = inp_groups()
# print(rules, ords)

gr = defaultdict(list)
for r in rules:
    a,b = ints_in(r)
    gr[a].append(b)

# a -> b : a comes directly before b
# b in gr[a] -> b comes after a



bad = []
t = 0
for ord in ords:
    ord = ints_in(ord)
    for ia,a in enumerate(ord):
        for b in ord[ia+1:]:
            if a in gr[b]:
                bad.append(ord)
                break 
        else:
            continue
        break
    else:
        # print(ord, ord[len(ord)//2+1])
        t += ord[len(ord)//2]

print("Part 1:", t)

t = 0
for ord in bad:
    nord = []
    while len(nord)<len(ord):
        nord.append(only([a for a in ord if a not in nord and not any(b not in nord and b in gr[a] for b in ord)]))
    # print(ord, "fix", nord)
    t += nord[len(nord)//2]

print("Part 2:", t)


# Post-solve testing of properties

if is_ex:
    after = defaultdict(list)
    for a in gr:
        after[a] = DGraph(gr).topsort(a) # b reachable from a -> b comes after
        print(a, len(after[a]), after[a], len(gr))
    for ord in bad:
        # original approach - failed bc i didn't know how cmp_to_key worked
        # wouldn't have worked on real anyway due to global topsort failing
        nord = sorted(ord, key=lt_to_key(lambda a,b: b in after[a])) 
        for a,b in windows(nord, 2):
            print(a, b, b in after[a])
        print(ord, nord)

# verifying that we have a total order on every provided list
# this implies sorting with a costom comparator would have worked 


for ord in ords:
    ord = ints_in(ord)
    for a,b in it.combinations(ord, 2):
        if a not in gr[b] and b not in gr[a]:
            print("Non total", ord, a, b)

# in fact its a total relation overall
for a,b in it.combinations(gr.keys(), 2):
    if a not in gr[b] and b not in gr[a]:
        print("Non total", ord, a, b)

            
# sorting with custom comparator (and reporting incomparable elements as equal) doesn't work 'in general' 
# (i saw some ppl specifying that's how they handle incomparable elements, but it only works because there *are* no incomparable elements)
# where 'in general' = 'under the minimum constraints such that every provided list has a unique sort'
# which is a little stronger than the true general constraint that there's only a unique centre
# either case a topsort restricted to eacj input list would work 
# but the question is whether sorting with custom comparator (that reports incomparible elements as equal) works in general with a non-transitive order
# in fact, clearly its not. Consider 1|2, 2|3. 
     

# graphviz-ing the real input crashes it (out of memory)

# import graphviz

# dot = graphviz.Digraph()
# for a in gr:
#     dot.node(str(a),str(a))

# for a,bs in gr.items():
#     for b in bs:
#         #if str(a) < str(b):
#             dot.edge(str(a),str(b))

# dot.render(f"2024/5/{'ex' if is_ex else 'real'}.gv", format="png")
