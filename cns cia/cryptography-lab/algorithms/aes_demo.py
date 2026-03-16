# AES (Advanced Encryption Standard) - Educational Demonstration
# AES operates on a 4x4 byte matrix (state) with multiple rounds.
# This demo shows the conceptual steps: SubBytes, ShiftRows, MixColumns, AddRoundKey.

# Simplified S-Box (first 16 values for demonstration)
S_BOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

def text_to_state(text):
    """Convert 16-byte text to 4x4 state matrix."""
    text = text[:16].ljust(16)
    return [[ord(text[r*4+c]) for c in range(4)] for r in range(4)]

def state_to_hex(state):
    """Convert state matrix to hex string."""
    return [[hex(state[r][c]) for c in range(4)] for r in range(4)]

def sub_bytes(state):
    """SubBytes: Replace each byte with its S-Box value."""
    return [[S_BOX[state[r][c]] for c in range(4)] for r in range(4)]

def shift_rows(state):
    """ShiftRows: Cyclically shift each row left by its row index."""
    return [state[r][r:] + state[r][:r] for r in range(4)]

def add_round_key(state, key_state):
    """AddRoundKey: XOR state with round key."""
    return [[state[r][c] ^ key_state[r][c] for c in range(4)] for r in range(4)]

def mix_columns_demo(state):
    """MixColumns: Simplified demo (just shows the concept, not full GF(2^8) math)."""
    # Simplified: rotate each column for visual demo
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        # Simplified mix: XOR adjacent bytes
        result[0][c] = col[0] ^ col[1]
        result[1][c] = col[1] ^ col[2]
        result[2][c] = col[2] ^ col[3]
        result[3][c] = col[3] ^ col[0]
    return result

def aes_encrypt_demo(plaintext, key):
    """
    Educational AES demonstration showing the 4 main operations.
    Uses a simplified 2-round version for clarity.
    """
    state = text_to_state(plaintext)
    key_state = text_to_state(key)
    steps = []

    steps.append({
        "step": "Initial State",
        "state": state_to_hex(state),
        "description": "Plaintext arranged into 4x4 byte matrix"
    })

    # Initial AddRoundKey
    state = add_round_key(state, key_state)
    steps.append({
        "step": "AddRoundKey (Initial)",
        "state": state_to_hex(state),
        "description": "XOR plaintext state with the cipher key"
    })

    # 2 demonstration rounds
    for round_num in range(1, 3):
        state = sub_bytes(state)
        steps.append({
            "step": f"Round {round_num}: SubBytes",
            "state": state_to_hex(state),
            "description": "Each byte replaced using the AES S-Box lookup table"
        })

        state = shift_rows(state)
        steps.append({
            "step": f"Round {round_num}: ShiftRows",
            "state": state_to_hex(state),
            "description": f"Row 0: no shift, Row 1: shift 1 left, Row 2: shift 2 left, Row 3: shift 3 left"
        })

        if round_num < 2:  # MixColumns not applied in final round
            state = mix_columns_demo(state)
            steps.append({
                "step": f"Round {round_num}: MixColumns",
                "state": state_to_hex(state),
                "description": "Each column mixed using matrix multiplication in GF(2^8)"
            })

        state = add_round_key(state, key_state)
        steps.append({
            "step": f"Round {round_num}: AddRoundKey",
            "state": state_to_hex(state),
            "description": "XOR current state with the round key"
        })

    result_hex = ''.join(hex(state[r][c])[2:].zfill(2) for r in range(4) for c in range(4))

    return {
        "result": result_hex,
        "steps": steps,
        "note": "Educational demo: 2 simplified rounds shown (real AES-128 uses 10 full rounds)"
    }


def aes_decrypt_demo(ciphertext, key):
    """Educational AES decryption overview."""
    return {
        "result": "[AES Decryption Demo]",
        "note": "AES decryption applies inverse operations in reverse order.",
        "steps": [
            {"step": "AddRoundKey", "description": "XOR with last round key"},
            {"step": "InvShiftRows", "description": "Shift rows right instead of left"},
            {"step": "InvSubBytes", "description": "Apply inverse S-Box"},
            {"step": "InvMixColumns", "description": "Apply inverse column mixing"},
            {"step": "Repeat for all rounds", "description": "10 rounds for AES-128"}
        ]
    }
