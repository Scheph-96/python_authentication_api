# API Endpoints

## Authentication

### POST /auth_api/v1/process/authenticate/register/
```
--------Create a user--------

Request:
{
    "email": "..." or "username": "...",
    "password": "..."
}

Response:
{
    "user_id": "..."
}
```

### POST /auth_api/v1/process/authenticate/login/
```
--------Login--------

Request:
{
    "email": "..." or "username": "...",
    "password": "..."
}

Response:
{
    "access_token": "...",
    "refresh_token": "..."
}
```

### POST /auth_api/v1/process/authenticate/logout/
```
--------Logout--------

Request:
{
    "refresh_token": "..."
}

Response:
{
    "status": "Logged Out"
}
```

### POST /auth_api/v1/process/authenticate/validate_email/
```
--------Validate Email--------

Request:
{
    "user_id": "...",
    "code": "..."
}

Response:
{
    {"status": "verified"}
}
```

### POST /auth_api/v1/process/authenticate/validate_email/retry/
```
--------Retry Email Validation--------

Request:
{
    "user_id": "..."
}

Response:
{
    {"status": "Email Resent"}
}
```

### POST /auth_api/v1/process/authenticate/refresh/tokens/
```
--------Refresh Tokens--------

Request:
{
    "refresh_token": "..."
}

Response:
{
    "access_token": "...",
    "refresh_token": "..."
}
```

### POST /auth_api/v1/process/authenticate/password_recovery/forgot/
```
--------Password Forgotten--------

Request:
{
    "email": "..."
}

Response:
{
    "password_recovery_token": "..."
}
```

### POST /auth_api/v1/process/authenticate/password_recovery/reset
```
--------Resetting Password--------

Request:
{
    "token": "...",
    "new_password": "..."
}

Response:
{
    "status": "Password updated"
}
```

## Authorization

### POST /auth_api/v1/process/authorize/create_role/
```
--------Creare Role--------

Request:
{
    "description": "..."
    "role_name": "..."
}

Response:
{
    "role_id": "..."
}
```

### POST /auth_api/v1/process/authorize/assign_role/
```
--------Assign Role To User--------

Request:
{
    "role_id": "..."
    "user_id": "..."
}

Response:
{
    "user_role_id": "..."
}
```

### POST /auth_api/v1/process/authorize/remove_user_role/
```
--------Remove Role From User--------

Request:
{
    "role_id": "..."
    "user_id": "..."
}

Response:
{
    "user_role_id": "..."
}
```

### POST /auth_api/v1/process/authorize/delete_role/
```
--------Delete Role--------

Request:
{
    "role_id": "..."
}

Response:
{
    "role_id": "..."
}
```

### POST /auth_api/v1/process/authorize/create_permissions/
```
--------Create Permission--------

Request:
{
    "permission_name": "..."
}

Response:
{
    "permission_id": "..."
}
```

### POST /auth_api/v1/process/authorize/assign_permission/
```
--------Assign Permission To Role--------

Request:
{
    "role_id": "..."
    "permission_id": "..."
}

Response:
{
    "role_permission_id": "..."
}
```

### POST /auth_api/v1/process/authorize/remove_role_permission/
```
--------Remove Permission From Role--------

Request:
{
    "role_id": "..."
    "permission_id": "..."
}

Response:
{
    "role_permission_id": "..."
}
```

POST /auth_api/v1/process/authorize/delete_permission/
```
--------Delete Permission--------

Request:
{
    "permission_id": "..."
}

Response:
{
    permission_id": "..."
}
```