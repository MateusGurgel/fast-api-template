import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode()
    hashed_password_bytes = hashed_password.encode()
    print("Print Testeee: ", plain_password)
    print("Print Testeee: ", hashed_password)
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


def get_salt() -> bytes:
    return bcrypt.gensalt()


def get_password_hash(password: str) -> str:
    password_bytes = password.encode()
    salt_bytes = get_salt()
    hashed_password = bcrypt.hashpw(password_bytes, salt=salt_bytes).decode()
    print("Print Testeee: ", hashed_password)
    return hashed_password
