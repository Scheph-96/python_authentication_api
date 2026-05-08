# from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings, Settings
from app.schemas.jwt_schema import JWTSchema
from jose import jwt, JWTError
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib

ALGORITHM = "RS256"

security = HTTPBearer()

"""
    This function hash refresh tokens
"""
def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

"""
    Here we create our access that by default expire after 15 minutes    
"""
def create_access_token(user_id: str, effective_permissions: list):
    # Get the private key from the file
    with open(Settings.PRIVATE_KEY_PATH, "r") as f:
        PRIVATE_KEY = f.read()
        f.close()

    # Expiration now + 15, so the token will last 15 minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # We create our token
    payload = JWTSchema(sub=user_id, iss=settings.ISSUER, exp=expire, effective_permissions=effective_permissions)
    return jwt.encode(payload.model_dump(), PRIVATE_KEY, algorithm=ALGORITHM)

"""
    Token validation. Only for test purpose
"""
# def verify_access_token(http_credentials: HTTPAuthorizationCredentials = Depends(security)):
#     try:
#         # Get the token from the header
#         token = http_credentials.credentials
#
#         # Get the public key from the file
#         with open(Settings.PUBLIC_KEY_PATH, "r") as f:
#             PUBLIC_KEY = f.read()
#             f.close()
#
#         # Retrieve the payload with the token
#         payload_dict = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM], issuer=settings.ISSUER)
#
#         payload = JWTSchema(**payload_dict)
#
#         # Return user_id
#         return payload #user_id
#     except JWTError or ValueError as e:
#         print(e)
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
