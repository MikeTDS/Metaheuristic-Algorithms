import sys
import random
import copy
import math
import time
import numpy as np

def read_input():
    temp = sys.stdin.readline().split()
    t,n,m,k = (int(temp[i]) for i in range(4))
    M = []
    for i in range(n):
        line = sys.stdin.readline().split()
        M.append([int(line[i]) for i in range(m)])
    return t,n,m,k,M

def cost(M, Mp, n, m):
    summ = 0
    for i in range(n):
        for j in range(m):
            summ += pow((M[i][j]-Mp[i][j]),2)
    return summ/(n*m)

def find_closest(avg,vals):
    x = min(vals, key = lambda x:abs(x-avg))
    return x 

def gen_first_blocks(n,m,k,ver):
    blocks = []
    if ver == 0:
        for i1 in range(0,n-k+1,k):
            for i2 in range(0,m-k+1,k):
                if (i1+2*k) <= n and (i2+2*k) <= m:
                    blocks.append([i1,i2,i1+k-1,i2+k-1])
                elif (i1+2*k) <= n and (i2+2*k) > m:
                    blocks.append([i1,i2,i1+k-1,m-1])
                elif (i1+2*k) > n and (i2+2*k) <= m:
                    blocks.append([i1,i2,n-1,i2+k-1])
                else:
                    blocks.append([i1,i2,n-1,m-1])
    elif ver == 1:
        for i1 in range(0,n-k+1,k):
            for i2 in range(m-k,-1,-k):
                if (i1+2*k) <= n and (i2-k) >= 0:
                    blocks.append([i1,i2,i1+k-1,i2+k-1])
                elif (i1+2*k) <= n and (i2-k) < 0:
                    blocks.append([i1,0,i1+k-1,i2+k-1])
                elif (i1+2*k) > n and (i2-k) >= 0:
                    blocks.append([i1,i2,n-1,i2+k-1])
                else:
                    blocks.append([i1,0,n-1,i2+k-1])
    if ver == 2:
        for i1 in range(n-k,-1,-k):
            for i2 in range(0,m-k+1,k):
                if (i1-k) >=0 and (i2+2*k) <= m:
                    blocks.append([i1,i2,i1+k-1,i2+k-1])
                elif (i1-k) >= 0 and (i2+2*k) > m:
                    blocks.append([i1,i2,i1+k-1,m-1])
                elif (i1-k) < 0 and (i2+2*k) <= m:
                    blocks.append([0,i2,i1+k-1,i2+k-1])
                else:
                    blocks.append([0,i2,i1+k-1,m-1])
    
    if ver == 3:
        for i1 in range(n-k,-1,-k):
            for i2 in range(m-k,-1,-k):
                if (i1-k) >=0 and (i2-k) >= 0:
                    blocks.append([i1,i2,i1+k-1,i2+k-1])
                elif (i1-k) >= 0 and (i2-k) < 0:
                    blocks.append([i1,0,i1+k-1,i2+k-1])
                elif (i1-k) < 0 and (i2-k) >= 0:
                    blocks.append([0,i2,i1+k-1,i2+k-1])
                else:
                    blocks.append([0,0,i1+k-1,i2+k-1])

    return blocks

def gen_random_mp(Mp,blocks,values):
    for block in blocks:
        Mp = fill_block(block,random.choice(values),Mp)
    return Mp

def get_block_size(block):
    return ((block[2]-block[0]+1)*(block[3]-block[1]+1))

def get_big_blocks(blocks):
    big = []
    min_size = get_block_size(blocks[0])
    for i in range(len(blocks)):
        if get_block_size(blocks[i]) > min_size:
            big.append(i)
    return big

def avg_block(block,M):
    summ = 0
    for i1 in range(block[0],block[2]+1):
        for i2 in range(block[1],block[3]+1):
            summ += M[i1][i2]
    avg = summ / get_block_size(block)
    return avg

def fill_block(block,value,Mp):
    for i1 in range(block[0],block[2]+1):
        for i2 in range(block[1],block[3]+1):
            Mp[i1][i2] = value
    return Mp

def fill_array(Mp,M,blocks,values):
    for block in blocks:
        avg = avg_block(block,M)
        val = find_closest(avg,values)
        Mp = fill_block(block,val,Mp)
    return Mp

def move_block(blocks,big_blocks):
    if big_blocks != []:
        idd = random.choice(big_blocks)
        if idd in big_blocks:
            move_big_block(idd,blocks)

def move_big_block(idd,blocks):
    dirs = ['U','D','R','L']
    dirr = random.choice(dirs)
    swap_neighbours(idd,blocks,dirr)

