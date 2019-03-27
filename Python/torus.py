import numpy as np
from util import *
from plotter import plotter


c = generateCurve((0,0), np.pi**(-1) * 1./100, 1, 400);
p = plotter(c, "Images")
subdiv = 0.005

p.plotLines()
#p.plotSegmentedPrimeWithPicker(subdiv)
p.plotSegmentedRandomOdd(subdiv)
p.plotSegmentedPrime(subdiv)
p.plotSegmentedRandom(subdiv)
p.plotSegmentedAll(subdiv)
#p.plotSegmentedComp(subdiv)
