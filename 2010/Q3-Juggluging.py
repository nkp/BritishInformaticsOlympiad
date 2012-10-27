#!/usr/bin/python

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

def get_child_states(parent):
    states = []
    for i in xrange(3):
        value, capacity = get_jug_value(parent, i), get_jug_capacity(parent, i)
        if capacity == 0: continue # 0 capacity indicates no more jugs.
        if value < capacity:
            states.append(fill_jug(parent, i))
        if value > 0:
            states.append(empty_jug(parent, i))
            for j in xrange(3):
                if i == j or get_jug_capacity(parent, j) == 0: continue
                states.append(pour_jug(parent, i, j))
    return states

def dfs(origin, target, history, depth, max_depth):
    if depth == max_depth: 
        for i in xrange(3):
            if get_jug_value(origin, i) == target:
                return True 
        return False
    if origin in history and history[origin] <= depth:
        return False
    history[origin] = depth
    children = get_child_states(origin)
    for child in children:
        result = dfs(child, target, history, depth+1, max_depth)
        if result:
            return result

if __name__ == '__main__':
    n_jugs, target = map(int, raw_input().split())
    origin = initial_state(map(int, raw_input().split()))
    for max_depth in xrange(1, 251):
        if dfs(origin, target, {}, 0, max_depth):
            print max_depth
            break

