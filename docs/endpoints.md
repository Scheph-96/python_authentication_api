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
```

### POST /auth_api/v1/process/authenticate/logout/
```
--------Logout--------
```

### POST /auth_api/v1/process/authenticate/validate_email/
```
--------Validate Email--------
```

### POST /auth_api/v1/process/authenticate/validate_email/retry/
```
--------Retry Email Validation--------
```

### POST /auth_api/v1/process/authenticate/refresh/tokens/
```
--------Refresh Tokens--------
```

### POST /auth_api/v1/process/authenticate/password_recovery/forgot/
```
--------Password Forgotten--------
```

### POST /auth_api/v1/process/authenticate/password_recovery/reset
```
--------Resetting Password--------
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