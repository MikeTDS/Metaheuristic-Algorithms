from HMAP import HMAP
import sys
import time
import random

letters = []
points = []

def read_params():
    raw = sys.stdin.readline().split()
    params = [int(x) for x in raw]
    return params

def sort_letters():
    return [x for _,x in sorted(zip(points,letters), reverse=True)]

def sort_points():
    return sorted(points , reverse=True)

def prepare_dictionary(n,s,t,start):
    global letters
    global points
    hmap = HMAP()
    letters = ['' for _ in range(n)]
    points = [0 for _ in range(n)]
    starting = ['' for _ in range(s)]

    for i in range(n):
        temp = sys.stdin.readline().split()
        letters[i] = temp[0]
        points[i] = int(temp[1])
        if time.time() - start > t:
            break

    for i in range(s):
        temp = sys.stdin.readline()
        if temp[-1] == '\n':
            temp = temp[:-1]
        starting[i] = temp

    with open('dict.txt', 'r') as file:
        line = file.readline()
        while line != '':
            hmap.insert(line.lower()[:-1])
            if time.time() - start > t:
                break
            line = file.readline()

    return hmap, letters, points, starting

def random_words(letters, length, k):
    words = ['' for _ in range(k)]
    for i in range(k):
        random.shuffle(letters)
        words[i] = ''.join(letters[:length])
    return words

def random_with_base(base, letters, length, k):
    base = list(base)
    words = ['' for _ in range(k)]
    for l in base:
        letters.remove(l)
    for i in range(k):
        random.shuffle(letters)
        ext = letters[:length-len(base)]
        ext += base
        random.shuffle(ext)
        words[i] = ''.join(ext)
    return words

def sort_by_points(words):
    return sorted(words, key=f, reverse=True)

def recombination(words):
    to_rec = words[:]
    res = []
    while to_rec != []:
        w1 = random.choice(to_rec)
        to_rec.remove(w1)
        if to_rec == []:
            break
        w2 = random.choice(to_rec)
        to_rec.remove(w2)
        if len(w1) > len(w2):
            w1,w2 = w2,w1
        if len(w1) > 3 and len(w2) > 3:
            i = random.randint(0, len(w1)-2)
            j = random.randint(i+1, len(w2)-1)
            res.append(w1[:i] + w2[i:j] + w1[j:])
            res.append(w2[:i] + w1[i:j] + w2[j:])
    return res

def two_swap(word):
    i = random.randint(0, len(word)-2)
    j = random.randint(i+1, len(word)-1)
    temp = list(word)
    temp[i],temp[j]=temp[j],temp[i]
    word = ''.join(temp)
    return word

def transposition(words):
    to_trans = words[:]
    res = []
    for w in to_trans:
        if len(w) > 3:
            for i in range(random.randint(1,len(w)//2)):
                w = two_swap(w)
            res.append(w)
    return res

def inversion(words):
    to_inv = words[:]
    res = []
    for w in to_inv:
        if len(w) > 3:
            i = random.randint(0, len(w)-2)
            j = random.randint(i+1, len(w)-1)
            temp = w[i:j]
            temp = temp[::-1]
            res.append(w[:i] + temp + w[j:])
    return res

def f(word):
    return sum(points[letters.index(w)] for w in word)

def is_ok(word):
    letters_copy = letters[:]
    for l in word:
        if l in letters_copy:
            letters_copy.remove(l)
        else:
            return False
    return True

def find_word(start,t,hmap,starting):
    global letters
    global points
    letters = sort_letters()
    points = sort_points()

    best_word = starting[0]
    total_points = f(best_word)

    words_len = len(letters)
    words_count = len(letters)
    generations = 10
    generation = []
    while time.time() - start < t:
        words = random_words(letters[:], words_len, words_count)
        words += starting
        words = sort_by_points(words)
        selected = words[:len(words)//2]
        chosen = []
        for word in words:
            for i in range(1,len(word)):
                w = word[:i]
                if hmap.find(w) and w:
                    val = f(w)
                    if val > total_points:
                        total_points = val
                        best_word = w
                    chosen.append(w)

        generation = selected + chosen
        chosen = []

        for i in range(generations):
            if time.time() - start > t:
                return best_word, total_points
            new_generation = recombination(generation)
            new_generation += transposition(generation)
            new_generation += inversion(generation)
            for word in new_generation:
                if time.time() - start > t:
                    return best_word, total_points
                for i in range(1,len(word)):
                    if time.time() - start > t:
                        return best_word, total_points
                    w = word[:i]
                    if is_ok(w) and hmap.find(w):
                        val = f(w)
                        if val > total_points:
                            total_points = val
                            best_word = w
                        chosen.append(w)
            generation = new_generation 
            generation = sort_by_points(generation)
            chosen = [c+random.choice(letters) for c in chosen]
            generation = generation[:20] + chosen
            chosen = []
        
        if words_count < 100:
            words_count = int(2*words_count)
        else:
            words_count = len(letters)

        #print(total_points, best_word)

    return best_word, total_points

def main():
    global points
    global letters
    p = read_params()
    t = p[0]
    n = p[1]
    s = p[2]
    start = time.time()
    hmap, letters, points, starting = prepare_dictionary(n,s,t,start)
    word, points = find_word(start,t,hmap,starting)
    print(points)
    sys.stderr.write(word)

if __name__ == "__main__":
    main()