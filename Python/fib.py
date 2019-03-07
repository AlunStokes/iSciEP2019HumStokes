from pyx import *
from math import *
from util import *
import numpy as np
import time


f = read("FibLists/1e4.dat")[2:]
print(f)
ca = canvas.canvas()
s = time.time()
j = 0
while j < len(f):
    i = j + 1
    r = sqrt(i)
    theta = r * 2 * pi
    x = cos(theta) * r
    y = -sin(theta) * r
    if (euler(f[j])):
        radius = 0.2
        ca.fill(path.circle(x, y, radius))
    j += 1
e = time.time()

print(e - s)
d = document.document(pages=[document.page(ca, paperformat=document.paperformat.A4, fittosize=1)])
d.writePSfile("Images/fib1e4.ps")
