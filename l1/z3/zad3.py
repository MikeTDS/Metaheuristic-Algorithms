#from random_agent_map import gen_map, print_map
import time
import random
import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line)
    temp = lines[0].split()
    x_map = []
    t = int(temp[0])
    n = int(temp[1])
    m = int(temp[2])
    for i in range(1,n+1):
        x_map.append(lines[i][:-1])
    return t,n,m,x_map

def find_agent(x_map,n,m):
    for i in range(n):
        for j in range(m):
            if x_map[i][j] == '5':
                return i,j
    return -1,-1

def is_valid(where,position,nf,m,x_map):
    if finished(position[0], position[1],x_map):
        return False
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

def make_move(where,position):
    if where == 'U':
        cur_pos = position[0]-1,position[1]
    elif where == 'D':
        cur_pos = position[0]+1,position[1]
    elif where == 'L':
        cur_pos = position[0],position[1]-1
    elif where == 'R':
        cur_pos = position[0],position[1]+1
    return cur_pos

def finished(position_y, position_x, x_map):
    if x_map[position_y][position_x] == '8':
        return True
    return False

def make_random_moves(position, x_map,n,m, steps, moves):
    made_steps = 0
    path = []
    prev = ''
    way_limit = random.randint(1,min(n,m))
    while made_steps < steps:
        cur_step = random.choice(moves)
        while cur_step == is_back(prev) or not is_valid(cur_step,position,n,m,x_map):
            cur_step = random.choice(moves)

        for i in range(way_limit):
            if not is_valid(cur_step,position,n,m,x_map):
                break
            position = make_move(cur_step,position)
            made_steps += 1
            path.append(cur_step)
            prev = cur_step
            if finished(position[0],position[1],x_map):
                return position, path, made_steps

    return position, path, made_steps

def check_path(position, path, x_map,n,m):
    steps = 0
    for i in path:
        if is_valid(i,position,n,m,x_map):
            position = make_move(i,position)
            steps +=1
        else:
            return position, steps
    return position, steps

def two_swap(path,T,t_limit):
    N = []
    max = 10
    iter = 0
    for i in range(len(path)-1):
        for j in range(i+1,len(path)):
            if iter > max:
                return N
            copy = path[:]
            copy[i],copy[j] = copy[j],copy[i]
            if copy[:t_limit] not in T:
                N.append(copy)
                iter += 1
    return N

def find_best(N,pos,x_map,n,m,T,t_limit):
    best_path = []
    best_steps = 0
    for p in N:
        c_pos, steps = check_path(pos,p,x_map,n,m)
        if finished(c_pos[0],c_pos[1],x_map):
            if steps < best_steps or steps == 0:
                best_steps = steps
                best_path = p
        else:
            T.append(p[:t_limit])
    return best_path, best_steps

def find_exit(x_map,n,m,t,position):
    best_steps = 0
    best_path = []
    T= []
    t_limit = 5
    moves = ['U','D','L','R']

    steps = 0
    path = []
    limit = 10
    start_pos = position

    time_start = time.time()
    time_delta = 0


    while time_delta < t:
        pos = start_pos
        path = []
        while not finished(pos[0],pos[1],x_map) and time_delta < t:
            pos, cur_path, cur_made_steps = make_random_moves(pos,x_map,n,m,n*m,moves)
            steps += cur_made_steps
            path += cur_path
            time_delta = time.time() - time_start
        


        if (steps < best_steps and steps != 0) or best_steps == 0:
            best_steps = steps
            best_path = path

        N = two_swap(path,T,t_limit)

        if len(T) > 100:
            T = T[len(T)-100:]

        path, steps = find_best(N,pos,x_map,n,m,T,t_limit)

        if (steps < best_steps and steps != 0) or best_steps == 0:
            best_steps = steps
            best_path = path

        time_delta = time.time() - time_start

    return best_path, best_steps

def main():
    #inp = input().split()
    #real_inp = [int(x) for x in inp]
    #t = real_inp[0]
    #n = real_inp[1]
    #m = real_inp[2]
    #x_map = gen_map(n, m)
    #print_map(x_map)
    t,n,m,x_map = read_input()
    agent = find_agent(x_map,n,m)
    p,s = find_exit(x_map,n,m,t,agent)
    sys.stdout.write(str(s) + '\n')
    sys.stderr.write(''.join(p) + '\n')
if __name__ == "__main__":
    main()