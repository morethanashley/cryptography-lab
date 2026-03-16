# Hill Cipher Implementation
# A polygraphic substitution cipher based on linear algebra.
# Uses matrix multiplication to encrypt blocks of letters.

import numpy as np

def mod_inverse_matrix(matrix, mod=26):
    """
    Compute the modular inverse of a matrix under mod 26.
    Uses the formula: inv = det_inv * adjugate(matrix) mod 26
    """
    det = int(round(np.linalg.det(matrix))) % mod
    # Find modular inverse of determinant
    det_inv = None
    for i in range(mod):
        if (det * i) % mod == 1:
            det_inv = i
            break
    if det_inv is None:
        raise ValueError("Matrix is not invertible under mod 26")

    # Compute adjugate (cofactor matrix transposed)
    size = matrix.shape[0]
    cofactors = np.zeros((size, size))
    for r in range(size):
        for c in range(size):
            minor = np.delete(np.delete(matrix, r, axis=0), c, axis=1)
            cofactors[r][c] = ((-1) ** (r + c)) * round(np.linalg.det(minor))
    adjugate = cofactors.T
    inv_matrix = (det_inv * adjugate) % mod
    return inv_matrix.astype(int)


def text_to_vector(text, size):
    """Convert text to numeric vectors (A=0, B=1, ..., Z=25), padded with X if needed."""
    text = text.upper().replace(" ", "")
    text = ''.join(filter(str.isalpha, text))
    while len(text) % size != 0:
        text += 'X'
    return text


def encrypt(text, key_matrix_flat):
    """
    Encrypt using Hill cipher.
    key_matrix_flat: comma-separated values for the key matrix (e.g., "6,24,1,13" for 2x2)
    """
    values = [int(x.strip()) for x in key_matrix_flat.split(',')]
    size = int(len(values) ** 0.5)
    if size * size != len(values):
        raise ValueError("Key must be a perfect square number of values (4 for 2x2, 9 for 3x3)")

    key_matrix = np.array(values).reshape(size, size)
    text = text_to_vector(text, size)
    result = []
    steps = []

    for i in range(0, len(text), size):
        block = text[i:i+size]
        vec = np.array([ord(c) - ord('A') for c in block])
        encrypted_vec = np.dot(key_matrix, vec) % 26
        encrypted_chars = ''.join(chr(int(v) + ord('A')) for v in encrypted_vec)
        result.append(encrypted_chars)
        steps.append({
            "block": block,
            "vector": vec.tolist(),
            "result_vector": encrypted_vec.tolist(),
            "encrypted": encrypted_chars
        })

    return {
        "result": "".join(result),
        "steps": steps,
        "key_matrix": key_matrix.tolist(),
        "size": size
    }


def decrypt(text, key_matrix_flat):
    """
    Decrypt using Hill cipher.
    Compute the modular inverse of the key matrix and multiply.
    """
    values = [int(x.strip()) for x in key_matrix_flat.split(',')]
    size = int(len(values) ** 0.5)
    key_matrix = np.array(values).reshape(size, size)
    inv_matrix = mod_inverse_matrix(key_matrix)

    text = text_to_vector(text, size)
    result = []
    steps = []

    for i in range(0, len(text), size):
        block = text[i:i+size]
        vec = np.array([ord(c) - ord('A') for c in block])
        decrypted_vec = np.dot(inv_matrix, vec) % 26
        decrypted_chars = ''.join(chr(int(v) + ord('A')) for v in decrypted_vec)
        result.append(decrypted_chars)
        steps.append({
            "block": block,
            "vector": vec.tolist(),
            "result_vector": decrypted_vec.tolist(),
            "decrypted": decrypted_chars
        })

    return {
        "result": "".join(result),
        "steps": steps,
        "inv_matrix": inv_matrix.tolist()
    }
