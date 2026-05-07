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
``````

### POST /auth_api/v1/process/authenticate/logout/
``````

### POST /auth_api/v1/process/authenticate/validate_email/
``````

### POST /auth_api/v1/process/authenticate/validate_email/retry/
``````

### POST /auth_api/v1/process/authenticate/refresh/tokens/
``````

### POST /auth_api/v1/process/authenticate/password_recovery/forgot/
``````

### POST /auth_api/v1/process/authenticate/password_recovery/reset
``````

## Authorization

### POST /auth_api/v1/process/authorize/create_role/
``````

### POST /auth_api/v1/process/authorize/assign_role/
``````

### POST /auth_api/v1/process/authorize/remove_user_role/
``````

### POST /auth_api/v1/process/authorize/delete_role/
``````

### POST /auth_api/v1/process/authorize/create_permissions/
``````

### POST /auth_api/v1/process/authorize/assign_permission_to_role/
``````

### POST /auth_api/v1/process/authorize/remove_permission_from_role/
``````

POST /auth_api/v1/process/authorize/delete_permission/
``````