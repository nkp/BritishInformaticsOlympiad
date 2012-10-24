#!/usr/bin/python
from operator import itemgetter
DIGITS = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']
INF = float('inf')

# Who cares about space in a BIO?
def memoize(f):
    mem = {}
    MEMOIZE_DEFAULT = '__MEMOIZE_DEFAULT__'
    def wrap(*args):
        value = mem.get(args, MEMOIZE_DEFAULT)
        if value is MEMOIZE_DEFAULT:
            value = f(*args)
            mem[args] = value
        return value
    return wrap

@memoize
def to_digit(n):
    # Convert integer `n` to its word form.
    s = ''
    if n == 0: s = DIGITS[n % 10]
    while n > 0:
        s = DIGITS[n % 10] + s
        n /= 10
    return s

def valid_transformation(n, m):
    # Returns true if the digit word for `n` can become the digit word for `m` 
    # by adding or removing 5 or fewer characters.
    digit_n = to_digit(n)
    digit_m = to_digit(m)
    count = 0
    for c in digit_n:
        if c in digit_m:
            digit_m = digit_m.replace(c, '', 1)
        else:
            count += 1
    count += len(digit_m)
    return count <= 5

def generate_graph():
    # Generate a graph for all possible number ladder steps.
    graph = {}
    for i in xrange(1, 1000):
        for j in xrange(i, 1000):
            if valid_transformation(i, j):
                if not i in graph: graph[i] = [INF, i, []]
                if not j in graph: graph[j] = [INF, j, []]
                graph[i][2].append(j)
                graph[j][2].append(i)
    return graph

def dijkstra(g, start, finish):
    # Based on dijkstra to return the fewest number of steps to get from 
    # `start` to `finish` on the number ladder.
    q = []
    for v in g.keys():
        if v == start: 
            g[v][0] = 0
        else: g[v][0] = INF
        q.append(g[v])

    while q:
        # Sorting the queue every time is not optimal, but very few verteces
        # and working to a time limit.
        q.sort(key=itemgetter(0)) # lambdas are slow
        dist, u, neighbours = q.pop(0)
        if dist == INF: break
        for v in neighbours:
            if dist + 1 < g[v][0]:
                g[v][0] = dist + 1
    return g[finish][0]

if __name__ == '__main__':
    g = generate_graph()
    tests = [map(int, raw_input().split(' ')) for i in xrange(3)]
    for s, f in tests:
        print dijkstra(g, s, f)

