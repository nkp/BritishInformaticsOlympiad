#!/usr/bin/python

from collections import deque

def get_jug_value(state, i):
    return state >> i*16+8 & 0xFF

def get_jug_capacity(state, i):
    return state >> i*16 & 0xFF

def set_jug_value(state, i, v):
    state &= ~(0xFF << i*16+8)
    state |= v << i*16+8
    return state

def set_jug_capacity(state, i, v):
    state &= ~(0xFF << i*16)
    state |= v << i*16
    return state

def fill_jug(state, i):
    capacity = (state >> i*16) & 0xFF
    state &= ~(0xFF << i*16+8)
    state |= (capacity << i*16+8)
    return state

def empty_jug(state, i):
    return state & ~(0xFF << i*16+8)

def pour_jug(state, i, j):
    i_value = state >> i*16+8 & 0xFF
    j_value = state >> j*16+8 & 0xFF
    j_capacity = state >> j*16 & 0xFF
    to_pour = min(i_value, j_capacity - j_value)
    i_value -= to_pour
    j_value += to_pour
    state &= ~(0xFF << i*16+8) & ~(0xFF << j*16+8)
    state |= (i_value << i*16+8) | (j_value << j*16+8)
    return state

def initial_state(capacities):
    i = long()
    capacities = capacities[::-1]
    for capacity in capacities:
        i <<= 16
        i |= capacity
    return i

def num_jugs(state):
    if state > 4294967296: # Capacity for third jug > 0
        return 3
    if state > 65536: # Capacity for second jug > 0
        return 2
    return 1

def get_child_states(parent):
    states = []
    nJugs = num_jugs(parent)
    for i in xrange(nJugs):
        value, capacity = get_jug_value(parent, i), get_jug_capacity(parent, i)
        if value < capacity:
            states.append(fill_jug(parent, i))
        if value > 0:
            states.append(empty_jug(parent, i))
            for j in xrange(nJugs):
                if i == j or get_jug_value(parent, j) == get_jug_capacity(parent, j): continue 
                states.append(pour_jug(parent, i, j))
    return states

def bfs(origin, target):
    distances = {origin:0}
    q = deque([origin])
    while q:
        state = q.popleft()
        distance = distances[state]
        for i in xrange(3):
            if get_jug_value(state, i) == target:
                return distance
        children = get_child_states(state)
        for child in children:
            if not child in distances: # Ensure no cycles.
                distances[child] = distance + 1
                q.append(child)


if __name__ == '__main__':
    n_jugs, target = map(int, raw_input().split())
    origin = initial_state(map(int, raw_input().split()))
    print bfs(origin, target)

