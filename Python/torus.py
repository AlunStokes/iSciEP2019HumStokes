import numpy as np
import matplotlib.pyplot as plt
from util import *
import time

def generateCurve(p0, slope, dim, numLines):
    return loop(p0, slope, dim, numLines)

def generatePlot(baseSlopeString, slopeMultiplier, segLen, numLines, prime, folderPath):
    p0 = (0,0)
    #slopeString = "1. / np.pi"
    slope = eval(baseSlopeString) * slopeMultiplier
    dim = 1
    #numLines = 500
    #segLen = 0.01
    #prime = True
    t0 = time.time()
    c = generateCurve(p0, slope, dim, numLines)
    #print("Num primes:", c.getLength() / segLen)
    t1 = time.time()
    #print("Generating curve:", t1 - t0)
    t0 = time.time()
    points = c.segmentCurve(segLen)
    t1 = time.time()
    #print("Segmenting curve:", t1 - t0)

    t0 = time.time()
    X = []
    Y = []
    i = 0
    while (i < len(points)):
        if (prime):
            if (isPrime(i + 1)):
                X.append(points[i][0])
                Y.append(points[i][1])
        else:
            if (i > 1 and runProb(1. / np.log(i + 1))):
                X.append(points[i][0])
                Y.append(points[i][1])
        i += 1
    t1 = time.time()
    #print("Determining Primality:", t1 - t0)

    plt.figure(figsize=(5,5), dpi=2000)
    t0 = time.time()
    plt.plot(X, Y, ".", ms=0.5)
    '''
    i = 0
    primeCounter = 1
    while (i < len(X) and i < 10000):
        doneOnce = False
        while (not isPrime(primeCounter) or not doneOnce):
            doneOnce = True
            primeCounter += 1
        plt.annotate(str(primeCounter), (X[i],Y[i]), fontsize=1)
        i += 1
    '''
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.1)
    # place a text box in upper left in axes coords
    plt.text(-0.05, dim + 0.1 * dim, "seg.len.=" + str(segLen), fontsize=8,
            verticalalignment='top', bbox=props)
    plt.text(0.20, dim + 0.1 * dim, "m=" + baseSlopeString + "*" + str(slopeMultiplier), fontsize=8,
            verticalalignment='top', bbox=props)
    plt.text(0.50, dim + 0.1 * dim, "lines=" + str(numLines), fontsize=8,
            verticalalignment='top', bbox=props)
    plt.text(0.8, dim + 0.1 * dim, "prime=" + str(prime), fontsize=8,
            verticalalignment='top', bbox=props)
    plt.axis([0, dim, 0, dim])
    #plt.show()
    fName = folderPath + "/"
    fName += "m=" + baseSlopeString + "*" + str(slopeMultiplier)
    if (prime):
        fName += "-prime"
    else:
        fName += "-rand"
    fName += "-seglen=" + str(segLen)
    fName += "-lines=" + str(numLines)
    fName += ".eps"
    plt.savefig(fName)
    plt.close()
    t1 = time.time()
    #print("Generate plot:", t1 - t0)

def generateBothPlots(baseSlopeString, slopeMultiplier, segLen, numLines, folderPath="."):
    generatePlot(baseSlopeString, slopeMultiplier, segLen, numLines, True, folderPath)
    generatePlot(baseSlopeString, slopeMultiplier, segLen, numLines, False, folderPath)

step = 1
i = 35
while(i < 39):
    print(i)
    generateBothPlots("np.exp(-1)", 1 + i * step, 0.005, 500, "torus_images_m=e^(-1)")
    i += 1



