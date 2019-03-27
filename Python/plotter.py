import os
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from util import *
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path


class SelectFromCollection(object):
    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        self.poly = PolygonSelector(ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.poly.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

def lookup(dictionary, keyArr):
    if (type(keyArr[len(keyArr) - 1]) in [list, np.ndarray]):
       keyArr = totuple(keyArr)
    l = []
    for i in keyArr:
        l.append(dictionary[i])
    return l

class plotter:
    def __init__(self, curve, path):
        self.curve = curve
        self.path = path
        self.folderName = str(curve.slope) + "|" + str(curve.numLines)
        if not os.path.exists(path + "/" + self.folderName):
            os.mkdir(path + "/" + self.folderName)
    def plotLines(self, show = False):
        plt.figure(figsize=(5, 5), dpi=400)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        for j in self.curve.lines:
            coords = j.getCoordArrays()
            x = coords[0]
            y = coords[1]
            plt.plot(x, y, linewidth=0.5)
        plt.savefig(self.path + "/" + self.folderName + "/line.eps")
        if (show):
            plt.show()
        plt.close()
    def plotSegmentedPrime(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            if (isPrime(i + 1)):
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        plt.plot(X, Y, "b.", ms=0.1)
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|prime"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()

    def plotSegmentedComp(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            if (not isPrime(i + 1)):
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        plt.plot(X, Y, "b.", ms=0.1)
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|comp"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()

    def plotSegmentedPrimeWithPicker(self, segLen):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            if (isPrime(i + 1)):
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        data = np.column_stack((X,Y))
        primeMap = {}
        i = 0
        primeCounter = 1
        while (i < len(X)):
            doneOnce = False
            while (not isPrime(primeCounter) or not doneOnce):
                doneOnce = True
                primeCounter += 1
            primeMap[(X[i], Y[i])] = primeCounter
            i += 1

        subplot_kw = dict(xlim=(0, self.curve.dim), ylim=(0, self.curve.dim), autoscale_on=False)
        fig, ax = plt.subplots(subplot_kw=subplot_kw)

        pts = ax.scatter(data[:, 0], data[:, 1], s=0.5)
        selector = SelectFromCollection(ax, pts)

        def accept(event):
            if event.key == "enter":
                print("Selected points:")
                keys = selector.xys[selector.ind]
                print(lookup(primeMap, keys))
                selector.disconnect()
                ax.set_title("")
                fig.canvas.draw()

        fig.canvas.mpl_connect("key_press_event", accept)
        ax.set_title("Press enter to accept selected points.")

        plt.show()


    def plotSegmentedRandWithPicker(self, segLen):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        numsPicked = []
        i = 0
        while (i < len(points)):
            if (i > 1 and runProb(1. / np.log(i + 1))):
                numsPicked.append(i + 1)
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        data = np.column_stack((X,Y))
        primeMap = {}
        i = 0
        while (i < len(X)):
            primeMap[(X[i], Y[i])] = numsPicked[i]
            i += 1

        subplot_kw = dict(xlim=(0, self.curve.dim), ylim=(0, self.curve.dim), autoscale_on=False)
        fig, ax = plt.subplots(subplot_kw=subplot_kw)

        pts = ax.scatter(data[:, 0], data[:, 1], s=0.5)
        selector = SelectFromCollection(ax, pts)

        def accept(event):
            if event.key == "enter":
                print("Selected points:")
                keys = selector.xys[selector.ind]
                print(lookup(primeMap, keys))
                selector.disconnect()
                ax.set_title("")
                fig.canvas.draw()

        fig.canvas.mpl_connect("key_press_event", accept)
        ax.set_title("Press enter to accept selected points.")

        plt.show()



    def plotSegmentedPrimeWithNum(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            if (isPrime(i + 1)):
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.plot(X, Y, "b.", ms=0.1)
        i = 0
        primeCounter = 1
        while (i < len(X) and i < 10000):
            doneOnce = False
            while (not isPrime(primeCounter) or not doneOnce):
                doneOnce = True
                primeCounter += 1
            plt.annotate(str(primeCounter), (X[i], Y[i]), fontsize=1)
            i += 1
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|prime|num"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()


    def plotSegmentedRandom(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            if (i > 1 and runProb(1. / np.log(i + 1))):
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.plot(X, Y, "b.", ms=0.1)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|rand"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()

    def plotSegmentedRandomEvenOdd(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        numsPicked = []
        i = 0
        while (i < len(points)):
            if (i > 1 and runProb(1. / np.log(i + 1))):
                numsPicked.append(i + 1)
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        Xe = []
        Ye = []
        Xo = []
        Yo = []
        i = 0
        while (i < len(X)):
            if (numsPicked[i] % 2 == 0):
                Xe.append(X[i])
                Ye.append(Y[i])
            else:
                Xo.append(X[i])
                Yo.append(Y[i])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.plot(Xo, Yo, "r.", ms=0.1)
        plt.plot(Xe, Ye, "b.", ms=0.1)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|randDiffEvenOdd"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()

    def plotSegmentedRandomOdd(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        numsPicked = []
        i = 0
        while (i < len(points)):
            if (i > 1 and runProb(2. / np.log(i + 1))):
                numsPicked.append(i + 1)
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        Xe = []
        Ye = []
        Xo = []
        Yo = []
        i = 0
        while (i < len(X)):
            if (numsPicked[i] % 2 == 0):
                Xe.append(X[i])
                Ye.append(Y[i])
            else:
                Xo.append(X[i])
                Yo.append(Y[i])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.plot(Xo, Yo, "b.", ms=0.1)
        #plt.plot(Xe, Ye, "r.", ms=0.1)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|randDiffOdd"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()

    def plotSegmentedAll(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            X.append(points[i][0])
            Y.append(points[i][1])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.plot(X, Y, "b.", ms=0.1)
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|all"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()

    def plotSegmentedRandomWithNum(self, segLen, show = False):
        points = self.curve.segmentCurve(segLen)
        X = []
        Y = []
        i = 0
        while (i < len(points)):
            if (i > 1 and runProb(1. / np.log(i + 1))):
                X.append(points[i][0])
                Y.append(points[i][1])
            i += 1
        plt.figure(figsize=(5, 5), dpi=400)
        plt.plot(X, Y, "b.", ms=0.3)
        i = 0
        primeCounter = 1
        while (i < len(X) and i < 10000):
            doneOnce = False
            while (not isPrime(primeCounter) or not doneOnce):
                doneOnce = True
                primeCounter += 1
            plt.annotate(str(primeCounter), (X[i], Y[i]), fontsize=1)
            i += 1
        plt.axis([0, self.curve.dim, 0, self.curve.dim])
        fName = self.path + "/" + self.folderName + "/"
        fName += str(segLen)
        fName += "|rand|num"
        fName += ".eps"
        plt.savefig(fName)
        if (show):
            plt.show()
        plt.close()


