import os


def read_text(path: str, encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def write_text(path: str, data: str, encoding: str = "utf-8") -> None:
    with open(path, "w", encoding=encoding) as f:
        f.write(data)


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def suggest_output_path(input_path: str, suffix: str = "_encrypted") -> str:
    base, ext = os.path.splitext(input_path)
    return f"{base}{suffix}{ext}"
