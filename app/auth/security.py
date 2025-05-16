from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from datetime import datetime
from config import settings
import os

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            try:
                payload = jwt.decode(
                    credentials.credentials,
                    settings.JWT_SECRET,
                    algorithms=[settings.JWT_ALGORITHM]
                )
                if payload.get("exp") < datetime.now().timestamp():
                    raise HTTPException(status_code=403, detail="Token expired")
                return payload
            except JWTError:
                raise HTTPException(status_code=403, detail="Invalid token")
        raise HTTPException(status_code=403, detail="Invalid authorization")

def verify_csrf_token(request: Request):
    token = request.cookies.get("csrf_token")
    if not token or not verify_state_token(token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

def generate_state_token() -> str:
    return jwt.encode(
        {"state": os.urandom(16).hex(), "iat": datetime.now().timestamp()},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_state_token(token: str) -> bool:
    try:
        jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return True
    except:
        return False
