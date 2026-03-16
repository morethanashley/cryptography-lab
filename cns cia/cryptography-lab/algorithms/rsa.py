# RSA (Rivest-Shamir-Adleman) Algorithm
# Asymmetric encryption using public/private key pairs.
# Security based on the difficulty of factoring large numbers.

import random
import math

def is_prime(n):
    """Check if a number is prime using trial division."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def mod_inverse(e, phi):
    """
    Extended Euclidean Algorithm to find modular inverse.
    Finds d such that (e * d) % phi == 1
    """
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1

    _, x, _ = extended_gcd(e % phi, phi)
    return (x % phi + phi) % phi

def generate_keys(p, q):
    """
    Generate RSA public and private keys from two primes p and q.
    Steps:
    1. n = p * q (modulus)
    2. phi = (p-1)(q-1) (Euler's totient)
    3. Choose e: 1 < e < phi, gcd(e, phi) = 1
    4. Find d: (e * d) % phi = 1
    """
    p, q = int(p), int(q)
    if not is_prime(p) or not is_prime(q):
        raise ValueError(f"Both p and q must be prime numbers. p={p} prime:{is_prime(p)}, q={q} prime:{is_prime(q)}")
    if p == q:
        raise ValueError("p and q must be different primes")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e
    e = 65537  # Common choice
    if e >= phi or math.gcd(e, phi) != 1:
        e = 3
        while e < phi and math.gcd(e, phi) != 1:
            e += 2

    d = mod_inverse(e, phi)

    return {
        "p": p, "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d,
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
        "steps": [
            {"step": "Compute n", "formula": f"n = p × q = {p} × {q} = {n}"},
            {"step": "Compute φ(n)", "formula": f"φ(n) = (p-1)(q-1) = {p-1} × {q-1} = {phi}"},
            {"step": "Choose e", "formula": f"e = {e} (gcd({e}, {phi}) = {math.gcd(e, phi)})"},
            {"step": "Compute d", "formula": f"d = {d} (e×d mod φ(n) = {(e*d)%phi})"},
        ]
    }

def encrypt(message, e, n):
    """
    RSA Encryption: C = M^e mod n
    Encrypts each character's ASCII value.
    """
    e, n = int(e), int(n)
    encrypted = []
    steps = []
    for char in message:
        m = ord(char)
        if m >= n:
            raise ValueError(f"Message value {m} must be less than n={n}. Use larger primes.")
        c = pow(m, e, n)
        encrypted.append(c)
        steps.append({"char": char, "ascii": m, "encrypted": c, "formula": f"{m}^{e} mod {n} = {c}"})

    return {
        "result": " ".join(map(str, encrypted)),
        "encrypted_values": encrypted,
        "steps": steps
    }

def decrypt(cipher_text, d, n):
    """
    RSA Decryption: M = C^d mod n
    Decrypts each number back to its ASCII character.
    """
    d, n = int(d), int(n)
    values = [int(x.strip()) for x in cipher_text.split()]
    result = []
    steps = []
    for c in values:
        m = pow(c, d, n)
        char = chr(m)
        result.append(char)
        steps.append({"encrypted": c, "decrypted": m, "char": char, "formula": f"{c}^{d} mod {n} = {m}"})

    return {
        "result": "".join(result),
        "steps": steps
    }
