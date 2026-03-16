# Rail Fence Cipher Implementation
# A transposition cipher that writes text in a zigzag pattern across 'rails'.
# The ciphertext is read row by row.

def encrypt(text, rails):
    """
    Encrypt using Rail Fence cipher.
    Write characters in zigzag across 'rails' rows, then read row by row.
    """
    rails = int(rails)
    if rails < 2:
        return {"result": text, "steps": [], "grid": []}

    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    result = ''.join(''.join(row) for row in fence)

    # Build visual grid for display
    grid = []
    rail = 0
    direction = 1
    positions = []
    for i, char in enumerate(text):
        positions.append((rail, i, char))
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    return {
        "result": result,
        "fence": [''.join(row) for row in fence],
        "positions": positions,
        "rails": rails
    }


def decrypt(text, rails):
    """
    Decrypt Rail Fence cipher.
    Determine the pattern of positions, then fill in the ciphertext characters.
    """
    rails = int(rails)
    n = len(text)
    if rails < 2:
        return {"result": text, "steps": []}

    # Determine which rail each position belongs to
    pattern = []
    rail = 0
    direction = 1
    for i in range(n):
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    # Sort indices by rail to know how many chars go on each rail
    indices = sorted(range(n), key=lambda i: pattern[i])
    result = [''] * n
    for idx, char in zip(indices, text):
        result[idx] = char

    return {
        "result": "".join(result),
        "rails": rails,
        "pattern": pattern
    }
