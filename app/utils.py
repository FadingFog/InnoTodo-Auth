from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.config import settings


class PasswordHelper:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, raw_password: str, hash_password: str) -> bool:
        return self.context.verify(raw_password, hash_password)

    def get_hash_password(self, raw_password: str) -> str:
        return self.context.hash(raw_password)


class TokenHelper:
    SECRET_KEY: str = '02C8A1wqr/eUA4xBrHH5pvBcaJyBoj6o98tYLK59OEI='
    PRIVATE_SECRET_KEY: str = settings.PRIVATE_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        # data.update({"exp": expire})  # Token expiration disabled
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_jwt

    def create_private_token(self, data: dict) -> str:
        encoded_jwt = jwt.encode(data, self.PRIVATE_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_token_payload(self, token: str):
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        return payload


password_helper = PasswordHelper()
token_helper = TokenHelper()
