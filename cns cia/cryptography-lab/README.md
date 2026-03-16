# 🔐 Cryptography Interactive Learning Lab

An interactive web application for learning and demonstrating classical and modern cryptography algorithms. Built with Flask (Python) and Vanilla JS.

## Project Structure

```
cryptography-lab/
├── app.py                  # Flask backend + API routes
├── algorithms/
│   ├── caesar.py           # Caesar cipher
│   ├── vigenere.py         # Vigenere cipher
│   ├── hill.py             # Hill cipher (matrix)
│   ├── playfair.py         # Playfair cipher
│   ├── railfence.py        # Rail Fence cipher
│   ├── rowcolumn.py        # Row-Column Transposition
│   ├── des_demo.py         # DES educational demo
│   ├── aes_demo.py         # AES educational demo
│   ├── rsa.py              # RSA algorithm
│   ├── diffie_hellman.py   # Diffie-Hellman key exchange
│   ├── elgamal.py          # ElGamal cryptosystem
│   └── ecc_demo.py         # Elliptic Curve Cryptography
├── templates/
│   └── index.html          # Single-page frontend
├── static/
│   ├── style.css           # UI styles
│   └── script.js           # Frontend logic
└── README.md
```

## Installation

### 1. Install Python dependencies

```bash
pip install flask numpy
```

### 2. Run the Flask server

```bash
cd cryptography-lab
python app.py
```

### 3. Open in browser

```
http://localhost:5000
```

## Algorithms Implemented

| Algorithm | Type | Key Concept |
|-----------|------|-------------|
| Caesar Cipher | Classical | Alphabet shift by fixed value |
| Vigenere Cipher | Classical | Polyalphabetic substitution with keyword |
| Hill Cipher | Classical | Matrix multiplication mod 26 |
| Playfair Cipher | Classical | Digraph substitution with 5×5 matrix |
| Rail Fence | Classical | Zigzag transposition |
| Row-Column Transposition | Classical | Columnar rearrangement by key |
| DES | Modern Symmetric | Feistel network, 16 rounds, 56-bit key |
| AES | Modern Symmetric | SubBytes, ShiftRows, MixColumns, AddRoundKey |
| RSA | Asymmetric | Public/private key pair, prime factoring |
| Diffie-Hellman | Key Exchange | Discrete logarithm problem |
| ElGamal | Asymmetric | Probabilistic encryption, DH-based |
| ECC | Asymmetric | Elliptic curve point multiplication |

## Features

- Interactive encrypt/decrypt for all 12 algorithms
- Step-by-step **Explain Mode** toggle
- Visual diagrams: alphabet strip, matrices, rail fence grid, ECC canvas
- Alice & Bob simulation for DH and ElGamal
- RSA key generation from primes
- Light / Dark mode
- Copy output button
- Example input button for each algorithm

## API Endpoints

```
POST /encrypt/caesar       POST /decrypt/caesar
POST /encrypt/vigenere     POST /decrypt/vigenere
POST /encrypt/hill         POST /decrypt/hill
POST /encrypt/playfair     POST /decrypt/playfair
POST /encrypt/railfence    POST /decrypt/railfence
POST /encrypt/rowcolumn    POST /decrypt/rowcolumn
POST /encrypt/des          POST /decrypt/des
POST /encrypt/aes          POST /decrypt/aes
POST /rsa/generate
POST /encrypt/rsa          POST /decrypt/rsa
POST /diffie-hellman/simulate
POST /elgamal/generate
POST /encrypt/elgamal      POST /decrypt/elgamal
POST /ecc/simulate
```
