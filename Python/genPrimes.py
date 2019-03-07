from util import *
from multiprocessing.dummy import Pool as ThreadPool
import time

exp = range(8,9)

def calcPrimes(n):
    s = time.time();
    savePrimesUpTo(10 ** n, "PrimeLists/1e" + str(n) + ".dat")
    e = time.time()
    print("Finished", n, "in", e - s, "seconds")

pool = ThreadPool(4)
pool.map(calcPrimes, exp)


'''
savePrimesUpTo(10**7, "PrimeLists/1e7b.dat")
'''

'''
primes2 = readPrimes("PrimeLists/1e7b.dat")
print (primes2[6355234])
'''

