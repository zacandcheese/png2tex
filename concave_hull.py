from enum import Enum, unique
import math
import numpy as np

def dot(coord1, coord2):
    (x1, y1) = coord1
    (x2, y2) = coord2
    return (x1 * x2) + (y1 * y2)

def distance(P1, P2, p):
    (x0, y0) = p
    (x1, y1) = P1
    (x2, y2) = P2
    
    return abs((x2 - x1)*(y1 - y0) - (x1 - x0)*(y2 - y1)) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def minus(P1, P2):
    return (P1[0] - P2[0], P1[1] - P2[1])

def cross(P1, P2):
    (x1, y1) = P1
    (x2, y2) = P2
    return (x1*y2) - (y1*x2)
    
def sign(x):
    if (x<0):
        return -1
    elif (x>0):
        return 1
    else:
        return 0
    
def line_side_test(P1, P2, P3):
    return sign(cross(minus(P2, P1), minus(P3, P1)))

@unique
class Curvage(Enum):
    Concave  = 1
    Line = 0
    Convex  = -1

class Geometry:
    def __init__(self, val):
        if (-0.5 < val < 0.5):
            self.cur = Curvage(0)
        else:
            self.cur = Curvage(sign(val))
        
    def __sub__(self, other):
        val1 = self.cur.value
        val2 = other.cur.value
        return abs(val2 - val1)
    
    def __str__(self):
        return self.cur.name
    
def line_type(segment):
    p1 = segment[0]
    p2 = segment[-1]
    x = sum(map(lambda p3: line_side_test(p1, p2, p3)  * distance(p1, p2, p3), segment))
    val = x / len(segment) #average rise over run
    return Geometry(val)

@unique
class Cardinal(Enum):
    N  = 0
    NE = 1
    E  = 2
    SE = 3
    S  = 4
    SW = 5
    W  = 6
    NW = 7

class Compass:
    def __init__(self, deg):
        temp = round(deg / 45, 0) % 8
        self.dir = Cardinal(temp)
        
    def __sub__(self, other):
        val1 = self.dir.value
        val2 = other.dir.value
        return min((val1 - val2) % 8, (val2 - val1) % 8)
    
    def __str__(self):
        return self.dir.name
    
def direction(P1, P2):
    (x,y) = minus(P2, P1)
    angle = math.atan2(x,y) * 180 / math.pi
    if angle < 0:
        angle = angle + 360 
    return Compass(angle)


def convert_border(border):
    borderxy = np.array([[x[1], x[0]] for x in border])
    segments = np.array_split(borderxy, 12)
    res = []
    for segment in segments:
        p1 = segment[0]
        p2 = segment[-1]
        res.append(tuple([line_type(segment), direction(p1, p2)]))
    return res
