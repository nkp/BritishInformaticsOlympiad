#!/usr/bin/python

class RailPoint:
    def __init__(self, name):
        self.name = name
        
    def set(self, straight, curve_left, curve_right):
        self.straight = straight
        self.curve_left = curve_left
        self.curve_right = curve_right
        # Default to the left curve.
        self.curve = self.curve_left

class LazyPoint(RailPoint):
    def next(self, previous):
        if previous == self.curve_left or previous == self.curve_right:
            # Approaching from a curved section of the track
            self.curve = previous
            return self.straight
        return self.curve

class FlipFlopPoint(RailPoint):
    def next(self, previous):
        if previous == self.curve_left or previous == self.curve_right:
            # Approaching from a curved section of the track.
            return self.straight
        result = self.curve
        self.curve = (self.curve==self.curve_left) and self.curve_right or self.curve_left
        return result
        
def create_graph(flip_flop_points):
    graph = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWX'
    for char in alphabet:
        graph[char] = FlipFlopPoint(char) if char in flip_flop_points else LazyPoint(char)
    
    # Node       # Straight  # Left      # Right
    graph['A'].set(graph['D'], graph['E'], graph['F'])
    graph['B'].set(graph['C'], graph['G'], graph['H'])
    graph['C'].set(graph['B'], graph['I'], graph['J'])
    graph['D'].set(graph['A'], graph['K'], graph['L'])
    graph['E'].set(graph['A'], graph['M'], graph['N'])
    graph['F'].set(graph['A'], graph['N'], graph['O'])
    graph['G'].set(graph['B'], graph['O'], graph['P'])
    graph['H'].set(graph['B'], graph['P'], graph['Q'])
    graph['I'].set(graph['C'], graph['Q'], graph['R'])
    graph['J'].set(graph['C'], graph['R'], graph['S'])
    graph['K'].set(graph['D'], graph['S'], graph['T'])
    graph['L'].set(graph['D'], graph['T'], graph['M'])
    graph['M'].set(graph['U'], graph['L'], graph['E'])
    graph['N'].set(graph['U'], graph['E'], graph['F'])
    graph['O'].set(graph['V'], graph['F'], graph['G'])
    graph['P'].set(graph['V'], graph['G'], graph['H'])
    graph['Q'].set(graph['W'], graph['H'], graph['I'])
    graph['R'].set(graph['W'], graph['I'], graph['J'])
    graph['S'].set(graph['X'], graph['J'], graph['K'])
    graph['T'].set(graph['X'], graph['K'], graph['L'])
    graph['U'].set(graph['V'], graph['M'], graph['N'])
    graph['V'].set(graph['U'], graph['O'], graph['P'])
    graph['W'].set(graph['X'], graph['Q'], graph['R'])
    graph['X'].set(graph['W'], graph['S'], graph['T'])
    return graph

def run_train(previous, next, n):
    for i in xrange(n):
        next, previous = next.next(previous), next
    return previous.name + next.name

if __name__ == '__main__':
    flip_flops = raw_input()
    previous, next = raw_input()
    n = int(raw_input())
    graph = create_graph(flip_flops)
    print run_train(graph[previous], graph[next], n)
    
