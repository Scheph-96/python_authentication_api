# User creation System Workflow

## Overview
To create an account users provide username,email and password, after validation we hash the password and store the user data. An confirmation is asynchronously sent to validate the email.

## User creation Flow
1. Data provided by the user
2. Data validation
3. Password hashed
4. User record store in database
5. Return user id and send validaiton email

After registration the user has to login

(I might make the email validation optional for quick tests and lightweight apps)