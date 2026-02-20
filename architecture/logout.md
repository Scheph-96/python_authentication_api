# Logout System Workflow

## Overview
To log out user we have to discard tokens, to forbid every future request.
- Increment authentication version.
- Revoke refresh token.
- Access token is short lived (5-15 min), no operation will be done we will just let it die(expire).

## Logout Flow
1. Validate refresh token
2. Revoke token
3. Increment auth version
4. Return success (True)

## What happens on logout

When user logs out:

`UPDATE users SET auth_version = auth_version + 1`

Now:

>Old tokens:
ver = 0\
Database:
ver = 1


Mismatch → reject token.

All previously issued tokens instantly invalid.