from bson import ObjectId

from app.core.config import Settings
from app.core.errors.authorization.authorization_errors import RoleAlreadyExists, RoleNotFound, UserNotFound, \
    RoleAlreadyAssigned, RoleNotAssigned, PermissionAlreadyExists, PermissionNotFound, PermissionAlreadyAssigned, \
    PermissionNotAssigned
from app.core.logging.logger import get_logger
from app.models.dependencies_model.authorization_dependencies import AuthorizationDependencies
from app.utils.resources import dict_string_to_objectid, string_to_objectid


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
        :return: user_role id
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
        :return: The deleted role id
        """

        # Get the role
        role = await self.autho_depends.role_service.find_role_by_id(data["role_id"])
        #
        # # If role is null then there is no role to delete, we can't proceed
        if not role:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_id=data["role_id"],
                detail="THIS ROLE DOES NOT EXIST"
            )

            raise RoleNotFound(data["role_id"])

        # Get the user_role
        user_roles = await self.autho_depends.user_role_service.get_user_role_user_ids_by_role_id(data["role_id"])

        # If user_role is not null it means that there are users
        # with this role. So before we delete the role we first have the delete
        # the relation role_permissions and finally the role
        if user_roles:
            await self.autho_depends.user_role_service.delete_many_user_role_by_role_id(data["role_id"])

        # # Get role_permissions
        role_permissions = await self.autho_depends.role_permission_service.find_role_permission_by_role_id(data["role_id"])

        # If role_permissions is not null it means that there are permissions
        # on this role. So before we delete the role we first have the delete
        # the relation role_permissions and finally the role
        if role_permissions:
            # Delete role_permissions
            await self.autho_depends.role_permission_service.delete_many_role_permissions_by_role_id(data["role_id"])

        # # Delete role
        await self.autho_depends.role_service.delete_role(data["role_id"])

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            role_id=data["role_id"],
            detail="ROLE DELETED SUCCESSFULLY"
        )

        if len(user_roles) > 0:
            # Recompute user permissions
            self.autho_depends.background_tasks.add_task(self._recompute_permissions, user_roles[0]["user_ids"])

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
            {"role_id": string_to_objectid(data["role_id"]),
             "permission_id": string_to_objectid(data["permission_id"])})

        # If role_permission then the permission is already assigned to the role, there is nothing to do
        if role_permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                role_permission=role_permission["_id"],
                detail="ROLE ALREADY HAS THIS PERMISSION"
            )
            raise PermissionAlreadyAssigned(data["permission_id"])

        # Now we can assign the role to the user
        role_permission_id = await self.autho_depends.role_permission_service.create_role_permission(
            dict_string_to_objectid(data))

        # Get the user_role
        user_roles = await self.autho_depends.user_role_service.get_user_role_user_ids_by_role_id(data["role_id"])

        if len(user_roles) > 0:
            # Recompute user permissions
            self.autho_depends.background_tasks.add_task(self._recompute_permissions, user_roles[0]["user_ids"])

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSION ASSIGNED SUCCESSFULLY",
            role_id=data["role_id"],
            permission_id=data["permission_id"]
        )

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

        # Get the user_role
        user_roles = await self.autho_depends.user_role_service.get_user_role_user_ids_by_role_id(data["role_id"])

        if len(user_roles) > 0:
            # Recompute user permissions
            self.autho_depends.background_tasks.add_task(self._recompute_permissions, user_roles[0]["user_ids"])

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSION REMOVED SUCCESSFULLY",
            role_id=data["role_id"],
            permission_id=data["permission_id"]
        )

        return {"role_permission_id": str(role_permission["_id"])}

    async def delete_permission(self, data: dict):
        """
            Delete a permission
        :param data:
        :return: The deleted permission id
        """

        # Get the permission
        permission = await self.autho_depends.permission_service.find_permission_by_id(data["permission_id"])

        # If permission is null then there is no permission to delete, we can't proceed
        if not permission:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                permission_id=data["permission_id"],
                detail="PERMISSION DOES NOT EXIST"
            )

            raise PermissionNotFound(data["permission_id"])

        # Get role_permissions
        role_permissions = await self.autho_depends.role_permission_service.get_user_ids_from_role_permissions(data["permission_id"])

        # If role_permissions is not null it means that the permission is assigned
        # to some roles. SO before we delete the permission we first have to delete
        # the relation role_permissions and finally the permission
        if role_permissions:
            # Delete role_permissions
            await self.autho_depends.role_permission_service.delete_many_role_permissions_by_permission_id(
                data["permission_id"])

        # Delete permission
        await self.autho_depends.permission_service.delete_permission(data["permission_id"])

        if len(role_permissions) > 0:
            # Recompute user permissions
            self.autho_depends.background_tasks.add_task(self._recompute_permissions, role_permissions[0]["user_ids"])

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            permission_id=data["permission_id"],
            detail="PERMISSION DELETED SUCCESSFULLY"
        )

        return {"permission_id": data["permission_id"]}

    async def _recompute_permissions(self, user_id_s: str | list):
        """
            How it works

            Whenever something changes:

            Event	                        Action
            role assigned	                recompute permissions
            role removed	                recompute
            permission added to role	    recompute all affected users
            permission removed	            recompute

            So permission resolution happens at mutation time not at request time

        :param user_id_s: the user to update
        """

        # If the user_id is passed as a unique string we convert it to a list of ObjectId
        # Otherwise (when it's a list) we keep it like that for the query
        user_id_s = [ObjectId(user_id_s)] if isinstance(user_id_s, str) else user_id_s

        # We get the list of permissions group by user_id. The query will return each
        # user with his permissions
        user_permissions = await self.autho_depends.user_role_service.recompute_user_permissions_by_ids(user_id_s)

        # Now we bulk update every user and their effective permissions
        await self.autho_depends.user_service.update_effective_permissions(user_permissions)

        # Some users may have no permissions remaining depending on the kind of
        # operation that trigger the recomputation so those user will not appear in
        # the result of the previous query where we returned the permissions for each user
        returned_ids = {user_permission["user_id"] for user_permission in user_permissions}

        # To fix that we get the ids remaining from the initial list that was passed
        # for the query. Those remaining ids are the ones that no longer have any
        # permission
        missing_ids = set(user_id_s) - returned_ids

        # So we update their effective_permissions to an empty array
        await self.autho_depends.user_service.update_users(list(missing_ids), {"effective_permissions": []})

        self.logger.info(
            Settings.OPERATION_SUCCESS_EVENT_LABEL,
            detail="PERMISSIONS RECOMPUTED SUCCESSFULLY"
        )
