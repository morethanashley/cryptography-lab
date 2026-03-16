# Elliptic Curve Cryptography (ECC) - Educational Demo
# ECC uses points on an elliptic curve: y^2 = x^3 + ax + b (mod p)
# Much stronger security per bit compared to RSA.

def point_add(P, Q, a, p):
    """Add two points on an elliptic curve mod p."""
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 != y2:
        return None  # Point at infinity

    if P == Q:
        # Point doubling
        lam = (3 * x1 * x1 + a) * pow(2 * y1, p - 2, p) % p
    else:
        # Point addition
        lam = (y2 - y1) * pow(x2 - x1, p - 2, p) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_multiply(k, P, a, p):
    """Multiply point P by scalar k using double-and-add."""
    result = None
    addend = P
    steps = []
    k_bin = bin(k)[2:]

    for bit in k_bin:
        if result is not None:
            result = point_add(result, result, a, p)
        if bit == '1':
            result = point_add(result, addend, a, p)
        steps.append({"bit": bit, "point": result})

    return result, steps


def get_curve_points(a, b, p, limit=50):
    """Get all points on the curve y^2 = x^3 + ax + b mod p."""
    points = []
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        for y in range(p):
            if (y*y) % p == rhs:
                points.append({"x": x, "y": y})
        if len(points) >= limit:
            break
    return points


def simulate_key_exchange(a, b, p, Gx, Gy, alice_k, bob_k):
    """
    Simulate ECC Diffie-Hellman key exchange.
    G = generator point, alice_k and bob_k are private keys.
    """
    a, b, p = int(a), int(b), int(p)
    Gx, Gy = int(Gx), int(Gy)
    alice_k, bob_k = int(alice_k), int(bob_k)

    G = (Gx, Gy)

    # Verify G is on the curve
    if (Gy**2) % p != (Gx**3 + a*Gx + b) % p:
        raise ValueError("Generator point G is not on the curve")

    # Alice's public key = alice_k * G
    alice_pub, alice_steps = scalar_multiply(alice_k, G, a, p)
    # Bob's public key = bob_k * G
    bob_pub, bob_steps = scalar_multiply(bob_k, G, a, p)

    # Shared secrets
    shared_alice, _ = scalar_multiply(alice_k, bob_pub, a, p)
    shared_bob, _ = scalar_multiply(bob_k, alice_pub, a, p)

    curve_points = get_curve_points(a, b, p)

    return {
        "curve": {"a": a, "b": b, "p": p, "equation": f"y² = x³ + {a}x + {b} (mod {p})"},
        "generator": {"x": Gx, "y": Gy},
        "alice_private": alice_k,
        "bob_private": bob_k,
        "alice_public": alice_pub,
        "bob_public": bob_pub,
        "shared_secret_alice": shared_alice,
        "shared_secret_bob": shared_bob,
        "match": shared_alice == shared_bob,
        "curve_points": curve_points[:30],
        "steps": [
            {"step": "Curve Parameters", "description": f"y² = x³ + {a}x + {b} mod {p}"},
            {"step": "Generator Point G", "description": f"G = ({Gx}, {Gy})"},
            {"step": "Alice's Public Key", "description": f"A = {alice_k} × G = {alice_pub}"},
            {"step": "Bob's Public Key", "description": f"B = {bob_k} × G = {bob_pub}"},
            {"step": "Alice's Shared Secret", "description": f"S = {alice_k} × B = {shared_alice}"},
            {"step": "Bob's Shared Secret", "description": f"S = {bob_k} × A = {shared_bob}"},
            {"step": "Keys Match", "description": str(shared_alice == shared_bob)}
        ]
    }
