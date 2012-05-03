from math import log10

Primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def PrimeProduct(N):
    Score = 1
    while N > 0:
        Score *= Primes[N % 10]
        N /= 10
    return Score

def GetAnagramDigits (N):
    AnagramDigits = []
    Score = PrimeProduct(N)
    for i in range(2, 10):
        if int(log10(N)) < int(log10(N*i)):
            break
        if PrimeProduct(N*i) == Score:
            AnagramDigits.append(str(i))
    return AnagramDigits

if __name__ == '__main__':
    while 1:
        Num = int(raw_input('Input: '))
        Digits = GetAnagramDigits(Num)
        if Digits:
            print ' '.join(Digits)
        else:
            print 'NO'
