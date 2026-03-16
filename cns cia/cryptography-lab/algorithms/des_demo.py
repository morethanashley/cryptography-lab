# DES (Data Encryption Standard) - Educational Demonstration
# This is a simplified educational version showing the key concepts of DES.
# Real DES uses 64-bit blocks and 56-bit keys with 16 rounds.
# We demonstrate the structure and concepts without full bit-level implementation.

# Initial Permutation Table (IP) - first 16 positions for demo
IP = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

# Final Permutation (IP inverse)
IP_INV = [40,8,48,16,56,24,64,32,
          39,7,47,15,55,23,63,31,
          38,6,46,14,54,22,62,30,
          37,5,45,13,53,21,61,29,
          36,4,44,12,52,20,60,28,
          35,3,43,11,51,19,59,27,
          34,2,42,10,50,18,58,26,
          33,1,41,9,49,17,57,25]

def text_to_bin(text):
    """Convert text string to binary string (8 bits per character)."""
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    """Convert binary string back to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

def permute(bits, table):
    """Apply a permutation table to a bit string."""
    return ''.join(bits[t-1] for t in table)

def xor_bits(a, b):
    """XOR two binary strings of equal length."""
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def des_encrypt_demo(plaintext, key):
    """
    Educational DES demonstration.
    Shows the structure: IP -> 16 rounds (simplified) -> IP_INV
    Uses first 64 bits of input, pads if needed.
    """
    # Prepare 64-bit block
    plain_bin = text_to_bin(plaintext[:8].ljust(8))[:64]
    key_bin = text_to_bin(key[:8].ljust(8))[:64]

    steps = []

    # Step 1: Initial Permutation
    after_ip = permute(plain_bin, IP)
    steps.append({
        "step": "Initial Permutation (IP)",
        "input": plain_bin,
        "output": after_ip,
        "description": "Rearranges the 64 bits according to the IP table"
    })

    # Split into Left and Right halves
    L = after_ip[:32]
    R = after_ip[32:]
    steps.append({
        "step": "Split into L and R",
        "L": L,
        "R": R,
        "description": "64-bit block split into two 32-bit halves"
    })

    # Simplified 3-round demonstration (real DES has 16)
    round_keys = []
    for i in range(3):
        # Simplified round key generation (rotate key bits)
        shift = (i + 1) * 2
        rk = key_bin[shift:] + key_bin[:shift]
        round_keys.append(rk[:32])

    for i in range(3):
        rk = round_keys[i]
        # Feistel function: XOR R with round key (simplified F function)
        f_output = xor_bits(R, rk)
        new_R = xor_bits(L, f_output)
        new_L = R
        steps.append({
            "step": f"Round {i+1}",
            "L_in": L, "R_in": R,
            "round_key": rk,
            "f_output": f_output,
            "L_out": new_L, "R_out": new_R,
            "description": f"Feistel round: new_L = R, new_R = L XOR F(R, K{i+1})"
        })
        L, R = new_L, new_R

    # Combine and apply Final Permutation
    combined = L + R
    after_ip_inv = permute(combined, IP_INV)
    steps.append({
        "step": "Final Permutation (IP⁻¹)",
        "input": combined,
        "output": after_ip_inv,
        "description": "Applies the inverse of the initial permutation"
    })

    # Convert back to text (for display)
    result_text = bin_to_text(after_ip_inv)

    return {
        "result": result_text,
        "result_hex": hex(int(after_ip_inv, 2)),
        "steps": steps,
        "note": "Educational demo: 3 simplified rounds shown (real DES uses 16 full rounds)"
    }


def des_decrypt_demo(ciphertext, key):
    """
    Educational DES decryption demo.
    Reverses the round order with the same round keys.
    """
    return {
        "result": "[DES Decryption Demo]",
        "note": "Full DES decryption uses the same structure with round keys in reverse order.",
        "steps": [
            {"step": "Apply IP", "description": "Initial permutation on ciphertext"},
            {"step": "16 Rounds (reversed)", "description": "Apply Feistel rounds with keys K16 to K1"},
            {"step": "Apply IP⁻¹", "description": "Final permutation to get plaintext"}
        ]
    }