def swap_neighbours(idd,blocks,dirr):
    current = blocks[idd]
    if dirr == 'U':
        c_side = current[2]-current[0]+1
        for i in range(len(blocks)):
            b = blocks[i]
            b_side = b[2]-b[0]+1
            if b[1] == current[1] and b[3] == current[3] and b[0]==current[0]-b_side and b[2]==current[2]-c_side:
                current = [current[0]-b_side, current[1], current[2]-b_side, current[3]]
                b = [b[0]+c_side, b[1], b[2]+c_side, b[3]]
                blocks[idd] = current
                blocks[i] = b
                break

    elif dirr == 'D':
        c_side = current[2]-current[0]+1
        for i in range(len(blocks)):
            b = blocks[i]
            b_side = b[2]-b[0]+1
            if b[1] == current[1] and b[3] == current[3] and b[0]==current[0]+c_side and b[2]==current[2]+b_side:
                current = [current[0]+b_side, current[1], current[2]+b_side, current[3]]
                b = [b[0]-c_side, b[1], b[2]-c_side, b[3]]
                blocks[idd] = current
                blocks[i] = b
                break

    if dirr == 'L':
        c_side = current[3]-current[1]+1
        for i in range(len(blocks)):
            b = blocks[i]
            b_side = b[3]-b[1]+1
            if b[0] == current[0] and b[2] == current[2] and b[1]==current[1]-b_side and b[3]==current[3]-c_side:
                current = [current[0], current[1]-b_side, current[2], current[3]-b_side]
                b = [b[0], b[1]+c_side, b[2], b[3]+c_side]
                blocks[idd] = current
                blocks[i] = b
                break

    elif dirr == 'R':
        c_side = current[3]-current[1]+1
        for i in range(len(blocks)):
            b = blocks[i]
            b_side = b[3]-b[1]+1
            if b[0] == current[0] and b[2] == current[2] and b[1]==current[1]+c_side and b[3]==current[3]+b_side:
                current = [current[0], current[1]+b_side, current[2], current[3]+b_side]
                b = [b[0], b[1]-c_side, b[2], b[3]-c_side]
                blocks[idd] = current
                blocks[i] = b
                break
    
def p(df, T,c):
    x = np.exp(-(df/T))
    return x

def check_if_ok(blocks1, blocks2):
    b1s = []
    b2s = []
    for b in blocks1:
        if get_block_size(b) not in b1s:
            b1s.append(get_block_size(b))
    for b in blocks2:
        if get_block_size(b) not in b2s:
            b2s.append(get_block_size(b))
    print(b1s,b2s)

def minim_cost(M,Mp,t,n,m,k,blocks,values,finish):
    big_blocks = get_big_blocks(blocks)
    T = 1000
    c = 0.8
    starting = blocks[:]
    val = cost(M,Mp,n,m)
    best = copy.deepcopy(Mp)
    M0 = copy.deepcopy(Mp)
    start = time.time()
    delta = 0
    same = 0
    rangee = 10
    version = [0,1,2,3]
    while T>0 and delta < finish:
        N = []

        if same > 10:
            same = 0
            if version != []:
                v = random.choice(version)
                version.pop(version.index(v))
                blocks = gen_first_blocks(n,m,k,v)
            else:
                version = [0,1,2,3]
            T = 1000
            rangee = 10

        for i in range(15):
            temp = blocks[:]
            r = random.randint(1,rangee)
            for i in range(r):
                move_block(temp,big_blocks)
            N.append(temp)
        
        for b in N:
            Mp = fill_array(Mp,M,b,values)
            df = cost(M,Mp,n,m)-cost(M,M0,n,m)
            if df < 0:
                blocks = b
                M0 = fill_array(M0,M,blocks,values)
                cst = cost(M,M0,n,m)
            else:
                r = random.uniform(0,1)
                if p(df, T,c) > r:
                    if T > 10:
                        T = T*c
                    elif 10 > T > 0.000001:
                        T = T/(T*c+1)
                    else:
                        T = 10
                    if rangee > 5:
                        rangee -= 1
                    blocks = b
                    M0 = fill_array(M0,M,blocks,values)
                    cst = cost(M,M0,n,m)
                    if cst < val:
                        val = cst
                        best = copy.deepcopy(M0)
                        same = 0
                    break
                else:
                    same += 1
        #print(val)
        delta = time.time() - start
    #check_if_ok(starting, blocks)
    return best

def main():
    t,n,m,k,M = read_input()
    values = [0,32,64,128,160,192,223,255]
    blocks = gen_first_blocks(n,m,k,0)
    Mp = [[0 for i in range(m)] for i in range(n)]
    Mp = fill_array(Mp,M,blocks,values)
    best = minim_cost(M,Mp,t,n,m,k,blocks,values,t)
    cst = cost(M,best,n,m)
    sys.stdout.write(str(cst) + '\n')
    for row in best:
        for x in row:
            sys.stderr.write(str(x) + ' ')
        sys.stderr.write('\n')
    

if __name__ == "__main__":
    main()