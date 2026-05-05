from fastapi import HTTPException

from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.models.core_model.authentication_model.user_model import User
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.models.pipelines_context.registration_context import RegistrationContext
from app.models.dependencies_model.step import Step


class UserCreationStep(Step):
    def __init__(self, auth_depends: AuthenticationDependencies):
        self.auth_depends = auth_depends
        self.logger = get_logger("UserCreationStep")

    async def run(self, ctx: RegistrationContext):
        # One email per user, no duplication
        if await self.auth_depends.user_service.get_by_email(ctx.request_data.email):
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail=f"EMAIL {ctx.request_data.email} ALREADY EXIST"
            )

            raise HTTPException(400, "Invalid Credential")

        # Unique username
        if await self.auth_depends.user_service.get_by_username(ctx.request_data.username):
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail=f"USERNAME {ctx.request_data.username} ALREADY EXIST"
            )

            raise HTTPException(400, "Invalid Credential")

        user = User(username=ctx.request_data.username, email=ctx.request_data.email)

        # This method hash the password
        user.set_password(ctx.request_data.password)

        # Create user and get the id
        user_id = await self.auth_depends.user_service.create_user(user.to_dict())
        user._id = user_id
        ctx.user = user

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: user created successfully",
            user_id=str(ctx.user._id),
        )

        return ctx
