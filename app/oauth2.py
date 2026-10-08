from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "7f3c9e1a84b6d2f0c5a8e7b13d9f46c2a1e8b5f703c6d9a2e4f8b1c7d5e9a3f6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
