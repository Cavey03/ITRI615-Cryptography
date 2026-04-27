def _key_stream(key: str, length: int) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes(key_bytes[i % len(key_bytes)] for i in range(length))


def encrypt(plaintext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")
    data = plaintext.encode("utf-8")
    xored = bytes(a ^ b for a, b in zip(data, _key_stream(key, len(data))))
    return xored.hex()


def decrypt(ciphertext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")
    try:
        data = bytes.fromhex(ciphertext.strip())
    except ValueError:
        raise ValueError("Invalid ciphertext — expected hex-encoded Vernam output.")
    xored = bytes(a ^ b for a, b in zip(data, _key_stream(key, len(data))))
    return xored.decode("utf-8")
