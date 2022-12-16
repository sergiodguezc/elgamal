from random import randint, randrange
from math import gcd


# Global variables
SIEVE_LEN: int = 500  # Maximum length of the sieve
primes: set = set()   # Primes set


# Implementation of the Sieve of Eratosthenes which is an algorithm for
# finding all prime numbers up to any given limit
#   @n:      sieve limit
#   @return: list containing the sieve of eratosthenes

def sieve_of_eratosthenes(n: int) -> list:
    sieve: list = [True] * (n + 1)
    # primes: set = set()
    sieve[0] = False
    sieve[1] = False

    p: int = 2
    while (p*p <= n):
        if sieve[p-1] is True:
            for i in range(p*p-1, n, p):
                sieve[i] = False
        p += 1

    return sieve


# Auxiliary function which returns if the number n has divisors less than
# SIEVE_LEN.
# @n:       positive integer
# @return:  boolean indicating if the number has divisors less than SIEVE_LEN

def is_eratostenes_prime(n: int) -> bool:
    for divisor in primes:
        if n % divisor == 0 and divisor * divisor <= n:
            return False
    return True


# Auxiliary function which initializes the global primes set.
def fill_primes_set():
    global primes

    sieve: list = sieve_of_eratosthenes(SIEVE_LEN)
    primes = [i for i in range(1, SIEVE_LEN) if sieve[i] and i > 1]


# Implementation of the Miller-Rabin test
#   @n:      positive integer to which we want to perform the test.
#   @k:      positive integer that indicates the number of attempts.
#   @return: boolean indicating if the prime is probable

def miller_rabin_test(n: int, k: int = 10) -> bool:
    # The first thing to do is to check if the number is less than 11 and
    # prime.
    if n in {2, 3, 5, 7}:  # We check whether n is prime less than 11
        return True
    if n < 11:
        return False

    # Check if the number is even
    if n % 2 == 0:
        return False

    # Find m and r such that n = 2**m * r + 1
    r: int = 0
    m: int = n - 1
    while m % 2 == 0:
        m //= 2
        r += 1

    # We start with the tests
    for i in range(k):
        # We choose a random integer between 1 and n-1.
        a: int = randint(1, n - 1)

        # First test
        if gcd(a, n) != 1:
            return False

        x: int = pow(a, m, n)
        probably_prime: bool = (x == 1) or (x == n - 1)

        # Second test
        t: int = 0
        while not probably_prime and t < r - 1:
            x = pow(x, 2, n)
            probably_prime = (x == n - 1)
            t += 1

        # If it fails the test, we terminate the search
        if not probably_prime:
            return False

    # If it passes the k tests we return that it is probably prime
    return True


# Auxiliary function which test if the number n is prime.
#   @n:      positive integer
#   @return: boolean indicating if the number is prime

def is_prime(n: int) -> bool:
    return is_eratostenes_prime(n) and miller_rabin_test(n)


# Function which generates a random prime of a given size in bits.
# @n_bits: positive integer
# @return: random prime of n_bits

def random_prime(n_bits: int) -> int:
    # Random number of n_bits
    n: int = randrange(2**(n_bits-1)-1, 2**(n_bits)-1)

    # If the number is even we make it odd
    n |= 1

    while not is_prime(n):
        # Random number of n_bits
        n: int = randrange(2**(n_bits-1)-1, 2**(n_bits)-1)

        # If the number is even we make it odd
        n |= 1
    return n


# Function which returns (p, g), where p is an n_bit bit prime and g is a
# generator of the multiplicative group (Z/pZ)*.
# @n_bits: positive integer
# @return: (p, g), where p is an n_bit bit prime and g is a generator of the
#          multiplicative group (Z/pZ)*.

def random_prime_with_generator(n_bits: int) -> (int, int):
    # First we look for a prime p of the form 2*q + 1, with q prime.
    p: int = 0
    prime: bool = False
    while not prime:
        q: int = random_prime(n_bits - 1)
        p: int = 2 * q + 1
        if is_prime(p):
            prime = True

    # The possible orders of the elements of (Z/pZ)* are 1, 2, q, p-1.
    # The only element of order 2 is p-1 = -1 mod p
    # The only element of order 1 is 1

    g: int = 0
    generator: bool = False
    while not generator:
        g = randint(2, p-2)

        # We just need to check that it is not of order q
        if pow(g, q, p) != 1:
            generator = True
    return p, g


fill_primes_set()
