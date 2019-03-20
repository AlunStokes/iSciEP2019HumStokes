import pickle
import random
from line import line
from curve import curve

def factor(n):
    if n in [-1, 0, 1]: return []
    if n < 0: n = -n
    F = []
    while n != 1:
        p = trial_division(n)
        e = 1
        n /= p
        while n%p == 0:
            e += 1; n /= p
        F.append((p,e))
    F.sort()
    return F

def runProb(pSucc):
    r = random.random()
    if (r <= pSucc):
        return True
    return False

def trial_division(n, bound=None):
    if n == 1: return 1
    for p in [2, 3, 5]:
        if n%p == 0: return p
    if bound == None: bound = n
    dif = [6, 4, 2, 4, 2, 4, 6, 2]
    m = 7; i = 1
    while m <= bound and m*m <= n:
        if n%m == 0:
            return m
        m += dif[i%8]
        i += 1
    return n

def searchOrdered(l, v):
    i = 0
    while (i < len(l)):
        if (v == l[i]):
            return True
        elif(v < l[i]):
            return False
        i += 1
    return False

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
    '''
    plt.axis([0, dim, 0, dim])
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

def isPrime(n):
    factors = factor(n)
    if (len(factors) == 1 and factors[0][1] == 1):
        return True
    return False


def isProbablePrime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(8):  # number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


def jacobi(a, n):
    """Return jacobi number.

    source: http://www.utm.edu/research/primes/glossary/JacobiSymbol.html"""
    j = 1
    while not a == 0:
        while a % 2 == 0:
            a = a / 2
            if (n % 8 == 3 or n % 8 == 5): j = -j

        x = a;
        a = n;
        n = x  # exchange places

        if (a % 4 == 3 and n % 4 == 3): j = -j
        a = a % int(n)

    if n == 1:
        return j
    else:
        return 0

def euler(n,b=2):
   """Euler probable prime if (b**(n-1)/2)%n = jacobi(a,n).
   (stronger than simple fermat test)"""
   term = pow(b,(n-1)//2,n)
   jac  = jacobi(b,n)
   if jac == -1: return term == n-1
   else: return  term == jac

def nearestPrimeNeighborDist(n):
    dist = 0
    i = -1
    while (True):
        if (isPrime(n + i)):
            dist = i
            break
        else:
            i -= 1
    i = 1
    while (i < abs(dist)):
        if (isPrime(n + i)):
            dist = i
            break
        else:
            i += 1
    return dist

def savePrimesUpTo(n, file):
    f = open(file, "wb")
    i = 2
    primes = [(1, False)]
    while (i <= n):
        factors = factor(i)
        if (len(factors) == 1 and factors[0][1] == 1):
            primes.append((i, True))
        else:
            primes.append((i, False))
        i += 1
    pickle.dump(primes, f)

def read(file):
    f = open(file, "rb")
    arr = pickle.load(f)
    return arr

def fib(n):
    i = 2
    f = [0, 1]
    while (i < n):
        f.append(f[len(f) - 2] + f[len(f) - 1])
        i += 1
    return f

def saveFibUpTo(n, file):
    f = open(file, "wb")
    farr = fib(n)
    pickle.dump(farr, f)