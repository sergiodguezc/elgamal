# Implementation of ElGamal Digital Signature Scheme
# Authors: Sergio Domínguez Cabrera
#          Javier Lobillo Olmedo
#          Marina Musse
# Description:

import random
import utils


def decrypt(x, y, public, private):
    p, _, _ = public
    return (y * pow(x, p - 1 - private, p)) % p


def encrypt(msg, public_dest):
    p, g, ga = public_dest
    k = random.randint(2, p - 2)
    gk = pow(g, k, p)
    return (gk, (msg * pow(ga, k, p)) % p)


# Generates a signature (r, s) for a given message.
def sign(public, private_key, message, k=None):
    m = message
    H = hash
    p, g, ga = public
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


# Return True if the signature is valid and False otherwise
def verify(public, signature, message):
    m = message
    p, g, ga = public
    H = hash
    r, s = signature

    if not (0 < r < p) or not (0 < s < p-1):
        return False

    return pow(g, H(m), p) == ((pow(ga, r, p) * pow(r, s, p)) % p)


# Generate the public key consisting of three elements:
# - p : prime number representing the body
# - g : generator of the cyclic group
# - g^a mod p : value used for encryption
# Generate the private key:
# - a : random number between 1 and p - 1
def generate_keys(n_bits: int) -> ((int, int, int), int):
    p, g = utils.random_prime_with_generator(n_bits)
    private = random.randint(1, p-2)
    public = (p, g, pow(g, private, p))
    return (public, private)
