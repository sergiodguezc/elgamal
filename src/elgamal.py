# Implementation of ElGamal Digital Signature Scheme
# Authors: Sergio Domínguez Cabrera
#          Javier Lobillo Olmedo
#          Marina Musse
# Date: --/--/----
# Description:

import random
import utils


# return (p, H, g)
def assign_parameters(p, H, g):
    # return parameters
    return (p, H, g)


# Return (private, public)
def assign_keys(parameters, private):
    p, _, g = parameters
    public = pow(g, private, p)
    return (private, public)


# return (r, s)
def sign(parameters, private_key, message, k=None):
    m = message
    p, H, g = parameters
    x = private_key

    k_already_selected = k is not None

    s = 0
    while s == 0:
        gcd = 0
        while gcd != 1:
            if not k_already_selected:
                k = random.randint(2, p-1)

            (gcd, k_inv, _) = utils.extended_gcd(k, p-1)
        r = pow(g, k, p)
        s = ((((H(m) - x * r) % (p-1)) * k_inv) % (p-1))

    return r, s


def verify(parameters, public_key, signature, message):
    m = message
    p, H, g = parameters
    y = public_key
    r, s = signature

    if not (0 < r < p) or not (0 < s < p-1):
        return False

    return pow(g, H(m), p) == ((pow(y, r, p) * pow(r, s, p)) % p)


# randomly generates parameters (g) given the number of bits of p and H
# returns (p, H, g)
def generate_parameters(n_bits, H):
    p, g = utils.random_prime_with_generator(n_bits)
    return p, H, g


def generate_keys(parameters):
    p, _, _ = parameters
    private = random.randint(1, p-2)
    return assign_keys(parameters, private)
