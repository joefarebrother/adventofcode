from utils import *

files = []
inp = inp_readall().strip()

@dataclass 
class Block:
    free: bool 
    id: int 
    offset: int 
    size: int

    def checksum(self):
        res = 0
        for o in range(self.offset, self.offset+self.size):
            res += self.id*o 
        return res

off = 0 
for i,n in enumerate(inp):
    n = int(n)
    files.append(Block(i%2==1,i//2,off,n))
    off += n 

print(files)

def next_free(blockid,off):
    while not files[blockid].free:
        off += files[blockid].offset
        blockid += 1 
    return blockid, off

cur_free = next_free(0,0)

def compact(file):
    global cur_free
    freeid, freeoff = cur_free

    freebl = files[freeid]
    assert freebl.free, (freeid, freebl, cur_free)

    

    while file.size:
        if freebl.offset > file.offset:
            return
        printx(freebl, file)
        if freebl.offset+freebl.size==file.offset:
            freebl.id = file.id 
            freebl.size = file.size 
            file.size = 0 
            freebl.free=False
            freeid,freeoff = cur_free =next_free(*cur_free)

        elif file.size >= freebl.size:
            freebl.id = file.id 
            freebl.free = False 
            file.size -= freebl.size 
            freeid,freeoff = cur_free =next_free(*cur_free)
            freebl = files[freeid]

        else:
            nsize = freebl.size - file.size 
            nfree = Block(True, 0, freebl.offset+file.size, nsize)
            files.insert(freeid+1, nfree)
            freebl.id = file.id 
            freebl.free = False 
            freebl.size = file.size
            file.size = 0 
            freeid,freeoff = cur_free =next_free(*cur_free)
        
# for bl in files[::-1]:
#     if not bl.free:
#         compact(bl)
    
# print(files)

# chk = 0
# toff = 0
# for bl in files:
#     #assert bl.offset == toff or bl.size==0, (bl, toff)
#     toff += bl.size
#     if not bl.free:
#         chk += bl.checksum()
#         printx(str(bl.id)*bl.size,end="")
        
# print()

# print("Part 1", chk)

def compact2(file):
    print(file)
    cur_free = next_free(0,0)
    while (freebl:=files[freeid:=cur_free[0]]).size < file.size and freebl.offset < file.offset:
        #print(cur_free)
        cur_free = next_free(cur_free[0]+1,cur_free[1]+freebl.size)

    if freebl.offset > file.offset:
            return
    
    elif file.size >= freebl.size:
            freebl.id = file.id 
            freebl.free = False 
            file.size -= freebl.size 
            return 


    
    nsize = freebl.size - file.size 
    nfree = Block(True, 0, freebl.offset+file.size, nsize)
    files.insert(freeid+1, nfree)
    freebl.id = file.id 
    freebl.free = False 
    freebl.size = file.size
    file.size = 0 

for bl in files[::-1]:
    if not bl.free:
        compact2(bl)

print(files)

chk = 0
toff = 0
for bl in files:
    #assert bl.offset == toff or bl.size==0, (bl, toff)
    toff += bl.size
    if not bl.free:
        chk += bl.checksum()
        printx(str(bl.id)*bl.size,end="")
    else:
        printx("."*bl.size,end="")

print()

print(chk)
