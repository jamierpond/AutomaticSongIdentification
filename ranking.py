

def rank(inp):
    count = 0
    output = []
    input_length = len(inp)
    while len(output) != input_length:
        max_idx = 0
        for i in range(len(inp)):
            max_idx = i if inp[max_idx][1] <= inp[i][1] else max_idx
        output.append([count + 1, inp[max_idx][0], inp[max_idx][1]])
        inp.remove(inp[max_idx])
        count += 1
    return output

#
# listy = [  ['pop.00009.wav', 4],
#            ['pop.00038.wav', 4],
#            ['pop.00068.wav', 4],
#            ['pop.00087.wav', 4],
#            ['pop.00090.wav', 3],
#            ['classical.00000.wav', 7],
#            ['classical.00030.wav', 3],
#            ['classical.00047.wav', 4],
#            ['classical.00048.wav', 3],
#            ['classical.00050.wav', 3]]
#
# print(rank(listy))