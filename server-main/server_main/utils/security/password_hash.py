from hashlib import sha256


def hash_password(password: str) -> str:
    hash = sha256(bytes(password, "utf-8"))
    return hash.hexdigest()
