import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

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
    l.append([p0,p1])
    while (i < iter - 1):
        p1 = nextPoint(p1, slope, dim)
        if (p1[0] == dim or p1[1] == dim):
            l[len(l) - 1].append(p1)
        if (i % 2 == 0):
            l.append([p1])
        i += 1
    plt.axis([0, dim, 0, dim])
    for j in l:
        x = []
        y = []
        for k in j:
            x.append(k[0])
            y.append(k[1])
        plt.plot(x,y)
    plt.show()

p0 = (0,0)
slope = math.sqrt(2)
dim = 1
iter = 5000

loop(p0, slope, dim, iter)


