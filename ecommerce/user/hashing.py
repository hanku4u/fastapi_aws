from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)