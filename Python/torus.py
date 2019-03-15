import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

class line:
    def __init__(self):
        pass
    def getLength(self):
        return math.sqrt((self.p1[0] - self.p0[0])**2 + (self.p1[1] - self.p0[1])**2)
    def getCoordArrays(self):
        x = [self.p0[0], self.p1[0]]
        y = [self.p0[1], self.p1[1]]
        return (x, y)
    def setP0(self, p0):
        self.p0 = p0
    def setP1(self, p1):
        self.p1 = p1
    def setP(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
    def getP0(self):
        return self.p0
    def getP1(self):
        return self.p1


def nextIntersection(p0, slope, dim):
    x0 = p0[0]
    y0 = p0[1]
    dx = (dim - y0)/slope + x0
    dy = slope * (dim - x0) + y0
    if (dx < dy):
        return (dx, dim)
    elif(dy < dx):
        return (dim, dy)
    else:
        return (dim, dim)

def nextPoint(p0, slope, dim):
    if (p0[0] == dim and p0[1] == dim):
        return (0,0)
    elif (p0[0] == dim):
        return (0, p0[1])
    elif (p0[1] == dim):
        return (p0[0], 0)
    else:
        return nextIntersection(p0, slope, dim)


def loop(p0, slope, dim, iter):
    l = []
    i = 0
    p1 = nextPoint(p0, slope, dim)
    l.append(line())
    l[0].setP(p0, p1)
    while (i < iter - 1):
        p1 = nextPoint(p1, slope, dim)
        if (p1[0] == dim or p1[1] == dim):
            l[len(l) - 1].setP1(p1)
        if (i % 2 == 0):
            l.append(line())
            l[len(l) - 1].setP0(p1)
        i += 1
    plt.axis([0, dim, 0, dim])
    for j in l:
        coords = j.getCoordArrays()
        x = coords[0]
        y = coords[1]
        plt.plot(x,y, linewidth = 0.5)
    #plt.savefig("test.png", dpi = 600)
    plt.show()

p0 = (0,0)
slope = math.sqrt(2)
dim = np.pi
#iter must be odd in order to have all lines with endpoints
iter = 21

loop(p0, slope, dim, iter)



