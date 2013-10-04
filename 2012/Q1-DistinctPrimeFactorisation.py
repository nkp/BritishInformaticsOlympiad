#!/usr/bin/python
from math import sqrt

def gen_primes(n):
    primes = range(n)
    primes[1] = 0
    for i in xrange(2, int(sqrt(n))+1):
        if primes[i] == 0: continue
        j = i**2
        while j < n:
            primes[j] = 0
            j += i
    return filter(None, primes) # Remove all 0s.

n = int(raw_input())
primes = gen_primes(n+1)
if primes[-1] == n:
    print n
else:
    distinct_prime_factors = [prime for prime in primes if not n % prime]
    print reduce(int.__mul__, distinct_prime_factors)
