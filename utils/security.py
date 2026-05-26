from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

pwd_context = PasswordHasher()


def get_hash_password(password: str):
    hash_password = pwd_context.hash(password)
    return hash_password


def verify_password(plain_password, hashed_password):
    """
    验证密码是否正确
    :param plain_password: 明文
    :param hashed_password: 密文
    :return: True/False
    """
    try:
        result = pwd_context.verify(hashed_password, plain_password)
        return result
    except VerifyMismatchError:
        return False

















