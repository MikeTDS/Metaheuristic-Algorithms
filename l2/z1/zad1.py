import random
import time
import math
import sys
import numpy as np

def read_data():
    temp = sys.stdin.readline()
    temp = temp.split()
    for i in range(5):
        temp[i] = int(temp[i])
    return temp

def f(x):
    sqrt_sum = 0
    for i in range(4):
        sqrt_sum += pow(x[i],2)
    sqrt_sum = math.sqrt(sqrt_sum)
    return round((1 - math.cos(2*math.pi*sqrt_sum) + 0.1*sqrt_sum),16)

def gen_N(x,step,limit):
    N = []
    while step < limit:
        N.append([x[0]+step, x[1], x[2], x[3]])
        N.append([x[0]-step, x[1], x[2], x[3]])
        N.append([x[0], x[1]+step, x[2], x[3]])
        N.append([x[0], x[1]-step, x[2], x[3]])
        N.append([x[0], x[1], x[2]+step, x[3]])
        N.append([x[0], x[1], x[2]-step, x[3]])
        N.append([x[0], x[1], x[2], x[3]+step])
        N.append([x[0], x[1], x[2], x[3]-step])
        step += 0.1
    return N

def find_best(N):
    best = N[0]
    val = 1000000
    for x in N:
        if f(x) < val:
            best = x
            val = f(x)
    return best

def find_xp(T,c,N,x0):
    for n in N:
        df = f(n)-f(x0)
        r = random.uniform(0,1)
        if p(df, T,c) > r: 
            return n

def p(df, T,c):
    if df < 0:
        return 1
    x = np.exp(-df/T)
    return x

def sa(T0,c,x0,t):
    T = T0
    alpha = 0.01
    same = 0
    f0 = f(x0)
    delta = 0
    start = time.time()
    best = x0
    val = f0
    xp = x0
    rangee = 1
    while T > 0 and delta < t:

        if same > 10:
            same = 0
            T *= 10
            rangee *= 0.5

        df = f(xp)-f(x0)

        if df == 0.0:
            if min(xp) != max(xp):
                xp = [random.uniform(min(xp)*rangee,max(xp)) for i in range(4)]
            else:
                xp = [random.uniform(-max(xp)*rangee,max(xp)) for i in range(4)]
        
        #1
        # N = gen_N(xp,min(xp),max(xp))
        # if N != []:
        #     old = xp[:]
        #     xp = find_best(N) 
        #     if f(old) <= f(xp):
        #         xp = find_xp(T,c,N,x0)
        #         if xp is None:
        #             if min(x0) != max(x0):
        #                 xp = [random.uniform(min(x0),max(x0)) for i in range(4)]
        #             else:
        #                 xp = [random.uniform(-max(x0),max(x0)) for i in range(4)]
        
        #2
        N = gen_N(xp,min(xp),max(xp))
        if N != []:
            xp = find_xp(T,c,N,x0)
            if xp is None:
                if min(x0) != max(x0):
                    xp = [random.uniform(min(x0)*rangee,max(x0)) for i in range(4)]
                else:
                    xp = [random.uniform(-max(x0)*rangee,max(x0)) for i in range(4)]
        
        

        if f(xp) == 0.0:
            return xp

        df = f(xp)-f(x0)
        r = random.uniform(0,1)
        if p(df, T,c) > r: 
            x0 = xp
            if f(x0) < val:
                val = f(x0)
                best = x0
            if f0 < f(x0):
                T = T*c
            else:
                T = T/(c*T + 1)
        else:
            same += 1
        
        delta = time.time()-start
        if f(x0) == 0.0:
            return x0
       # print(val)
    return best

def main():
    data = read_data()
    t = data[0]
    x0 = data[1:5]
    T0 = abs(max(x0))
    c = 0.8
    x = sa(T0,c,x0,t)
    x = [round(i,15) for i in x]
    for i in x:
        print(str(i), end=' ')
    print(str(f(x)))
if __name__ == "__main__":
    main()