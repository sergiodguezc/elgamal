from random import randint, randrange
from math import gcd, log2


# Global variables
SIEVE_LEN: int = 500  # Maximum length of the sieve
primes: set = set()   # Primes set


# Implementation of the Sieve of Eratosthenes which is an algorithm for
# finding all prime numbers up to any given limit
#   @n:      sieve limit
#   @return: list containing the sieve of eratosthenes
def sieve_of_eratosthenes(n: int) -> list:
    sieve = [1] * (n+1)
    sieve[0] = 0
    sieve[1] = 0

    num: int = 1

    while num <= n:
        if sieve[num] == 1:
            i = 2 * num
            while i <= n:
                sieve[i] = 0
                i += num
        num += 1

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


# returns (gcd, x, y)
# (x, y) such that gcd = x * a + b * y
def extended_gcd(a, b):
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
        q = old_r // r
        (old_r, r) = (r, old_r - q * r)
        (old_s, s) = (s, old_s - q * s)
        (old_t, t) = (t, old_t - q * t)

    return old_r, old_s, old_t


# Auxiliary function which initializes the global primes set.
def fill_primes_set():
    global primes

    sieve: list = sieve_of_eratosthenes(SIEVE_LEN)
    primes = [i for i in range(1, SIEVE_LEN) if sieve[i]]


# Implementation of the Miller-Rabin test
#   @n:      positive integer to which we want to perform the test.
#   @k:      positive integer that indicates the number of attempts.
#   @return: boolean indicating if the prime is probable

def miller_rabin_test(n: int, k: int = 40) -> bool:
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
    n: int = randrange(2**(n_bits-1)+1, 2**(n_bits)-1)

    # If the number is even we make it odd
    n |= 1

    while not is_prime(n):
        # Random number of n_bits
        n: int = randrange(2**(n_bits-1)+1, 2**(n_bits)-1)

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


# Function which converts a string to a list of integers.
def message_to_ascii_blocks(msg: str, blk_size: int) -> list:
    blocks = []

    ascii = ord(msg[0])  # Compute ASCII value of a one-point string
    for i in range(1, len(msg)):
        if (i % blk_size == 0):
            blocks.append(ascii)
            ascii = 0
        # ASCII values have at most 3 characters
        ascii = 1000 * ascii + ord(msg[i])
    blocks.append(ascii)  # Add the last element
    return blocks


# Function which converts a list of integers to a string
def ascii_blocks_to_message(blk: int, blk_size: int) -> str:
    message = ""
    for i in range(len(blk)):
        tmp = ""
        for _ in range(blk_size):
            tmp = chr(blk[i] % 1000) + tmp  # chr is the inverse of ord
            blk[i] //= 1000  # Drop the translated part
        message += tmp
    return message


def smooth_prime_minus_1_500() -> (int, int, list):
    n_bits: int = 5
    fact = list()
    while True:
        p, g = random_prime_with_generator(n_bits)
        p_aux = p - 1
        for i in range(30):
            e: int = 0
            if p_aux == 0:
                return p, g, fact
            while p_aux % primes[i] == 0:
                p_aux == p_aux // i
                e += 1
            if e != 0:
                fact.append((primes[i], e))


def reduce_congruence(cong: list):
    if len(cong) == 1:
        return cong[0][0], cong[0][1]
    if len(cong) == 2:
        a1, N1, a2, N2 = cong[0][0], cong[0][1], cong[1][0], cong[1][1]

    else:
        m = len(cong) // 2
        a1, N1 = reduce_congruence(cong[:m])
        a2, N2 = reduce_congruence(cong[m:])

    g, a, b = extended_gcd(N1, N2)
    x1 = N2 * (b % N1)  # x1 =1 (mod N), x1 =0 (mod M)
    x2 = N1 * (a % N2)  # x2 =0 (mod N), x2 =1 (mod M)
    return (x1*a1 + x2*a2) % (N1*N2), N1*N2


def silver_pohlig_hellman(b: int, h: int, n: int, fact: list) -> int:
    m = list()
    for (pi, ei) in range(len(fact)):
        rij = list()
        for j in range(pi):
            rij.append(pow(b, (j*n)//pi))
        x = list()
        for k in range(ei):
            exp = 0
            for t in range(k):
                exp += x[t]*pow(pi, t)
            yk = h // pow(b, exp)

            ykn = pow(yk, n // pow(pi, k + 1))
            res = 0
            for j in range(pi):
                if ykn == rij[j]:
                    res = j
            x.append(res)
        mi = 0
        for k in range(ei):
            mi = x[k]*pow(pi, k)
        m.append((mi, pow(pi, ei)))
    return reduce_congruence(m)


fill_primes_set()
print(smooth_prime_minus_1_500())
