from fastapi import HTTPException

from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.models.core_model.authentication_model.user_model import User
from app.models.dependencies_model.authorization_dependencies import AuthorizationDependencies
from app.utils.resources import dict_string_to_objectid, string_to_objectid


class AuthorizationService:
    def __init__(self, autho_depends: AuthorizationDependencies):
        self.autho_depends = autho_depends
        self.logger = get_logger("AuthorizationService")

    async def create_role(self, data: dict):
        """
            Creation of a role.

            We allow the creation of roles without permission
            but to assign that role permission(s) has/ve to
            be created first.

            A role cannot be assigned without permission
        :param data:
        :return:
        """

        role = await self.autho_depends.role_service.find_role_by_name(data["role_name"])

        # If a role already exist with this name stop the process
        if role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=role["_id"],
                detail="THIS ROLE ALREADY EXIST"
            )
            raise HTTPException(401, "Invalid data")

        # Create role and insert in database
        role_id = await self.autho_depends.role_service.create_role(data)

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            role_id=role_id,
            detail="ROLE CREATED SUCCESSFULLY"
        )

        return {"role_id": role_id}

    async def assign_role_to_user(self, data: dict):

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])

        # If the role does not exist we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="ROLE DOES NOT EXIST"
            )
            raise HTTPException(400, "Unable to proceed")

        # Does that role has permission(s) ?
        permission = await self.autho_depends.role_permission_service.find_role_permission_by_role_id(str(role["_id"]))

        # If it doesn't it cannot be assigned
        if not permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="ROLE HAS NO PERMISSION THUS CANNOT BE ASSIGNED"
            )
            raise HTTPException(400, "Unable to proceed")

        # Get the user
        user = await self.autho_depends.user_service.get_by_id(data["user_id"])

        # If the user does not exist we can't proceed
        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="USER DOES NOT EXIST"
            )
            raise HTTPException(400, "Unable to proceed")

        # Now we check if the user has the role assigned to him
        user_role = await self.autho_depends.user_role_service.find_user_role({"role_id": string_to_objectid(data["role_id"]), "user_id": string_to_objectid(data["user_id"])})

        # If user_role then the role is already assigned to the user, there is nothing to do
        if user_role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                user_role = user_role["_id"],
                detail="USER ALREADY HAS THIS ROLE"
            )
            raise HTTPException(400, "Unable to proceed")

        # Now we can assign the role to the user
        user_role_id = await self.autho_depends.user_role_service.create_user_role(dict_string_to_objectid(data))

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="ROLE ASSIGNED SUCCESSFULLY",
            user_id=data["user_id"],
            role_id=data["role_id"]
        )

        # Recompute user permissions
        self.autho_depends.background_tasks.add_task(self._recompute_permissions, data["user_id"])

        return {"user_role_id": user_role_id}

    async def remove_role_from_user(self):
        pass

    async def delete_role(self):
        pass

    async def create_permission(self):
        pass

    async def assign_permission_to_role(self):
        pass

    async def remove_permission_from_role(self):
        pass

    async def _recompute_permissions(self, user_id: str):
        """
            How it works

            Whenever something changes:

            Event	                        Action
            role assigned	                recompute permissions
            role removed	                recompute
            permission added to role	    recompute all affected users
            permission removed	            recompute

            So permission resolution happens at mutation time not at request time

        :param user_id: the user to update
        """

        user_roles = await self.autho_depends.user_role_service.find_user_role_by_user_id(user_id, options={"_id": 0, "role_id": 1})

        # If there is no user_roles it means that the user has no role assigned
        if not user_roles:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                user_id=user_id,
                detail="THIS USER HAS NO ROLE"
            )
            await self.autho_depends.user_service.update_user(user_id, {"effective_permissions": []})
            return

        # Create a list of role_id
        role_ids = [user_role["role_id"] for user_role in user_roles]

        # With the role_id list we get the role_permissions.
        # Like return the role_permission entry for each
        # role_id in the list
        role_permissions = await self.autho_depends.role_permission_service.find_role_permission_by_role_ids(role_ids, options={"_id": 0, "role_permission": 1})

        # If there is no role_permission it means that
        # the role doesn't have permissions assigned
        # As each role has one or many permissions
        # So maybe the role was created but the permissions
        # were not
        if not role_permissions:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_ids=role_ids,
                detail="THESE ROLES HAVE NO PERMISSIONS"
            )
            await self.autho_depends.user_service.update_user(user_id, {"effective_permissions": []})
            return

        # Create a list of permission_id
        permission_ids = [role_permission["permission_id"] for role_permission in role_permissions]

        # With the permission_id list we get permissions name
        # For each permission_id the name or the label of that
        # permission is returned
        permissions = await self.autho_depends.permission_service.find_permission_by_ids(permission_ids, {"_id": 0, "permission_name": 1})

        # Create a list of permission names
        permissions = [permission["permission_name"] for permission in permissions]

        # Assign the permissions name list to the user
        # effective_permissions represent a cache of user permissions
        await self.autho_depends.user_service.update_user(user_id, {"effective_permissions": permissions})

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSIONS RECOMPUTED SUCCESSFULLY"
        )