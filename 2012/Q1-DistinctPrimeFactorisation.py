#!/usr/bin/python
from math import sqrt

def gen_primes(n):
    primes = range(2, n)
    for i in xrange(int(sqrt(n))):
        if primes[i] == 0: continue
        j = i + primes[i]
        while j < len(primes):
            primes[j] = 0
            j += primes[i]
    return filter(lambda x: x, primes) # Remove all 0s.

n = int(raw_input())
primes = gen_primes(n+1)
if primes[-1] == n:
    print n
else:
    distinct_prime_factors = [prime for prime in primes if not n % prime]
    print reduce(int.__mul__, distinct_prime_factors)
