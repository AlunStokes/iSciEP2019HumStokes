import math

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