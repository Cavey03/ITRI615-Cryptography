import string

ALPHABET = string.ascii_uppercase


def _build_cipher_alpha(key: str) -> str:
    key_clean = "".join(dict.fromkeys(c for c in key.upper() if c in ALPHABET))
    remaining = "".join(c for c in ALPHABET if c not in key_clean)
    return key_clean + remaining


def encrypt(plaintext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")
    cipher_alpha = _build_cipher_alpha(key)
    table = str.maketrans(
        ALPHABET + ALPHABET.lower(),
        cipher_alpha + cipher_alpha.lower()
    )
    return plaintext.translate(table)


def decrypt(ciphertext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")
    cipher_alpha = _build_cipher_alpha(key)
    table = str.maketrans(
        cipher_alpha + cipher_alpha.lower(),
        ALPHABET + ALPHABET.lower()
    )
    return ciphertext.translate(table)
