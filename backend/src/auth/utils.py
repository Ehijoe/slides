import bcrypt


# hash a password using bcrypt
def hash_password(password):
    hashed = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

    return hashed


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = bytes(plain_password, "utf-8")
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)