## Database Architecture

## Overview
For a standalone authentication api their are only a few collections to validate data and authenticate users. So we have users, email_validation_code, password_recovery_token, refresh_tokens. (You might want to forgive my poor naming skills 😅)

Name the database how you want (The value is environment variables). If you want to change collections name it's possible in app/api/v1/user_controller.py under 
```
#Dependency: user repository
def get_user_repository():
    return UserRepository(db.users)

Change db.<users> with db.<anything> to change users collection name
```

## Collections
### users 
Update it with your project user model but these fields are **mandatory**
```
    username: string
    email: string
    hashed_password: string
    is_verified: boolean
    create_at: date
    auth_version: integer
```

### email_validation_code
After registration we generate a code that is send to the user email to validate his email address. We have to keep a record of the generated code
```
    user_id: string
    code_hash: string // the code sent to user are not stored raw
    created_at: date
    expire_at: date
```

### Indexes
```
    expire_at: TTL index, auto delete document
```

### password_recovert_tokens
Users will reset their password when they forget it, the recovery token is generated when the email provided in the password recovery process is validate. This token is then use to reset the password
```
    user_id: string
    token_hash: string
    expire_at: string
    created_at: string
    used: boolean
```

### Indexes
```
    expire_at: TTL index, auto delete document
```

### refreah_tokens
Refresh tokens are used to keep the user session alive

```
    user_id: string
    token_hash: string
    auth_version: integer // Need to have the same value as the attribute in users collection or the token is invalid
    replaced_by: string // new generated token when this one is revoked
    expire_at: date
    created_at: date
```

### Indexes
```
    token_hash: Unique index
    user_id: speed up queries by creating pointer structure
    expire_at: TTL index, auto delete document
```
