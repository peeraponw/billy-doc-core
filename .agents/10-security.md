# 10. Security Requirements

## 10.1 Secrets and Credentials

* Secrets MUST NOT be committed to the repository.
* Secrets MUST come from environment variables, secret stores, or configuration services.

## 10.2 Database and External Services

* All database access MUST use parameterized queries or ORM methods that generate such queries.
* User input MUST NOT be concatenated into SQL strings.

```python
# ❌ Forbidden
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")


# ✅ Required
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

## 10.3 Input Validation

* All inbound data from clients MUST be validated with Pydantic models or explicit validators before use.
