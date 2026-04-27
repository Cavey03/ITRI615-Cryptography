def _get_order(key: str):
    # Returns the column order based on sorted key
    return sorted(range(len(key)), key=lambda k: key[k])


def encrypt(plaintext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")

    key_len = len(key)
    text = plaintext.replace(" ", "")  # optional: remove spaces
    rows = (len(text) + key_len - 1) // key_len

    # Pad text if necessary
    padded = text.ljust(rows * key_len, 'X')

    # Create matrix
    matrix = [padded[i:i + key_len] for i in range(0, len(padded), key_len)]

    order = _get_order(key)

    # Read columns in key order
    ciphertext = ""
    for col in order:
        for row in matrix:
            ciphertext += row[col]

    return ciphertext


def decrypt(ciphertext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")

    key_len = len(key)
    rows = (len(ciphertext) + key_len - 1) // key_len

    order = _get_order(key)

    # Create empty matrix
    matrix = [[''] * key_len for _ in range(rows)]

    index = 0
    for col in order:
        for row in range(rows):
            if index < len(ciphertext):
                matrix[row][col] = ciphertext[index]
                index += 1

    # Read row-wise
    plaintext = ""
    for row in matrix:
        plaintext += "".join(row)

    return plaintext.rstrip('X')  # remove padding