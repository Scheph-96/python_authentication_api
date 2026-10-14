# API Endpoints

## Authentication

### POST <Settings.API_PREFIX>/authenticate/register/
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

### POST <Settings.API_PREFIX>/authenticate/login/
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

### POST <Settings.API_PREFIX>/authenticate/logout/
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

### POST <Settings.API_PREFIX>/authenticate/validate_email/
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

### POST <Settings.API_PREFIX>/authenticate/validate_email/retry/
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

### POST <Settings.API_PREFIX>/authenticate/refresh/tokens/
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

### POST <Settings.API_PREFIX>/authenticate/password_recovery/forgot/
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

### POST <Settings.API_PREFIX>/authenticate/password_recovery/reset
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

### POST <Settings.API_PREFIX>/authorize/create_role/
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

### POST <Settings.API_PREFIX>/authorize/assign_role/
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

### POST <Settings.API_PREFIX>/authorize/remove_user_role/
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

### POST <Settings.API_PREFIX>/authorize/delete_role/
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

### POST <Settings.API_PREFIX>/authorize/create_permissions/
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

### POST <Settings.API_PREFIX>/authorize/assign_permission/
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

### POST <Settings.API_PREFIX>/authorize/remove_role_permission/
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

### POST <Settings.API_PREFIX>/authorize/delete_permission/
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