import numpy as np
class curve:
    def __init__(self, slope, dim, numLines):
        self.lines = []
        self.slope = slope
        self.dim = dim
        self.numLines = numLines
    def addLines(self, lines):
        for i in lines:
            self.lines.append(i)
    def addLine(self, line):
        self.lines.append(line)
    def nextPoint(self, lineIndex, p0, initialOffset = 0):
        line = self.lines[lineIndex]
        d = self.distanceBetweenPoints(p0, line.getP1())
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
    def distanceBetweenPoints(self, p0, p1):
        return ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** (1 / 2)
    def getCoords(self):
        return self.coords
    def getLength(self):
        l = 0
        for i in self.lines:
            l += i.getLength()
        return l
    def __repr__(self):
        return str(self.lines)