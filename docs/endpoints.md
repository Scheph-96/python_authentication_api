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
```

### POST /auth_api/v1/process/authorize/assign_role/
```
--------Assign Role To User--------
```

### POST /auth_api/v1/process/authorize/remove_user_role/
```
--------Remove Role From User--------
```

### POST /auth_api/v1/process/authorize/delete_role/
```
--------Delete Role--------
```

### POST /auth_api/v1/process/authorize/create_permissions/
```
--------Create Permission--------
```

### POST /auth_api/v1/process/authorize/assign_permission/
```
--------Assign Permission To Role--------
```

### POST /auth_api/v1/process/authorize/remove_role_permission/
```
--------Remove Permission From Role--------
```

POST /auth_api/v1/process/authorize/delete_permission/
```
--------Delete Permission--------
```