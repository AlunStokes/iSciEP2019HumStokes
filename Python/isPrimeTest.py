from util import *
import time

'''

l = 100000
n = 1000000

s = time.time()
i = l
while (i < n):
    isProbablePrime(i)
    i += 1
e = time.time()
print("Probable took:", e - s)

s = time.time()
i = l
while(i < n):
    isPrime(i)
    i += 1
e = time.time()
print("Analytic took:", e - s)

s = time.time()
i = l
while(i < n):
    euler(i)
    i += 1
e = time.time()
print("Euler took:", e - s)

'''

s = time.time()
f = read("FibLists/1e4.dat")[2:]
for i in f:
    euler(i)
e = time.time()
print("First", len(f) + 2, "fib took:", e - s)