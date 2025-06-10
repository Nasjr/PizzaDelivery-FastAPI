
# auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from settings import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def create_refresh_token(data: dict):
    return create_access_token(data, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        return payload  # or payload.get("sub") for user
    except JWTError:
        return None

