from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    user_id = decode_access_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, details="Invalid or expired token")
    return user_id