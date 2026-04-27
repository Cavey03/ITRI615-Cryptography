import string

ALPHABET = string.ascii_uppercase


def _clean_key(key: str) -> str:
    cleaned = "".join(c.upper() for c in key if c.isalpha())
    if not cleaned:
        raise ValueError("Key must contain at least one letter.")
    return cleaned


def encrypt(plaintext: str, key: str) -> str:
    key = _clean_key(key)
    result = []
    key_index = 0
    for char in plaintext:
        if char.upper() in ALPHABET:
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def decrypt(ciphertext: str, key: str) -> str:
    key = _clean_key(key)
    result = []
    key_index = 0
    for char in ciphertext:
        if char.upper() in ALPHABET:
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)
