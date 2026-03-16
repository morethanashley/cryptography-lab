# Caesar Cipher Implementation
# One of the oldest and simplest substitution ciphers.
# Each letter is shifted by a fixed number (key) in the alphabet.

def encrypt(text, shift):
    """
    Encrypt plaintext using Caesar cipher.
    Each alphabetic character is shifted forward by 'shift' positions.
    Non-alphabetic characters remain unchanged.
    """
    result = []
    steps = []
    shift = int(shift) % 26

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            original_pos = ord(char) - base
            new_pos = (original_pos + shift) % 26
            new_char = chr(new_pos + base)
            result.append(new_char)
            steps.append({
                "original": char,
                "original_pos": original_pos,
                "shift": shift,
                "new_pos": new_pos,
                "encrypted": new_char
            })
        else:
            result.append(char)
            steps.append({"original": char, "encrypted": char, "unchanged": True})

    return {
        "result": "".join(result),
        "steps": steps,
        "shift": shift
    }


def decrypt(text, shift):
    """
    Decrypt ciphertext using Caesar cipher.
    Decryption is just encryption with a negative shift (or 26 - shift).
    """
    shift = int(shift) % 26
    data = encrypt(text, 26 - shift)
    data["operation"] = "decrypt"
    return data
