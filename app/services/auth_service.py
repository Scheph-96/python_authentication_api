from app.services.user_service import UserService
from app.services.refresh_token_service import RefreshTokenService
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.utils.jwt import create_access_token, hash_token
from fastapi import HTTPException
from argon2.exceptions import VerifyMismatchError, InvalidHashError

"""
    Here lies all or authentication process. If we want to add other type of authentication it will be here
    
    The data here is safe to process, we already went through the sanitization and validation with the SignUpSchema in the controller
"""


class AuthService:
    def __init__(self, user_service: UserService, refresh_token: RefreshTokenService, base_repository: BaseRepository):
        self.user_service = user_service
        self.refresh_token = refresh_token
        self.base_repository = base_repository

    """
        Authenticate a user
        
        We want to log our users in whether with the 
        email or the username

        Raises:
            HTTPException: the request body has to contain email or username otherwise the request is rejected
            
            HTTPException: if no record match with the provided data we reject the request. No user match thus invalid email or username
            
            HTTPException: password verification failed. Invalid password
    """

    async def login(self, data: dict):

        # If the request provide a username attribute, the login is performed with username
        if data.get("username"):
            user = await self.user_service.get_by_username(data["username"])

        # If the request provide a email attribute, the login is performed with the email
        elif data.get("email"):
            user = await self.user_service.get_by_email(data["email"])
        if not user:
            raise HTTPException(401, "Invalid credentials")

        user = User(**user)

        try:
            user.verify_password(data["password"])
        except VerifyMismatchError:
            raise HTTPException(401, "Invalid credentials")
        except InvalidHashError:
            print(user.to_dict())
            raise HTTPException(401, "Invalid credentials")

        access_token = create_access_token(str(user._id))
        refresh_token = await self.refresh_token.create_refresh_token(str(user._id))

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def validate_email(self, data: dict):
        # First we hash the code
        code_hash = hash_token(data.get("code"))
        
        # Now we compare the hashed code and the user with our database record
        email_validation_code = await self.base_repository.find({
            "user_id": data.get("user_id"), 
            "code_hash": code_hash
        })
        
        # If there is no match reject the request
        if not email_validation_code:
            raise HTTPException(400, "Invalid or expired code")
        
        # If there is a match we delete code record
        await self.base_repository.delete(email_validation_code["_id"])
        
        # And finally we update the user status
        await self.user_service.update_user(data.get("user_id"), {"is_verified": True})
        
        return {"status": "verified"}
        

    def password_recovery():
        pass
