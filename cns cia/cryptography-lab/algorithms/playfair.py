# Playfair Cipher Implementation
# A digraph substitution cipher using a 5x5 key matrix.
# Encrypts pairs of letters based on their positions in the matrix.

def generate_matrix(key):
    """
    Generate the 5x5 Playfair matrix from the key.
    I and J are treated as the same letter.
    """
    key = key.upper().replace('J', 'I')
    seen = []
    for ch in key:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    for ch in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if ch not in seen:
            seen.append(ch)
    matrix = [seen[i*5:(i+1)*5] for i in range(5)]
    return matrix


def find_position(matrix, char):
    """Find row and column of a character in the matrix."""
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None


def prepare_text(text):
    """
    Prepare plaintext: remove non-alpha, uppercase, replace J with I,
    split into digraphs, insert X between repeated letters.
    """
    text = text.upper().replace('J', 'I')
    text = ''.join(filter(str.isalpha, text))
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                pairs.append((a, 'X'))
                i += 1
            else:
                pairs.append((a, b))
                i += 2
        else:
            pairs.append((a, 'X'))
            i += 1
    return pairs


def encrypt(text, key):
    """
    Encrypt using Playfair cipher.
    Rules:
    - Same row: shift right
    - Same column: shift down
    - Rectangle: swap columns
    """
    matrix = generate_matrix(key)
    pairs = prepare_text(text)
    result = []
    steps = []

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            ea = matrix[r1][(c1 + 1) % 5]
            eb = matrix[r2][(c2 + 1) % 5]
            rule = "Same Row"
        elif c1 == c2:
            ea = matrix[(r1 + 1) % 5][c1]
            eb = matrix[(r2 + 1) % 5][c2]
            rule = "Same Column"
        else:
            ea = matrix[r1][c2]
            eb = matrix[r2][c1]
            rule = "Rectangle"

        result.append(ea + eb)
        steps.append({"pair": a + b, "encrypted": ea + eb, "rule": rule})

    return {
        "result": "".join(result),
        "steps": steps,
        "matrix": matrix
    }


def decrypt(text, key):
    """
    Decrypt using Playfair cipher.
    Reverse the encryption rules (shift left/up instead of right/down).
    """
    matrix = generate_matrix(key)
    text = text.upper().replace('J', 'I')
    text = ''.join(filter(str.isalpha, text))
    pairs = [(text[i], text[i+1]) for i in range(0, len(text), 2)]
    result = []
    steps = []

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            da = matrix[r1][(c1 - 1) % 5]
            db = matrix[r2][(c2 - 1) % 5]
            rule = "Same Row"
        elif c1 == c2:
            da = matrix[(r1 - 1) % 5][c1]
            db = matrix[(r2 - 1) % 5][c2]
            rule = "Same Column"
        else:
            da = matrix[r1][c2]
            db = matrix[r2][c1]
            rule = "Rectangle"

        result.append(da + db)
        steps.append({"pair": a + b, "decrypted": da + db, "rule": rule})

    return {
        "result": "".join(result),
        "steps": steps,
        "matrix": matrix
    }
