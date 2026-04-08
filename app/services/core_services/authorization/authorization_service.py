from fastapi import HTTPException
from pymongo.synchronous.auth import authenticate

from app.core.config import Settings
from app.core.errors.authorization.authorization_errors import RoleAlreadyExists, RoleNotFound, UserNotFound, \
    RoleAlreadyAssigned, RoleNotAssigned, PermissionAlreadyExists, PermissionNotFound, PermissionAlreadyAssigned, \
    PermissionNotAssigned
from app.core.logging.logger import get_logger
from app.models.dependencies_model.authorization_dependencies import AuthorizationDependencies
from app.utils.resources import dict_string_to_objectid, string_to_objectid, build_insert_many_document_list


########### REMEMBER TO ADD THE FEATURE THAT ALLOW PERMISSION CREATION ON ROLE CREATION

class AuthorizationService:
    def __init__(self, autho_depends: AuthorizationDependencies):
        self.autho_depends = autho_depends
        self.logger = get_logger("AuthorizationService")

    async def create_role(self, data: dict):
        """
            Creation of a role.
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
            raise RoleAlreadyExists(role["role_name"])

        # Create role and insert in database
        role_id = await self.autho_depends.role_service.create_role(data)

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            role_id=role_id,
            detail="ROLE CREATED SUCCESSFULLY"
        )

        return {"role_id": role_id}

    async def assign_role_to_user(self, data: dict):
        """
            Assign a role to a user
        :param data:
        :return:
        """

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])

        # If the role does not exist we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="ROLE DOES NOT EXIST"
            )
            raise RoleNotFound(data["role_id"])

        # Get the user
        user = await self.autho_depends.user_service.get_by_id(data["user_id"])

        # If the user does not exist we can't proceed
        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="USER DOES NOT EXIST"
            )
            raise UserNotFound(data["user_id"])

        # Now we check if the user has the role assigned to him
        user_role = await self.autho_depends.user_role_service.find_user_role(
            {"role_id": string_to_objectid(data["role_id"]), "user_id": string_to_objectid(data["user_id"])})

        # If user_role then the role is already assigned to the user, there is nothing to do
        if user_role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                user_role=user_role["_id"],
                detail="USER ALREADY HAS THIS ROLE"
            )
            raise RoleAlreadyAssigned(data["role_id"])

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

    async def remove_role_from_user(self, data: dict):
        """
            Remove a role from a user
        :param data:
        :return:
        """

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])

        # If the role does not exist we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=f"{data["role_id"]}",
                detail="ROLE DOES NOT EXIST"
            )
            raise RoleNotFound(data["role_id"])

        # Get the user
        user = await self.autho_depends.user_service.get_by_id(data["user_id"])

        # If the user does not exist we can't proceed
        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                user_id=f"{data["user_id"]}",
                detail="USER DOES NOT EXIST"
            )
            raise UserNotFound(data["user_id"])

        # Now we check if the user has the role assigned to him
        user_role = await self.autho_depends.user_role_service.find_user_role(
            {"role_id": string_to_objectid(data["role_id"]), "user_id": string_to_objectid(data["user_id"])})

        # If no user_role then the user doesn't have this role, there is nothing to do
        if not user_role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=data["role_id"],
                user_id=data["user_id"],
                detail="USER DOES NOT HAVE THIS ROLE"
            )
            raise RoleNotAssigned(role["role_name"])

        # Delete user_role record of that user and the role
        await self.autho_depends.user_role_service.delete_user_role(str(user_role["_id"]))

        # Recompute user permissions
        self.autho_depends.background_tasks.add_task(self._recompute_permissions, data["user_id"])

        return {"user_role_id": str(user_role["_id"])}

    async def delete_role(self, data: dict):
        """
            Delete a role
        :param data:
        :return:
        """

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])

        # If role is null then there is no role to delete, we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=data["role_id"],
                detail="THIS ROLE DOES NOT EXIST"
            )

            raise RoleNotFound(data["role_id"])

        # Get the user_role
        user_roles = await self.autho_depends.user_role_service.find_user_role_by_role_id(data["role_id"])

        # If user_role is not null it means that there are users
        # with this role. So before we delete the role we first have the delete
        # the relation role_permissions and finally the role
        if user_roles:
            await self.autho_depends.user_role_service.delete_many_user_role_by_role_id(data["role_id"])

        # Get role_permissions
        role_permissions = await self.autho_depends.role_permission_service.find_role_permission_by_role_id(
            data["role_id"])

        # If role_permissions is not null it means that there are permissions
        # on this role. So before we delete the role we first have the delete
        # the relation role_permissions and finally the role
        if role_permissions:
            # Delete role_permissions
            await self.autho_depends.role_permission_service.delete_many_role_permissions_by_role_id(data["role_id"])

        # Delete role
        await self.autho_depends.role_service.delete_role(data["role_id"])

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            role_id=data["role_id"],
            detail="ROLE DELETED SUCCESSFULLY"
        )

        return {"role_id": data["role_id"]}

    async def create_permissions(self, data: dict):
        """
            Create a permissions
        :param data:
        :return:
        """

        # Get permissions
        permission = await self.autho_depends.permission_service.find_permission_by_name(data["permission_name"])

        # if the permission already exist, we can't proceed
        if permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                permissions=data["permission_name"],
                detail="PERMISSION ALREADY EXIST"
            )
            raise PermissionAlreadyExists(data["permission_name"])

        # Insert all the permissions and retrieve ids
        permission_id = await self.autho_depends.permission_service.create_permission(data)

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            role_permissions=permission_id,
            detail="PERMISSIONS CREATED SUCCESSFULLY"
        )

        return {"permission_id": permission_id}

    async def assign_permission_to_role(self, data: dict):
        """
            Assign a permission to a role
        :param data:
        :return: The assigned role_permission id
        """

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])

        # If the role does not exist we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="ROLE DOES NOT EXIST"
            )
            raise RoleNotFound(data["role_id"])

        # Get the user
        permission = await self.autho_depends.permission_service.find_permission_by_id(data["permission_id"])

        # If the permission does not exist we can't proceed
        if not permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="PERMISSION DOES NOT EXIST"
            )
            raise PermissionNotFound(data["permission_id"])

        # Now we check if the role has the permission assigned
        role_permission = await self.autho_depends.role_permission_service.find_role_permission(
            {"role_id": string_to_objectid(data["role_id"]), "permission_id": string_to_objectid(data["permission_id"])})

        # If role_permission then the permission is already assigned to the role, there is nothing to do
        if role_permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_permission=role_permission["_id"],
                detail="ROLE ALREADY HAS THIS PERMISSION"
            )
            raise PermissionAlreadyAssigned(data["permission_id"])

        # Now we can assign the role to the user
        role_permission_id = await self.autho_depends.role_permission_service.create_role_permission(dict_string_to_objectid(data))

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSION ASSIGNED SUCCESSFULLY",
            role_id=data["role_id"],
            permission_id=data["permission_id"]
        )

        # Get the user_roles that have the role_id
        user_roles = await self.autho_depends.user_role_service.find_user_role_by_role_id(data["role_id"])

        # From the user_roles we get the user_id. So each user that has the specified role
        for user_role in user_roles:
            # Recompute user permissions
            self.autho_depends.background_tasks.add_task(self._recompute_permissions, user_role["user_id"])

        return {"role_permission_id": role_permission_id}

    async def remove_permission_from_role(self, data: dict):
        """
            Remove a permission from a role
        :param data:
        :return: The deleted role_permission id
        """

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])

        # If the role does not exist we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=f"{data["role_id"]}",
                detail="ROLE DOES NOT EXIST"
            )
            raise RoleNotFound(data["role_id"])

        # Get the permission
        permission = await self.autho_depends.permission_service.find_permission_by_id(data["permission_id"])

        # If the permission does not exist
        if not permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                permission_id=f"{data["permission_id"]}",
                detail="PERMISSION DOES NOT EXIST"
            )
            raise PermissionNotFound(data["permission_id"])

        # Get role_permission
        role_permission = await self.autho_depends.role_permission_service.find_role_permission(
            {"role_id": data["role_id"], "permission_id": data["permission_id"]})

        # If the role_permission does not exist
        if not role_permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=data["role_id"],
                permission_id=data["permission_id"],
                detail="PERMISSION NOT ASSIGNED TO ROLE"
            )
            raise PermissionNotAssigned(data["permission_id"])

        # Delete role_permission record of that permission and role
        await self.autho_depends.role_permission_service.delete_one_role_permission_by_id(role_permission["_id"])

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSION REMOVED SUCCESSFULLY",
            role_id=data["role_id"],
            permission_id=data["permission_id"]
        )

        # Get the user_roles that have the role_id
        user_roles = await self.autho_depends.user_role_service.find_user_role_by_role_id(data["role_id"])

        # From the user_roles we get the user_id. So each user that has the specified role
        for user_role in user_roles:
            # Recompute user permissions
            self.autho_depends.background_tasks.add_task(self._recompute_permissions, user_role["user_id"])

        return {"role_permission_id": role_permission["_id"]}

    async def delete_permission(self):
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

        user_roles = await (self.autho_depends.user_role_service
                            .find_user_role_by_user_id(user_id, options={"_id": 0, "role_id": 1}))

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
        role_permissions = await (self.autho_depends.role_permission_service
                                  .find_role_permission_by_role_ids(role_ids, options={"_id": 0, "role_permission": 1}))

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
        permissions = await (self.autho_depends.permission_service
                             .find_permission_by_ids(permission_ids, {"_id": 0, "permission_name": 1}))

        # Create a list of permission names
        permissions = [permission["permission_name"] for permission in permissions]

        # Assign the permissions name list to the user
        # effective_permissions represent a cache of user permissions
        await self.autho_depends.user_service.update_user(user_id, {"effective_permissions": permissions})

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSIONS RECOMPUTED SUCCESSFULLY"
        )
