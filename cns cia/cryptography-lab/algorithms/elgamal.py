# ElGamal Cryptosystem
# An asymmetric key encryption algorithm based on Diffie-Hellman key exchange.
# Security relies on the difficulty of the discrete logarithm problem.

import random

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def generate_keys(p, g, private_key=None):
    """
    Generate ElGamal public and private keys.
    
    p: large prime
    g: generator (primitive root mod p)
    private_key x: random integer 1 < x < p-1
    public_key y = g^x mod p
    """
    p, g = int(p), int(g)
    if not is_prime(p):
        raise ValueError(f"{p} is not prime")

    x = int(private_key) if private_key else random.randint(2, p - 2)
    y = pow(g, x, p)

    return {
        "p": p, "g": g,
        "private_key": x,
        "public_key": y,
        "steps": [
            {"step": "Choose prime p", "value": p},
            {"step": "Choose generator g", "value": g},
            {"step": "Choose private key x", "value": x, "note": "Keep secret"},
            {"step": "Compute public key y = g^x mod p", "formula": f"{g}^{x} mod {p} = {y}"}
        ]
    }

def encrypt(message, p, g, y, k=None):
    """
    ElGamal Encryption.
    For each character M:
    1. Choose random k
    2. Compute c1 = g^k mod p
    3. Compute c2 = M * y^k mod p
    Ciphertext = (c1, c2)
    """
    p, g, y = int(p), int(g), int(y)
    if k is None:
        k = random.randint(2, p - 2)
    else:
        k = int(k)

    encrypted_pairs = []
    steps = []

    for char in message:
        m = ord(char)
        c1 = pow(g, k, p)
        c2 = (m * pow(y, k, p)) % p
        encrypted_pairs.append({"c1": c1, "c2": c2})
        steps.append({
            "char": char,
            "ascii": m,
            "k": k,
            "c1": c1,
            "c2": c2,
            "formula_c1": f"c1 = g^k mod p = {g}^{k} mod {p} = {c1}",
            "formula_c2": f"c2 = M × y^k mod p = {m} × {y}^{k} mod {p} = {c2}"
        })

    return {
        "result": str(encrypted_pairs),
        "encrypted_pairs": encrypted_pairs,
        "k_used": k,
        "steps": steps
    }

def decrypt(encrypted_pairs, p, x):
    """
    ElGamal Decryption.
    For each (c1, c2):
    M = c2 * (c1^x)^(-1) mod p
    """
    p, x = int(p), int(x)
    result = []
    steps = []

    for pair in encrypted_pairs:
        c1, c2 = int(pair["c1"]), int(pair["c2"])
        # Compute c1^x mod p, then its modular inverse
        s = pow(c1, x, p)
        s_inv = pow(s, p - 2, p)  # Fermat's little theorem for inverse
        m = (c2 * s_inv) % p
        char = chr(m)
        result.append(char)
        steps.append({
            "c1": c1, "c2": c2,
            "s": s,
            "s_inv": s_inv,
            "m": m,
            "char": char,
            "formula": f"M = c2 × (c1^x)^(-1) mod p = {c2} × {s_inv} mod {p} = {m}"
        })

    return {
        "result": "".join(result),
        "steps": steps
    }
