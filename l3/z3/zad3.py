import time
import random
import sys
import numpy as np
import math
from random import randint, uniform, choice

def read_input():
    temp = sys.stdin.readline().split()
    t,n,m,s,p = (int(temp[i]) for i in range(5))
    M = []
    Paths = []
    for i in range(n):
        line = sys.stdin.readline()
        M.append([line[i] for i in range(m)])
    for i in range(s):
        line = sys.stdin.readline()
        Paths.append(list(line)[:-1])
    return t,n,m,M,Paths,p

def find_agent(x_map,n,m):
    for i in range(n):
        for j in range(m):
            if x_map[i][j] == '5':
                return [i,j]
    return [-1,-1]

def is_valid(where,position,x_map):
    if where == 'U':
        if x_map[position[0]-1][position[1]] != '1':
            return True      
    elif where == 'D':
        if x_map[position[0]+1][position[1]] != '1':
            return True    
    elif where == 'L':
        if x_map[position[0]][position[1]-1] != '1':
            return True    
    elif where == 'R':
        if x_map[position[0]][position[1]+1] != '1':
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
        for i in range(r):
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

def mutate(generation):
    res = []
    for g in generation:
        temp = g[:]
        two_swap(temp)
        res.append(temp)
        temp = g[:]
        two_del(temp)
        res.append(temp)
    return res

def two_swap(path):
    i = random.randint(0, len(path)-1)
    j = random.randint(0, len(path)-1)
    if i!=j:
        path[i],path[j] = path[j],path[i]

def two_del(path):
    if len(path) > 3:
        i = random.randint(0, len(path)-2)
        path.pop(i)
        path.pop(i)

def find_p(real_path):
    path = real_path.copy()
    gen_type = random.randint(0, 1)
    if gen_type == 0:
        two_swap(path)
    if gen_type == 1:
        two_del(path)
    return path

def find_exit(x_map, n, m, t, position,starting_paths,population):
    best_path = ['X' for _ in range(1000)]
    moves = ['U','D','L','R']
    start = time.time()
    generations = 10
    while time.time() - start < t:
        current_paths = starting_paths
        for _ in range(population-len(starting_paths)):
            pos = position.copy()
            path = []
            while not finished(pos[0],pos[1],x_map) and time.time() - start < t:
                pos = position.copy()
                path = make_random_moves(pos, x_map, n, m, max(n*m//4,max(n,m)),moves)
            current_paths.append(path)

        generation = current_paths
        for i in range(generations):
            next_generation = mutate(generation)
            for path in next_generation:
                state, length = check_path(position.copy(), path, x_map)
                if state:
                    path = path[:length]
                    if len(path) < len(best_path):
                        best_path = path
            generation = next_generation
            print(len(best_path))

        
    return best_path

def main():
    t,n,m,x_map,starting_paths,p = read_input()
    agent = find_agent(x_map,n,m)
    p = find_exit(x_map,n,m,t,agent,starting_paths,p)
    print(len(p))
    sys.stderr.write(''.join(p) + '\n')
if __name__ == "__main__":
    main()