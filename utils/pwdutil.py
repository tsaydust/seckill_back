from passlib.hash import pbkdf2_sha256

def hash_pwd(pwd):
    return pbkdf2_sha256.hash(pwd)

def verify_pwd(pwd,hashed_pwd):
    return pbkdf2_sha256.verify(pwd,hashed_pwd)

