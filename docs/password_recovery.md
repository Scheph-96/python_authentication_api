# Password Recovery System Workflow

## Overview
In this process a token is issued then a link is generated with the token to the page where the user can reset his password
- This API doesn't generate links.
- Other projects backends (consumers) get the recovery token from the AUTH API.
- Recovery token last 30 minutes.

The recovery process include:
- Email validation
- Token issuing
- Token validation
- Password reset
- Increment auth version

## Email validation Flow

> POST users/auth/password_recovery/forgot

1. User provide email
2. Auth API validate user existence with email
3. A token is generated
4. Store hash token
5. Return raw token

No email, No HTML, No links. **Pure security responsibility**

## Consumer backend builds the link

For Web
>app.example.com/reset-password?token=hQF8cY2k9pL

For Mobile
>myapp://reset-password?token=hQF8cY2k9pL

Then send the link via email

## Password Recovery Token Expiration Flow

> POST /users/auth/password_recovery/reset

1. new password and password recovery token are sent (user_id is in password recovery token model, see below)
2. Hash token
3. Validate token expiry and verify if used
4. Invalidate token
5. Hash new password
6. Increment auth version
7. Return success

## Password Recovery Token Storage Model
Password Recovery tokens are never stored raw.

Database record:

| Field           | Purpose                                   |
|-----------------|-------------------------------------------|
|  token_hash     | SHA256 hash of refresh token              |
| user_id         | Token owner                               |
| expire_at       | Expiration time (TTL indexed)             |
| used            | Whether the token was already used ot not |
| created_at      | Creation time                             |

Expired tokens are automatically deleted using a MongoDB TTL index