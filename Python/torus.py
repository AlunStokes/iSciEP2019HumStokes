import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time
from util import *

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
    def __repr__(self):
        s = "{("
        s = s + str(self.p0[0]) + ", " + str(self.p0[1]) + "), "
        s = s + str(self.p1[0]) + ", " + str(self.p1[1]) + ")}"
        return s

class curve:
    def __init__(self, slope):
        self.lines = []
        self.slope = slope
    def addLines(self, lines):
        self.lines = lines
    def addLine(self, line):
        self.lines.append(line)
    def getLines(self):
        return self.lines
    def nextPoint(self, lineIndex, p0, initialOffset = 0):
        line = self.lines[lineIndex]
        d = dist(p0, line.getP1())
        if (d < self.subdiv):
            return d
        dx = np.cos(np.arctan(self.slope)) * (self.subdiv - initialOffset)
        dy = self.slope * dx
        return (p0[0] + dx, p0[1] + dy)
    def segmentCurve(self, subdiv):
        self.coords = []
        self.subdiv = subdiv
        i = 0
        lineIndex = 0
        p0 = self.lines[0].getP0()
        self.coords.append(p0)
        while (lineIndex < len(self.lines) - 1):
            nP = self.nextPoint(lineIndex, p0)
            while (isinstance(nP, (int, float))):
                if (lineIndex >= len(self.lines) - 1):
                    return self.coords
                lineIndex += 1
                initialOffset = np.cos(np.arctan(self.slope)) * nP
                nP = self.nextPoint(lineIndex, self.lines[lineIndex].getP0(), initialOffset)
            p0 = nP
            self.coords.append(p0)
            i += 1
        return self.coords
    def step(self, stepSize):
        return self.segmentCurve(self.subdiv + stepSize)
    def getCoords(self):
        return self.coords
    def __repr__(self):
        return str(self.lines)

def dist(p0, p1):
    return ((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)**(1/2)

def pointArrayToXY(pArr):
    x = []
    y = []
    for p in pArr:
        x.append(p[0])
        y.append(p[1])
    return (x,y)

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


def loop(p0, slope, dim, numLines):
    iter = 2 * numLines - 1
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
    '''
    for j in l:
        coords = j.getCoordArrays()
        x = coords[0]
        y = coords[1]
        plt.plot(x,y, linewidth = 0.5)
    plt.show()
    '''
    c = curve(slope)
    c.addLines(l)
    return c

def generateCurve(p0, slope, dim, numLines):
    return loop(p0, slope, dim, numLines)

p0 = (0,0)
slope = math.sqrt(2)
dim = 1
numLines = 500
segLen = 0.01
stepSize = 0.1
c = generateCurve(p0, slope, dim, numLines)
points = c.segmentCurve(segLen)


'''
ANIMATION CODE
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(0, 1), ylim=(0, 1))
line, = ax.plot([],[],"ro", ms=1)

def init():
    line.set_data([],[])
    return line,

def animate(i):
    p = c.step(stepSize)
    coords = pointArrayToXY(p)
    line.set_data(coords[0], coords[1])
    return line,


dt = 1./30
t0 = time()
animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 10, 1), blit=True, init_func=init)

plt.show()
'''

i = 0
while i < len(points):
    if (isPrime(i + 1)):
        plt.plot(points[i][0], points[i][1], "ro", ms=1)
    #plt.text(points[i][0], points[i][1], i + 1, fontsize=5)
    i += 1
props = dict(boxstyle='round', facecolor='wheat', alpha=0.1)
# place a text box in upper left in axes coords
plt.text(-0.05, dim + 0.1 * dim, "seg. len. = " + str(segLen), fontsize=14,
        verticalalignment='top', bbox=props)
plt.axis([0, dim, 0, dim])
plt.show()


