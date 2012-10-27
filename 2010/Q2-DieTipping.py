#!/usr/bin/python
import sys

class Grid:
    cells = []
    
    def __init__ (self):
        self.cells = [[1]*11 for i in xrange(11)]

    def read(self, Input):
        for y in xrange(4, 7):
            for x in xrange(4, 7):
                self.set_cell(x, y, Input[y-4][x-4])
    
    def get_cell(self, x, y):
        return self.cells[y][x]
    
    def set_cell(self, x, y, var):
        self.cells[y][x] = var

    def print_cells_about_point (self, x, y):
        for _y in xrange(y-1, y+2):
            Row = ''
            for _x in xrange(x-1, x+2):
                if _x > 10 or _x < 0 or _y > 10 or _y < 0:
                    Row += 'X'
                else:
                    Row += str(self.get_cell(_x, _y))
            print Row
                        
class Die:
    x = 5
    y = 5
    top = 1
    bottom = 6
    front = 2
    back = 5
    left = 3
    right = 4
    directions = {'N':[0, -1], 'E':[1, 0], 'S':[0, 1], 'W':[-1, 0]}
    map_90 = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
    heading = 'N'
    grid = Grid()
    
    def move (self):
        delta = self.directions[self.heading]
        self.x += delta[0]
        self.y += delta[1]
        if self.x > 10:
            self.x = 0
        if self.x < 0:
            self.x = 10
        if self.y > 10:
            self.y = 0
        if self.y < 0:
            self.y = 10     
        self.orientate()
    
    def orientate (self):
        old_top = self.top
        if self.heading == 'N':
            self.top = self.back
            self.back = self.bottom
            self.bottom = self.front
            self.front = old_top
        elif self.heading == 'E':
            self.top = self.left
            self.left = self.bottom
            self.bottom = self.right
            self.right = old_top
        elif self.heading == 'S':
            self.heading = 'N'
            self.orientate()
            self.orientate()
            self.orientate()
            self.heading = 'S'
        elif self.heading == 'W':
            self.heading = 'E'
            self.orientate()
            self.orientate()
            self.orientate()
            self.heading = 'W'          
    
    def rotate_90 (self):
        self.heading = self.map_90[self.heading]
    
    def tick (self):
        # Step 1
        Total = self.top + self.grid.get_cell(self.x, self.y)
        if Total > 6:
            Total -= 6
        # Step 2
        self.grid.set_cell(self.x, self.y, Total)
        # Step 3
        if Total == 2:
            self.rotate_90()
        elif Total == 3 or Total == 4:
            self.rotate_90()
            self.rotate_90()
        elif Total == 5:
            self.rotate_90()
            self.rotate_90()
            self.rotate_90()
        self.move()
    
    def show (self):
        self.grid.print_cells_about_point(self.x, self.y)

    def next (self, n):
        for i in xrange(n):
            self.tick()

if __name__ == '__main__':
    grid = []
    for i in xrange(3):
        grid.append([ int(x) for x in raw_input().split(' ') ])
    d = Die()
    d.grid.read(grid)
    while 1:
        movesStr = raw_input()
        try:
            moves = int(movesStr)
        except ValueError:
            pass
        else:
            if moves > 0 and moves <= 100:
                d.next(moves)
                d.show()
            elif not moves:
                sys.exit(0)
        
