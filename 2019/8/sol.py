from utils import inp_readall, block_char

inp = inp_readall()
min_0s = 100000000000000
min_score = 0
layers = []

for i in range(0, len(inp)-1, 25*6):
    layer = inp[i:i+25*6]
    num_0 = layer.count('0')
    num_1 = layer.count('1')
    num_2 = layer.count('2')
    #print(i, len(layer), len(input), num_0, num_1, num_2)
    if num_0 < min_0s:
        min_0s = num_0
        min_score = num_1*num_2

    layers.append(layer)

print(min_score)

for y in range(6):
    for x in range(25):
        layer = 0
        while (layers[layer][y*25+x] == '2'):
            layer += 1
        if layers[layer][y*25+x] == '1':
            print(block_char, end="")
        else:
            print(" ", end="")
    print()

print(input())
