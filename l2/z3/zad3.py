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
    for i in range(n):
        line = sys.stdin.readline()
        M.append([line[i] for i in range(m)])
    return t,n,m,M

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
    for i in path:
        if is_valid(i,position,x_map):
            make_move(i,position)
        else:
            return False
        if finished(position[0],position[1],x_map):
            return True
    return False

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

def p(df, T):
    return np.exp(-(df/T))

def find_exit(x_map, n, m, t, position):
    best_path = []
    T = 1000
    c = 0.8
    n_search = 0
    moves = ['U','D','L','R']
    time_delta = 0
    N_size = 20
    start = time.time()
    while time_delta < t:
        pos = position.copy()
        path = []
        while not finished(pos[0],pos[1],x_map) and time_delta < t:
            pos = position.copy()
            path = make_random_moves(pos, x_map, n, m, max(n*m//4,max(n,m)),moves)

        if len(path) < len(best_path) or len(best_path) == 0:
            best_path = path.copy()
            N_size = len(best_path)
        
        for i in range(N_size):
            pathp = find_p(path)
            found_escape = check_path(position.copy(), pathp, x_map)
            if found_escape:
                r = random.uniform(0, 1)
                df = len(pathp) - len(path)
                if df < 0:
                    path = pathp.copy()
                else:
                    if p(df, T) > r:
                        path = pathp.copy()
                T = T/(T*c+1)
            

        print(len(best_path))
        time_delta = time.time() - start

    return best_path

def main():
    t,n,m,x_map = read_input()
    agent = find_agent(x_map,n,m)
    p = find_exit(x_map,n,m,t,agent)
    sys.stdout.write(str(len(p)) + '\n')
    sys.stderr.write(''.join(p) + '\n')
if __name__ == "__main__":
    main()