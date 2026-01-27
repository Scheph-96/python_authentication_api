from app.services.user_service import UserService
from app.models.user_model import User
from app.utils.jwt import create_access_token
from fastapi import HTTPException
from argon2.exceptions import VerifyMismatchError, InvalidHashError

"""
    Here lies all or authentication process. If we want to add other type of authentication it will be here
    
    The data here is safe to process, we already went through the sanitization and validation with the SignUpSchema in the controller
"""
class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
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
        
        return create_access_token(str(user._id))
        
    
    def password_recovery():
        pass