from argon2 import PasswordHasher


pwd_context = PasswordHasher()


def get_hash_password(password: str):
    hash_password = pwd_context.hash(password)
    return hash_password

















