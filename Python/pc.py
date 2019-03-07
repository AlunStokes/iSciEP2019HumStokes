from pyx import *
from math import *
from util import *
import numpy as np
import time



primes = read("PrimeLists/1e5.dat")
ca = canvas.canvas()
s = time.time()
j = 0
while j < len(primes):
    i = j + 1
    r = i**(1/2)
    theta = r * 2 * pi
    x = cos(theta) * r
    y = -sin(theta) * r
    radius = 0.2
    if (primes[j][1]):
        ca.fill(path.circle(x, y, radius), [color.rgb.blue])
    else:
        nd = nearestPrimeNeighborDist(j)
        radius = 0.2 * pow(1.05, nd)
        if (nd > 10):
            ca.fill(path.circle(x, y, radius))
    j += 1
e = time.time()

print(e - s)
d = document.document(pages=[document.page(ca, paperformat=document.paperformat.A4, fittosize=1)])
d.writePDFfile("Images/PDFs/nearestNeighbor>10neighbors1e5.pdf")
