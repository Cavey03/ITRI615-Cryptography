def _parse_shift(key: str) -> int:
    try:
        shift = int(key.strip())
    except ValueError:
        raise ValueError("Caesar key must be a whole number (e.g. 3).")
    if not 1 <= shift <= 25:
        raise ValueError("Caesar key must be between 1 and 25.")
    return shift


def encrypt(plaintext: str, key: str) -> str:
    shift = _parse_shift(key)
    result = []
    for char in plaintext:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    shift = _parse_shift(key)
    result = []
    for char in ciphertext:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)
