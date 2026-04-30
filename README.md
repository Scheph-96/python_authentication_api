# Authentication API

This project is a standalone authentication service for us who no longer want to go through the burden of creating
authentication services for each project, this project is a full **Python** and **MongoDB** based project, using
**FastAPI** and **Motor**.

## Architecture
The system follows a layered architecture:
- Controller → handle HTTP requests
- Service → Contain business logic
- Repositories → handle database access
- Pipelines → handle feature-based workflow

```
Client → Controller → Service → Repository → Database 
```

## Features

The following features are available in the project:

- Authentication
    - Data validation and sanitization
    - Password hashing
    - Access and Refresh token handler
    - Email validation process
    - Password recovery
    - Clean logout
- Authorization
    - Role and permissions management
- Console and File logging
- Error handler

## Core Concepts

### User
Represent an authenticated entity.

### Role
A collection of permissions.

### Permission
A granular action (e.g `user.create`, `article.delete`).

### Effective Permissions
A cached list of permissions computed from user roles.

[Learn more](docs/core_concepts.md)

## Authentication Flow
1. Credentials are sent to Auth API
2. Optional steps:
    - email validation
    - role assignment
3. Auth API validate credentials and log user in
4. Auth API returns:
    - Access Token (15 min)
    - Refresh Token (30 days)

[Learn more](docs/authentication.md)

## Authorization Model
- Roles are assigned to users
- Permissions are assigned to roles
- Effective permissions are computed and stored on the user

Authorization is excepted to be enforced by the consumer backend. [Learn more](docs/authrization.md)

## API Endpoints

### Authentication

**POST** /auth_api/v1/process/authenticate/register\
**POST** /auth_api/v1/process/authenticate/login\
**POST** /auth_api/v1/process/authenticate/logout\
**POST** /auth_api/v1/process/authenticate/validate_email\
**POST** /auth_api/v1/process/authenticate/validate_email/retry\
**POST** /auth_api/v1/process/authenticate/refresh/tokens\
**POST** /auth_api/v1/process/authenticate/password_recovery/forgot\
**POST** /auth_api/v1/process/authenticate/password_recovery/reset

### Authorization

**POST** /auth_api/v1/process/authorize/create_role\
**POST** /auth_api/v1/process/authorize/assign_role\
**POST** /auth_api/v1/process/authorize/remove_user_role\
**POST** /auth_api/v1/process/authorize/delete_role\
**POST** /auth_api/v1/process/authorize/create_permissions\
**POST** /auth_api/v1/process/authorize/assign_permission_to_role\
**POST** /auth_api/v1/process/authorize/remove_permission_from_role\
**POST** /auth_api/v1/process/authorize/delete_permission

[Learn more](docs/endpoints.md)

## Pipelines

The system uses pipelines to compose features dynamically.

Example: Registration pipeline
- EmailVerificationStep (optional)
- AssignRoleStep (optional)

Pipelines are configured via settings. [Learn more](docs/pipeline.md)

## Database Architecture

For a standalone authentication api there are only a few collections to validate data and authenticate users. So we have (You might want to forgive my poor naming skill):
- Authentication
  - users
  - email_validation_code
  - password_recovery_token
  - refresh_tokens
- Authorization
  - roles
  - user_roles
  - permissions
  - role_permissions

[Learn more](docs/database.md)

## Errors

- Authentication\
    For security reason authentication errors are not verbose for the end user but logs show every detail

- Authorization\
    Errors follow a structured format:
```    
    {
        "error": "ROLE_ALREADY_EXISTS",
        "message": "Role already exists"
      }
```

## Integration Notes

- This service does not enforce authorization
- Consumer backend must check permissions
- Tokens contain user_id and permissions


Keep in mind that this api is a standalone reusable authentication api,
all it does is authentication and provide an authorization
interface **IT DOES NOTHING MORE** all the processing and
handling and computation and so on are done by the consumer
**YOUR BACKEND**
