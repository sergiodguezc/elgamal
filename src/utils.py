from random import randint, randrange


# Global variables
SIEVE_LEN = 500  # Maximum length of the sieve
primes = set()   # Primes list


# Implementation of the Sieve of Eratosthenes
#   @n      : sieve length
#   @return : list containing the sieve of eratosthenes


def eratosthenes(n: int) -> list:
    sieve: list = [True] * (n + 1)
    sieve[0] = False
    sieve[1] = False

    p: int = 2
    while (p*p <= n):
        if sieve[p-1] is True:
            for i in range(p*p-1, n, p):
                sieve[i] = False
        p += 1
    ret: list = []
    for i in range(1, n):
        if sieve[i]:
            ret += [i+1]
    return ret
