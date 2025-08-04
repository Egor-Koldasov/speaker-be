Refactor the database schema.

No backward compatibility is required, including database migrations. Do the full reset.

New tables:

```
profile
  id
  name
  auth_user_id

auth_user
  id
  email // unique

auth_password
  id
  password_hash
  auth_user_id

otp
  code // primary key
  auth_user_id
```

- New database rule: all ids are uuidv7, no database generated ids are used. Make this a project rule.
- Name cannot be empty, but user can skip it during registration, which will use email part before `@`.
- `/me` will return both `profile` and `auth_user`


## Next

### Extract e2e user table

```
e2e_user
  id
  auth_user_id
```
The user is marked as e2e user if the record is present.

### Cleanup models

