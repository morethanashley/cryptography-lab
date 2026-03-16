# Vigenere Cipher Implementation
# A polyalphabetic substitution cipher using a keyword.
# Each letter of the plaintext is shifted by the corresponding letter of the key.

def encrypt(text, key):
    """
    Encrypt using Vigenere cipher.
    Key is repeated to match the length of the plaintext.
    Each character is shifted by the corresponding key character's position.
    """
    key = key.upper()
    result = []
    steps = []
    key_index = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - ord('A')
            original_pos = ord(char.upper()) - ord('A')
            new_pos = (original_pos + key_shift) % 26
            new_char = chr(new_pos + base)
            steps.append({
                "plain": char,
                "key_char": key_char,
                "key_shift": key_shift,
                "encrypted": new_char
            })
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
            steps.append({"plain": char, "encrypted": char, "unchanged": True})

    return {
        "result": "".join(result),
        "steps": steps,
        "key_used": key
    }


def decrypt(text, key):
    """
    Decrypt using Vigenere cipher.
    Reverse the shift using the same key.
    """
    key = key.upper()
    result = []
    steps = []
    key_index = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - ord('A')
            original_pos = ord(char.upper()) - ord('A')
            new_pos = (original_pos - key_shift) % 26
            new_char = chr(new_pos + base)
            steps.append({
                "cipher": char,
                "key_char": key_char,
                "key_shift": key_shift,
                "decrypted": new_char
            })
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
            steps.append({"cipher": char, "decrypted": char, "unchanged": True})

    return {
        "result": "".join(result),
        "steps": steps,
        "key_used": key
    }
