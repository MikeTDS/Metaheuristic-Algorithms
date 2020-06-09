import sys
import time
from random import randint, uniform

class Particle():
    def __init__(self, current_x, best_x, value, v):
        self.current_x = current_x
        self.best_x = best_x
        self.value = value
        self.v = v

eps = []
t = 0

def read_input():
    global eps
    global t
    raw = sys.stdin.readline().split()
    inp = [int(x) for x in raw[:6]]
    eps = [float(x) for x in raw[6:11]]
    t = inp[0]
    xs = inp[1:6]
    return xs

def f(x):
    return sum(eps[i]*abs(pow(x[i],i+1)) for i in range(5))

def rand_v():
    return [uniform(-2,2) for _ in range(5)]

def spawn(x, size):
    swarm = []
    particle = Particle(x,x,f(x),rand_v())
    swarm.append(particle)
    for i in range(size-1):
        xp = [uniform(min(x)-1, max(x)+1) for _ in range(5)]
        particle = Particle(xp,xp,f(xp),rand_v())
        swarm.append(particle)
        x = xp
    return swarm

def minim(xs, time_max):
    swarm = spawn(xs, 7)
    global_min_part = xs
    global_min = f(xs)
    alpha = 0.45
    beta = 2.2
    eta = 1.9
    start = time.time()
    while time.time() - start < t:

        for particle in swarm:
            val = f(particle.current_x)
            if val < particle.value:
                particle.value = val
                particle.best_x = particle.current_x.copy()
                if val < global_min:
                    global_min = val
                    global_min_part = particle.current_x.copy()

            for i in range(5):
                particle.v[i] = (alpha * particle.v[i])\
                            + uniform(0, beta)*(particle.best_x[i] - particle.current_x[i])\
                            + uniform(0, eta)*(global_min_part[i] - particle.current_x[i])

                particle.current_x[i] += particle.v[i]

        #print(global_min)
    global_min_part.append(global_min)

    return global_min_part


def main():
    global eps
    global t
    xs = read_input()
    res = minim(xs, time)
    for i in range(6):
        print(round(res[i],16), end=' ')
    print()

if __name__ == "__main__":
    main()
