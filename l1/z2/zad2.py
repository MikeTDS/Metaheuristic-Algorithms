import random
#import tsp
#from random_map import generate_random_map
import math
import time
import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line)
    
    first = lines[0].split()
    t = int(first[0])
    n = int(first[1])
    x = []
    for i in range(1,n+1):
        row = []
        temp_row = lines[i].split()
        row = [int(x) for x in temp_row]
        x.append(row)
    return t, n, x

def convert_path(path):
    s = ''
    for i in path:
        s += str(i+1)
        s += ' '
    s += '1 \n'
    return s

def calc_distance(x,path):
    current = 0
    res = 0
    for i in range(len(path)+1):
        res += x[current][path[i%len(path)]]
        current = path[i%len(path)]
    return res

def distance(x, a, b):
    return x[a][b]

def find_first_path(x, limit):
    cities = list(range(len(x)))
    cities = cities[1:]
    path = [0]
    current = 0
    to_visit = -1
    for i in cities:
        best = -1
        val = float('inf')
        possible = [t for t in cities if t not in path]
        for c in possible:
            if 0 < x[current][c] < val:
                val = x[current][c]
                best = c
        path.append(best)
        current = best
    return path

def gen_rand_perm(n,seed,step,T_id):
    res = seed[:]
    for i in range(1,n,step):
        p = random.randint(1,i)
        if i not in T_id and p not in T_id:
            res[i],res[p] = res[p],res[i]
    return res

def two_opt(path, n, T):
    N = []
    for i in range(1, n-2):
        for j in range(i+1, n):
            if j == i+1:
                continue
            copy = path[:]
            copy[i:j] = copy[j-1:i-1:-1]
            if copy not in T:
                #print(copy)
                N.append(copy)
    return N

def two_swap(x, path, n, T, T_id, same_ids, limit_same_ids):
    N = []
    temp = calc_distance(x, path)
    val = temp
    best = path
    for i in range(1,n-1):
        if i not in T_id:
            for j in range(i+1,n):
                copy = path[:]
                copy[i],copy[j] = copy[j],copy[i]
                i_val = calc_distance(x, copy)
                if(i_val > temp):
                    same_ids[i] += 1
                    if same_ids[i] > limit_same_ids:
                        T_id.append(i)
                        break
                if copy not in T:
                    N.append(copy)
                    if(i_val < val):
                        val = i_val
                        best = copy

    return N, best, val
    
def find_best(x,N):
    best = N[0]
    val = calc_distance(x,N[0])
    for n in N:
        temp = calc_distance(x,n)
        if temp < val:
            val = temp
            best = n
    return best, val

#def find_best_pairs(x,path):
    
def minim_tabu(x, path, n, time_limit, explr, tabu, tabu_index, limit_same_ids):
    T = []
    T_id = []
    same_ids = [0 for i in range(n)]
    N = []
    val = calc_distance(x,path)
    best = path
    same = 0
    same_limit = 4*explr
    time_delta = 0
    time_start = time.time()
    
    while time_delta < time_limit:
        same = 0
        for i in range(explr):
            time_delta = time.time() - time_start
            if same > explr//2 or time_delta > time_limit:
                break

            N, path, temp = two_swap(x, path, n, T, T_id, same_ids, limit_same_ids)

            if N == []:
                break

            T += N
            if len(T) > tabu:
               T = T[len(T)-tabu:]
            
            if len(T_id) > tabu_index:
                for index in T_id[:len(T_id)-tabu_index-1]:
                    same_ids[index] = 0
                T_id = T_id[len(T_id)-tabu_index:]

            N = two_opt(path,n,T)
            if N!=[]:
                path, temp = find_best(x,N)

            if temp < val:
                val = temp
                best = path
                same = 0
            else:
                same += 1
        
        path = gen_rand_perm(n,path,random.randint(1,n),T_id)
        N = two_opt(path,n,T)
        if N!=[]:
                path, temp = find_best(x,N)
        N = two_opt(path,n,T)
        if N!=[]:
                path, temp = find_best(x,N)

        if temp < val:
            val = temp
            best = path

        time_delta = time.time() - time_start
        #print(val, T_id)
    return val, best

def main():
    time_limit,n,x = read_input()
    #inp = input().split()
    #time_limit = int(inp[0])
    #n = int(inp[1])
    explr = int(0.4*n)
    limit_same_ids = n**3/math.log(n)
    tabu_size = int(5*n**2/math.log(n))
    tabu_index_size = int(n//10)

    #x = generate_random_map(n)
    s2 = {(i,j):x[i][j] for i in range(n) for j in range(n)}

    path = find_first_path(x, n)
    v1, p1 = minim_tabu(x, path, n, time_limit,explr, tabu_size, tabu_index_size, limit_same_ids)
    sys.stdout.write(str(v1) + '\n')
    sys.stderr.write(convert_path(p1))
    
    #v2, p2 = tsp.tsp(range(n),s2)
    #print((v1,p1))
    #print((v2,p2))
    #print(str(v2/v1))

if __name__ == "__main__":
    main()
