# Authorization Interface

## Overview
Authorization comes into action after the user has been authenticated.
It provides access to resources through roles and permissions associated
to roles.

## Authorization Flow
1. User login
2. User data verify and validate
3. The system check what role is associated to the user
4. Permissions are computed and cached into effective_permissions
5. Permissions are stored in the access token which is sent back to the client

## Data Model

### Role
Users have one or several roles granting access to various resources.\
Roles example:
```
user
admin
```

### Permission
Actions related to roles. Depending on the role assigned to a user that
user is granted all the permissions associated to that role, the permissions
represented every action the user can perform such as:

```
user.create
user.edit_profile
```

## Effective Permissions
effective_permissions is a computed cache of all permissions granted to a user through assigned roles.

This avoids resolving roles and permissions on every request.

**IMPORTANT NOTE:**\
The api only provide an **INTERFACE** for authorization management,
it does **not** decide access riles inside consumer applications.

Authorization enforcement must be implemented by the consumer backend.

## Permissions Recompute triggers

Permissions are recomputed when:

- role assigned to user
- role removed from user
- role deleted
- permission assigned to role
- permission removed from role
- permission deleted