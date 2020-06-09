import math
import random
import time
import sys

def h(x):
    alpha = 0.125
    a = (pow(x[0], 2) + pow(x[1], 2) + pow(x[2], 2) + pow(x[3], 2))

    left = pow((pow((a-4),2)),alpha)

    b = 0
    for i in range(4):
        b += x[i]
    
    return left + 0.25*(0.5*a + b) + 0.5

def g(x):
    x_sum = 0
    x_mul = 1
    for i in range(4):
        x_sum += pow(x[i], 2)
        x_mul *= math.cos(x[i]/math.sqrt(i+1))
    return 1 + x_sum/4000 - x_mul
    
def gen_neighbourhood(x, start, limit, inc):
    N = []   
    step = start
    while step < limit:
        N.append([x[0]+step, x[1], x[2], x[3]])
        N.append([x[0]-step, x[1], x[2], x[3]])
        N.append([x[0], x[1]+step, x[2], x[3]])
        N.append([x[0], x[1]-step, x[2], x[3]])
        N.append([x[0], x[1], x[2]+step, x[3]])
        N.append([x[0], x[1], x[2]-step, x[3]])
        N.append([x[0], x[1], x[2], x[3]+step])
        N.append([x[0], x[1], x[2], x[3]-step])
        step += inc
    return N

def choose_best(f, N):
    best = N[0]
    for i in range(len(N)):
        if f(N[i]) < f(best):
            best = N[i]
    return best

def gen_gradient(x, alpha):
    x1 = x[0] - alpha*((2*x[0]*(math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4))/math.pow((math.pow((math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4), 2)), 7//8)+x[0]+1)/4
    x2 = x[1] - alpha*((2*x[1]*(math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4))/math.pow((math.pow((math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4), 2)), 7//8)+x[1]+1)/4
    x3 = x[2] - alpha*((2*x[2]*(math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4))/math.pow((math.pow((math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4), 2)), 7//8)+x[2]+1)/4
    x4 = x[3] - alpha*((2*x[3]*(math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4))/math.pow((math.pow((math.pow(x[3], 2)+math.pow(x[0], 2)+math.pow(x[1], 2)+math.pow(x[2], 2)-4), 2)), 7//8)+x[3]+1)/4
    return [x1,x2,x3,x4]

def gen_rand_perm(low, high):
    return [random.uniform(low,high) for i in range(4)]

def minim_g(x,time_limit, limit, n_range, n_start, n_limit, n_inc, improvment):
    same = 0
    best = x
    val = g(x)
    o_start = n_start
    o_inc = n_inc
    time_delta = 0
    time_start = time.time()
    while time_delta < time_limit:
        
        if g(x) <= val:
            val = g(x)
            best = x
            same = 0
        else:
            same += 1

        for i in range(limit):

            N = gen_neighbourhood(x, n_start, n_limit, n_inc)
            x = choose_best(g, N)

            if N == []:
                break

            if g(x) < val:
                best = x
                val = g(x)
                same = 0
            else:
                same += 1
            
        x = gen_rand_perm(min(x)-n_range,max(x)+n_range)

        if same > improvment and n_start > 0.0001:
            n_start /= 2
            n_inc /= 2
        elif same == 0:
            n_start = o_start
            n_inc = o_inc

        if same > improvment*5:
            x = gen_rand_perm(min(x)-2*n_range,max(x)+2*n_range)
            n_start = o_start
            n_inc = o_inc

        
        time_delta = time.time() - time_start
    return best, val

def minim_h(x, time_limit, limit, alpha, n_range):
    start_time = time.time()
    val = h(x)
    n_start = n_range
    best = x
    same = 0
    mini = 0
    maxi = 0
    t = 0
    while t < time_limit:

        temp = h(x)
        cur_x = x
        for j in range(limit):
            old_minimum = temp
            cur_x = gen_gradient(cur_x,alpha)
            temp = h(cur_x)
            if old_minimum <= temp:
                break
            j += 1
            cur_min = temp

        if cur_min <= val:
            val = cur_min
            best = cur_x
            same = 0
        else:
            same += 1

        if same > 20 and n_range > 0.000001:
            n_range /= 2
        elif same == 0:
            n_range = n_start

        if same > 200:
            x = gen_rand_perm(-2, 0)
            same = 0
            n_range = n_start
        elif same < 50:
            cur_x = best
            mini = min(cur_x) - n_range
            maxi = max(cur_x) + n_range
            x = gen_rand_perm(mini, maxi)
        else:
            x = gen_rand_perm(mini*2, maxi*2)
            same = 0
            n_range = n_start

        t = time.time() - start_time

    return best, val

def main():
    #inp = input().split()
    #inp = sys.argv
    lines = []
    for line in sys.stdin:
        stripped = line.split()
        lines.append(stripped)
        break
    inp = lines[0]
    time_limit = int(inp[0])
    if inp[1] == '0':
        x = gen_rand_perm(-2, 0)
        vect, res = minim_h(x, time_limit, 100, 0.05, 0.01)
        sys.stdout.write(str(round(vect[0],15)) + ' ' + str(round(vect[1],15)) + ' ' + str(round(vect[2],15)) + ' ' + str(round(vect[3],15)) + ' ' + str(round(res,15))+ '\n')
    else:
        x = gen_rand_perm(-1, 1)
        vect, res = minim_g(x,time_limit, 5, 0.001, 0.001, 0.01, 0.0005, 100)
        sys.stdout.write(str(round(vect[0],15)) + ' ' + str(round(vect[1],15)) + ' ' + str(round(vect[2],15)) + ' ' + str(round(vect[3],15)) + ' ' + str(round(res,15))+ '\n')
if __name__ == "__main__":
    main()
