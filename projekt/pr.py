import time
import random
import sys
import numpy as np
import math
from random import randint, uniform, choice

def read_input():
    temp = sys.stdin.readline().split()
    t,n,m = (int(temp[i]) for i in range(3))
    M = []
    for _ in range(n):
        line = sys.stdin.readline()
        M.append([line[i] for i in range(m)])
    line = sys.stdin.readline()
    Paths = list(line)[:-1]
    return t,n,m,M,Paths

def find_agent(x_map,n,m):
    for i in range(n):
        for j in range(m):
            if x_map[i][j] == '5':
                return [i,j]
    return [-1,-1]

def is_valid(where,position,x_map):
    if where == 'U' and x_map[position[0]][position[1]] != '3':
        if x_map[position[0]-1][position[1]] != '1' and x_map[position[0]-1][position[1]] != '3':
            return True      
    elif where == 'D' and x_map[position[0]][position[1]] != '3':
        if x_map[position[0]+1][position[1]] != '1' and x_map[position[0]+1][position[1]] != '3':
            return True    
    elif where == 'L' and x_map[position[0]][position[1]] != '2':
        if x_map[position[0]][position[1]-1] != '1' and x_map[position[0]][position[1]-1] != '2':
            return True    
    elif where == 'R' and x_map[position[0]][position[1]] != '2':
        if x_map[position[0]][position[1]+1] != '1' and x_map[position[0]][position[1]+1] != '2':
            return True
    return False

def is_back(move):
    if move == 'U':
        return 'D'
    elif move == 'D':
        return 'U'
    elif move == 'L':
        return 'R'
    elif move == 'R':
        return 'L'
    return 0

def is_stack(cur_step,position,x_map):
    steps = ['U','D','L','R']
    steps.pop(steps.index(is_back(cur_step)))
    for i in steps:
        if is_valid(i,position,x_map):
            return False
    return True

def finished(position_y, position_x, x_map):
    if x_map[position_y-1][position_x] == '8':
        return True
    if x_map[position_y+1][position_x] == '8':
        return True
    if x_map[position_y][position_x-1] == '8':
        return True
    if x_map[position_y][position_x+1] == '8':
        return True    
    return False

def make_random_moves(position, x_map, n, m, limit, moves):
    path = []
    where = ''
    prev = ''
    while len(path) <= limit:
        where = random.choice(moves)
        while not is_valid(where, position, x_map) or prev == is_back(where):
            if is_stack(where,position,x_map):
                return path
            where = random.choice(moves)
        prev = where
        r = random.randint(1, min(n, m))
        for _ in range(r):
            if not is_valid(where, position, x_map) or is_stack(where,position,x_map):
                break
            make_move(where, position)
            path.append(where)
            if finished(position[0], position[1], x_map):
                return path
    return path

def make_move(where, position):
    if where == 'U':
        position[0] -= 1
    elif where == 'D':
        position[0] += 1
    elif where == 'L':
        position[1] -= 1
    elif where == 'R':
        position[1] += 1

def check_path(position, path, x_map):
    count = 0
    for i in path:
        if is_valid(i,position,x_map):
            make_move(i,position)
            count += 1
        else:
            return False, 0
        if finished(position[0],position[1],x_map):
            return True, count
    return False, 0

def two_swap(path):
    if len(path) > 2:
        i = random.randint(0, len(path)-1)
        j = random.randint(0, len(path)-1)
        if i!=j:
            path[i],path[j] = path[j],path[i]

def two_del(path):
    if len(path) > 3:
        i = random.randint(0, len(path)-2)
        path.pop(i)
        path.pop(i)

def four_del(path):
    if len(path) > 6:
        i = random.randint(0, len(path)-4)
        for _ in range(4):
            path.pop(i)

def remove_blocks(path):
    if len(path) > 6:
        i = random.randint(0, len(path)-1)
        b = path[i]
        while i < len(path) and b == path[i]:
            path.pop(i)

def remove_opps(path):
    i = random.randint(0, len(path)//2)
    j = i+1
    while j < len(path) and i < len(path):
        if path[i] == is_back(path[j]) and len(path) > 3:
                path.pop(i)
                j -= 1
                path.pop(j)

        j += 1

def select(generation):
    generation.sort(key = lambda x: len(x))
    generation = generation[:len(generation)//2] + generation[3*(len(generation)//4):]

def recombine(generation):
    i = 1
    j = len(generation)-1
    while i < j:
        cur1 = generation[i]
        cur2 = generation[j]
        r1 = random.randint(1,min(len(cur1),len(cur2))//2)
        r2 = random.randint(r1,min(len(cur1),len(cur2)))
        res1 = cur1[:r1] + cur2[r1:r2] + cur1[r2:]
        res2 = cur2[:r1] + cur1[r1:r2] + cur2[r2:]
        generation[i] = res1
        generation[j] = res2
        i += 1
        j -= 1

def mutate(generation):

    mutations = [(two_swap,1), 
        (two_del,0.1), 
        (four_del,0.1), 
        (remove_blocks,0.1),
        (remove_opps, 0.1)]

    for g in generation[1:]:
        for m in mutations:
            if random.uniform(0,1) < m[1]:
                m[0](g)

def find_exit(x_map, n, m, t, position,starting_path):
    best_path = ['X' for _ in range(1000)]
    moves = ['U','D','L','R']
    start = time.time()
    generations = 25
    population = 7
    while time.time() - start < t:
        current_paths = [starting_path]
        for _ in range(population):
            pos = position.copy()
            path = []
            while not finished(pos[0],pos[1],x_map) and time.time() - start < t:
                pos = position.copy()
                path = make_random_moves(pos, x_map, n, m, max(n*m//4,max(n,m)),moves)
            current_paths.append(path)
        
        if time.time() - start >= t:
            return best_path

        generation = current_paths
        for _ in range(generations):

            select(generation)
            recombine(generation)
            mutate(generation)

            for path in generation:
                state, length = check_path(position.copy(), path, x_map)
                if state:
                    path = path[:length]
                    if len(path) < len(best_path):
                        best_path = path
            
        #print(len(best_path), time.time()-start)
            
    return best_path

def main():
    t,n,m,x_map,starting_path = read_input()
    agent = find_agent(x_map,n,m)
    p = find_exit(x_map,n,m,t,agent,starting_path)
    print(len(p))
    sys.stderr.write(''.join(p) + '\n')
if __name__ == "__main__":
    main()