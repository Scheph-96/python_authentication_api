## Database Architecture

## Overview
For a standalone authentication api there are only a few collections
to validate data and authenticate users. So we have (You might want to forgive my poor naming skill):

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

Name the database whatever you want (The value is in environment variables).\
If you want to change collections name it's possible in [Settings](../app/core/config.py)

## Collections

```
############# UNIQUE INDEXES #############
    The "1" stand for the order of sorting. 1 Ascending order -1 Descending order
    token_hash must be unique
    
############# EXPIRATION INDEXES #############
    Delete the document as soon as the date stored in that field is reached.
    current_time >= expire_at
    expireAfterSeconds=0. Delete time is exactly the time set in the document
    
############# LOOKUP INDEXES #############
    Without an index Mongo does a collection scan (checks every document).
    With an index Mongo uses a pointer structure to jump directly to matches,
    which accelerate find queries
    
    The collection
    {key1: value1, key2: value2} -> doc1
    {key1: value3, key2: value4} -> doc2
    {key1: value5, key2: value6} -> doc3
    {key1: value1, key2: value7} -> doc4
    
    While creating an index on an attribute 
    for example in this case
        `(db.collection.create_index("key1": 1))`
    mongodb create something like this:
    
    value1-  [doc1, doc4]
    value3-  doc2
    value5-  doc3
    
    When a `find` query is done, instead of looking
    for each document in the collection, mongodb
    jump to indexes and resolve the query by just
    picking the corresponding index
```

### Authentication

#### users 
Update it with your project user model but these fields are **mandatory**
```
---Atributes---
username: string
email: string
hashed_password: string
is_verified: boolean
effective_permissions: list
created_at: date
auth_version: integer

---Indexes---
email: Unique index
username: Unique index
```

#### email_validation_code
After registration, we generate a code that is sent to the user email to validate his email address. We have to keep a record of the generated code
```
---Attributes---
user_id: string
code_hash: string // the code sent to user are not stored raw
created_at: date
expire_at: date

---Indexes---
expire_at: TTL index, auto delete document
```

#### password_recovert_tokens
Users will reset their password when they forget it, the recovery token is generated when the email provided in the password recovery process is validate. This token is then use to reset the password
```
---Attributes---
user_id: string
token_hash: string
expire_at: string
created_at: string
used: boolean

---Indexes---
expire_at: TTL index, auto delete document
```

#### refresh_tokens
Refresh tokens are used to keep the user session alive

```
---Attributes---
user_id: string
token_hash: string
auth_version: integer // Need to have the same value as the attribute in users collection or the token is invalid
replaced_by: string // new generated token when this one is revoked
expire_at: date
created_at: date

---Indexes---
token_hash: Unique index
user_id: speed up queries by creating pointer structure
expire_at: TTL index, auto delete document
```

### Authorization

#### roles
Roles that will be assigned to users

```
---Attributes---
role_name: string
description: string // A brief description of the role

---Indexes---
role_name: Unique index
```

#### permissions
Permissions granted by a role

```
---Attributes---
permission_name: string

---Indexes---
permission_name: Unique index
```

#### role_permissions
A many-to-many relation table between roles and permissions

```
---Attributes---
role_id: ObjectId
permission_id: ObjectId

---Indexes---
{"role_id", "permission_id"}: Unique index
role_id: speed up queries by creating pointer structure
permission_id: speed up queries by creating pointer structure
```

#### user_roles
A many-to-many relation table between roles and users

```
--Attributes---
role_id: ObjectId
user_id: ObjectId

---Indexes---
{"user_id", "role_id"}: Unique index
role_id: speed up queries by creating pointer structure
user_id: speed up queries by creating pointer structure
```
