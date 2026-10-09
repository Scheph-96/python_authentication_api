# Authentication API

This project is a standalone authentication service for us who no longer want to go through the burden of creating
authentication services for each project, this project is a full **Python** and **MongoDB** based project, using
**FastAPI** and **Motor**.

## Prerequisites

> Python 3.14+

## Getting Started

Follow these steps to initialize the api before running it\

1. Create jwt private and public keys

```shell
# In the terminal navigate to app/keys/ in the project folder and run:

# Create the private key
openssl genrsa -out private.pem 2048

# From that private key, create the public key
openssl rsa -in private.pem -pubout -out public.pem
```

Learn more in [Authentication.md](docs/authentication.md)

2. Create a virtual environment and install required package listed in requirements.txt

```shell
# In the terminal navigate to the project root and run:

# Create a virtual environment:
python3 -m venv <your_environment_name>

# Activate the virtual environment:
source <your_environment_name>/bin/activate

# Install required packages:
pip install -r requirements.txt
```

3. Update environment variables\
   These variables are initialized for code in [Settings](app/core/config.py)

```shell
# In the project root create .env file and update variables.
# See below for default values:

APP_HOST=127.0.0.1
APP_PORT=8000
DATABASE_URI=mongodb://127.0.0.1:27017/rbac_api_db
DATABASE_NAME=rbac_api_db
ENV=development
API_PREFIX=/rbac_api
COMPANY_NAME="MY_COMPANY INC."
PRIVATE_KEY_PATH="keys/private.pem" #Settings code resolves keys/... relative to app/
PUBLIC_KEY_PATH="keys/public.pem" #Settings code resolves keys/... relative to app/
ACCESS_TOKEN_EXPIRATION_MINUTES=5
REFRESH_TOKEN_EXPIRATION_DAYS=15
PASSWORD_RECOVERY_TOKEN_EXPIRATION_MINUTES=30
EMAIL_VALIDATION_CODE_EXPIRATION_HOURS=1
ISSUER=APP_RBAC_API
 # SMTP configs are optional if email validation is not enabled, which is the case by default.
 # See Settings 
SMTP_HOST=
SMTP_PORT=0
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=
```

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
    - [Password recovery](docs/password_recovery.md)
    - [Clean logout](docs/logout.md)
- Authorization
    - Role and permissions interface
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

## Authorization Interface
- Roles are assigned to users
- Permissions are assigned to roles
- Effective permissions are computed and stored on the user

Authorization is excepted to be enforced by the consumer backend. [Learn more](docs/authorization.md)

## API Endpoints

### Authentication

```
POST /auth_api/v1/process/authenticate/register/
POST /auth_api/v1/process/authenticate/login/
POST /auth_api/v1/process/authenticate/logout/
POST /auth_api/v1/process/authenticate/validate_email/
POST /auth_api/v1/process/authenticate/validate_email/retry/
POST /auth_api/v1/process/authenticate/refresh/tokens/
POST /auth_api/v1/process/authenticate/password_recovery/forgot/
POST /auth_api/v1/process/authenticate/password_recovery/reset/
```

### Authorization

```
POST /auth_api/v1/process/authorize/create_role/
POST /auth_api/v1/process/authorize/assign_role/
POST /auth_api/v1/process/authorize/remove_user_role/
POST /auth_api/v1/process/authorize/delete_role/
POST /auth_api/v1/process/authorize/create_permissions/
POST /auth_api/v1/process/authorize/assign_permission/
POST /auth_api/v1/process/authorize/remove_role_permission/
POST /auth_api/v1/process/authorize/delete_permission/
```

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
Check [logging](docs/logging.md)

## Integration Notes

- This service does not enforce authorization
- Consumer backend must check permissions
- Tokens contain user_id and permissions

## FileSystem
[Check it out](docs/project_filesystem.md)


## Conclusion
Keep in mind that this api is a standalone reusable authentication api,
all it does is authentication and provide an authorization
interface **IT DOES NOTHING MORE** all the processing and
handling and computation and so on are done by the consumer
**YOUR BACKEND**
