# Diffie-Hellman Key Exchange
# Allows two parties (Alice and Bob) to establish a shared secret
# over an insecure channel without ever transmitting the secret itself.
# Security based on the discrete logarithm problem.

def is_prime(n):
    """Check if n is prime."""
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def is_primitive_root(g, p):
    """Check if g is a primitive root modulo p (simplified check)."""
    if p < 2: return False
    required = set(range(1, p))
    actual = set(pow(g, i, p) for i in range(1, p))
    return required == actual

def simulate(p, g, alice_private, bob_private):
    """
    Simulate Diffie-Hellman key exchange between Alice and Bob.
    
    Public parameters: prime p, generator g
    Alice chooses private key a, Bob chooses private key b
    
    Steps:
    1. Alice computes A = g^a mod p  (public key)
    2. Bob computes B = g^b mod p    (public key)
    3. Alice computes shared = B^a mod p
    4. Bob computes shared = A^b mod p
    Both arrive at the same shared secret!
    """
    p = int(p)
    g = int(g)
    a = int(alice_private)
    b = int(bob_private)

    if not is_prime(p):
        raise ValueError(f"{p} is not a prime number")
    if g >= p:
        raise ValueError(f"Generator g must be less than p")

    # Public key generation
    A = pow(g, a, p)  # Alice's public key
    B = pow(g, b, p)  # Bob's public key

    # Shared secret computation
    shared_alice = pow(B, a, p)  # Alice computes using Bob's public key
    shared_bob = pow(A, b, p)    # Bob computes using Alice's public key

    steps = [
        {
            "step": "Public Parameters",
            "description": f"Prime p = {p}, Generator g = {g}",
            "note": "Both parties agree on these values publicly"
        },
        {
            "step": "Alice's Private Key",
            "description": f"Alice secretly chooses a = {a}",
            "note": "Never shared with anyone"
        },
        {
            "step": "Bob's Private Key",
            "description": f"Bob secretly chooses b = {b}",
            "note": "Never shared with anyone"
        },
        {
            "step": "Alice's Public Key",
            "formula": f"A = g^a mod p = {g}^{a} mod {p} = {A}",
            "description": f"Alice sends A = {A} to Bob",
            "note": "Safe to transmit publicly"
        },
        {
            "step": "Bob's Public Key",
            "formula": f"B = g^b mod p = {g}^{b} mod {p} = {B}",
            "description": f"Bob sends B = {B} to Alice",
            "note": "Safe to transmit publicly"
        },
        {
            "step": "Alice Computes Shared Secret",
            "formula": f"S = B^a mod p = {B}^{a} mod {p} = {shared_alice}",
            "description": f"Alice uses Bob's public key"
        },
        {
            "step": "Bob Computes Shared Secret",
            "formula": f"S = A^b mod p = {A}^{b} mod {p} = {shared_bob}",
            "description": f"Bob uses Alice's public key"
        },
        {
            "step": "Shared Secret Established",
            "description": f"Both Alice and Bob now share the secret: {shared_alice}",
            "note": "An eavesdropper only knows p, g, A, B — computing the secret requires solving the discrete log problem"
        }
    ]

    return {
        "p": p, "g": g,
        "alice_private": a,
        "bob_private": b,
        "alice_public": A,
        "bob_public": B,
        "shared_secret": shared_alice,
        "match": shared_alice == shared_bob,
        "steps": steps
    }
