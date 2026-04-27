import string


def _build_square(key: str) -> list:
    key = key.upper().replace('J', 'I')
    seen = []
    for c in key:
        if c.isalpha() and c not in seen:
            seen.append(c)
    for c in string.ascii_uppercase.replace('J', ''):
        if c not in seen:
            seen.append(c)
    return [seen[i * 5:(i + 1) * 5] for i in range(5)]


def _find(square: list, char: str) -> tuple:
    for r, row in enumerate(square):
        if char in row:
            return r, row.index(char)


def _prepare(plaintext: str) -> str:
    text = plaintext.upper().replace('J', 'I')
    text = ''.join(c for c in text if c.isalpha())
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 == len(text):
            digraphs.append(a + 'X')
            i += 1
        elif text[i] == text[i + 1]:
            digraphs.append(a + 'X')
            i += 1
        else:
            digraphs.append(a + text[i + 1])
            i += 2
    return ''.join(digraphs)


def encrypt(plaintext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")
    if not any(c.isalpha() for c in plaintext):
        raise ValueError("Plaintext must contain at least one letter.")
    square = _build_square(key)
    prepared = _prepare(plaintext)
    result = []
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i + 1]
        r1, c1 = _find(square, a)
        r2, c2 = _find(square, b)
        if r1 == r2:
            result += [square[r1][(c1 + 1) % 5], square[r2][(c2 + 1) % 5]]
        elif c1 == c2:
            result += [square[(r1 + 1) % 5][c1], square[(r2 + 1) % 5][c2]]
        else:
            result += [square[r1][c2], square[r2][c1]]
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    if not key.strip():
        raise ValueError("Key cannot be empty.")
    square = _build_square(key)
    text = ciphertext.upper().replace('J', 'I')
    text = ''.join(c for c in text if c.isalpha())
    result = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        r1, c1 = _find(square, a)
        r2, c2 = _find(square, b)
        if r1 == r2:
            result += [square[r1][(c1 - 1) % 5], square[r2][(c2 - 1) % 5]]
        elif c1 == c2:
            result += [square[(r1 - 1) % 5][c1], square[(r2 - 1) % 5][c2]]
        else:
            result += [square[r1][c2], square[r2][c1]]
    return ''.join(result)
