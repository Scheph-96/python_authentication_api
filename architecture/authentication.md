# Authentication System Workflow

## Overview
This system uses JWT (RS256) for authentication with refresh token rotation.
- A dedicated Auth API(FastAPI) is responsible for login and token issuance.
- Other projects backends trust this Auth API and verify JWTs using the public key.
- Access tokens are short-lived; refresh tokens maintain long sessions securely.

## What is auth_version?
auth_version is a per-user session version number stored in the database.
Each refresh token stores the version at creation time.
A refresh token is considered valid only if its stored version matches the user's current auth_version.

Incrementing auth_version immediately invalidates all existing refresh tokens and prevents further session renewal.

The rule is:

>A token is valid ony if\
refresh_token.auth_version == user.auth_version

## When is this used?

auth_version is usefull when we want to:

Logout all devices\
Password change invalidates sessions

## Authentication Flow
1. Credentials are sent to Auth API
2. Auth API validate credentials
3. Auth API returns:
    - Access Token (15 min)
    - Refresh Token (30 days)

## Protected Route Flow
Frontend → Backend\
Header: Authorization: Bearer <access_token>

The backend that consumes this Auth system verifies:
- JWT signature using the RS256 public key
- Token expiration
- Issuer (iss)
- Subject (sub = user_id)

If valid → request proceeds.
If invalid/expired → return 401 Unauthorized

## Token Expiration Flow
1. Access token expires
2. Backend rejects request with 401
3. Frontend calls /auth/refresh
4. Auth API verifies refresh token:
    - Token hash exist in database
    - Not revoked
    - Not expired
    - auth version match
5. If valid:
    - New access token issued
    - New refresh token issued (rotation)
    - Old refresh token mark revoked
6. Frontend retries the original request using the new access token

If refresh token is invalid or expired → user must log in again

## Refresh Token Storage Model
Refresh tokens are never stored raw.

Database record:

| Field        | Purpose                                   |
|--------------|-------------------------------------------|
| token_hash   | SHA256 hash of refresh token              |
| user_id      | Token owner                               |
| auth_version | Assure token validity                     |
| expire_at    | Expiration time (TTL indexed)             |
| revoked      | Whether token is invalid                  |
| replaced_by  | Hash of new token created during rotation |
| created_at   | Creation time                             |

Expired tokens are automatically deleted using a MongoDB TTL index

## Security Features
- RS256 asymmetric signing
   * Private key → Auth API
   * Public key → Backend consumer
- Short-lived access tokens
- Hashed refresh token
- Refresh token rotation
- Revocation tracking
- TTL-based automatic cleanup
- Protection against refresh token replay attacks
