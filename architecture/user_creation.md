# User creation System Workflow

## Overview
To create an account users provide username,email and password, after validation we hash the password and store the user data. A confirmation code is asynchronously sent to validate their email.

## User creation Flow
1. User provide data
2. Data validation
3. Password hashe
4. User credentials store in database
5. User create
6. Return user id and send validaiton email

After registration the user has to login

(I might make the email validation optional for quick tests and lightweight apps) => AND I DID IT. With pipelines